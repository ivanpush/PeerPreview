import React, { createContext, useContext, useState, useCallback } from 'react';

const ManuscriptContext = createContext();

export const useManuscript = () => {
  const context = useContext(ManuscriptContext);
  if (!context) {
    throw new Error('useManuscript must be used within ManuscriptProvider');
  }
  return context;
};

export const ManuscriptProvider = ({ children }) => {
  const [manuscript, setManuscript] = useState(null);
  const [issues, setIssues] = useState([]);
  const [biasProfile, setBiasProfile] = useState(null);
  const [lastRewrite, setLastRewrite] = useState(null);
  const [selectedIssue, setSelectedIssue] = useState(null);
  const [activeFigureId, setActiveFigureId] = useState(null);
  const [acceptedIssues, setAcceptedIssues] = useState(new Set());
  const [acceptedWithRewrite, setAcceptedWithRewrite] = useState(new Set()); // Track which accepted issues had rewrites
  const [dismissedIssues, setDismissedIssues] = useState(new Set());
  const [userEdits, setUserEdits] = useState(new Map()); // Track all user edits and deletions
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const updateParagraph = useCallback((paragraphId, newText, isRewrite = false, isRevert = false, isDelete = false) => {
    if (!manuscript) return;

    // Find the paragraph to store previous state
    const paragraph = manuscript.paragraphs.find(p => p.paragraph_id === paragraphId);
    if (!paragraph) return;

    // Get section info for user edits tracking
    const section = manuscript.sections.find(s => s.section_id === paragraph.section_id);
    const sectionName = section?.title || section?.name || paragraph.section_id.replace('sec_', '').toUpperCase();
    const paragraphNumber = manuscript.paragraphs.filter(p => p.section_id === paragraph.section_id)
      .findIndex(p => p.paragraph_id === paragraphId) + 1;

    setLastRewrite({
      paragraphId,
      previousText: paragraph.text,
      newText,
      timestamp: Date.now()
    });

    // If deleting, mark as deleted and track in userEdits
    if (isDelete) {
      const originalText = paragraph.originalText || paragraph.text;

      // Track in userEdits if it's a manual deletion (not part of an AI rewrite)
      if (!isRewrite) {
        setUserEdits(prev => {
          const newEdits = new Map(prev);
          newEdits.set(paragraphId, {
            id: `edit_${paragraphId}_${Date.now()}`,
            paragraphId,
            type: 'deleted',
            originalText: originalText,
            currentText: '',
            timestamp: new Date(),
            sectionId: paragraph.section_id,
            sectionName: sectionName,
            paragraphNumber
          });
          return newEdits;
        });
      }

      setManuscript(prev => ({
        ...prev,
        paragraphs: prev.paragraphs.map(p =>
          p.paragraph_id === paragraphId
            ? {
                ...p,
                isDeleted: true,
                originalText: originalText,
                // Store previous flags to restore later
                wasRewritten: p.isRewritten,
                wasEdited: p.isEdited
              }
            : p
        )
      }));
      return;
    }

    // If reverting, clear all flags and restore original
    if (isRevert) {
      // Remove from userEdits if reverting to original
      const originalText = paragraph.originalText;
      if (originalText && newText === originalText) {
        setUserEdits(prev => {
          const newEdits = new Map(prev);
          newEdits.delete(paragraphId);
          return newEdits;
        });
      }

      setManuscript(prev => ({
        ...prev,
        paragraphs: prev.paragraphs.map(p =>
          p.paragraph_id === paragraphId
            ? {
                ...p,
                text: newText,
                isRewritten: false,
                isEdited: false,
                isDeleted: false,
                originalText: undefined // Clear original since we're back to it
              }
            : p
        )
      }));
      return;
    }

    // Store original text if this is the first edit
    const originalText = paragraph.originalText || paragraph.text;
    const isEdited = !isRewrite; // Manual edits are marked as "edited", rewrites as "rewritten"

    // Track manual edits (not AI rewrites) in userEdits
    if (isEdited && newText !== originalText) {
      setUserEdits(prev => {
        const newEdits = new Map(prev);
        newEdits.set(paragraphId, {
          id: `edit_${paragraphId}_${Date.now()}`,
          paragraphId,
          type: 'edited',
          originalText: originalText,
          currentText: newText,
          timestamp: new Date(),
          sectionId: paragraph.section_id,
          sectionName: sectionName,
          paragraphNumber
        });
        return newEdits;
      });
    }

    // Update paragraph text while preserving metadata and marking status
    setManuscript(prev => ({
      ...prev,
      paragraphs: prev.paragraphs.map(p =>
        p.paragraph_id === paragraphId
          ? {
              ...p,
              text: newText,
              isRewritten: isRewrite,
              isEdited: isEdited,
              isDeleted: false,
              originalText: originalText
            }
          : p
      )
    }));
  }, [manuscript]);

  const undoLastRewrite = useCallback(() => {
    if (!lastRewrite || !manuscript) return;

    setManuscript(prev => ({
      ...prev,
      paragraphs: prev.paragraphs.map(p =>
        p.paragraph_id === lastRewrite.paragraphId
          ? { ...p, text: lastRewrite.previousText, isRewritten: false, isEdited: false }
          : p
      )
    }));

    setLastRewrite(null);
  }, [lastRewrite, manuscript]);

  const restoreDeleted = useCallback((paragraphId) => {
    if (!manuscript) return;

    const paragraph = manuscript.paragraphs.find(p => p.paragraph_id === paragraphId);
    if (!paragraph) return;

    // Remove from userEdits when restoring deleted paragraph
    setUserEdits(prev => {
      const newEdits = new Map(prev);
      // Check if this paragraph has a deleted entry
      if (newEdits.has(paragraphId) && newEdits.get(paragraphId).type === 'deleted') {
        newEdits.delete(paragraphId);
      }
      return newEdits;
    });

    setManuscript(prev => ({
      ...prev,
      paragraphs: prev.paragraphs.map(p =>
        p.paragraph_id === paragraphId
          ? {
              ...p,
              isDeleted: false,
              isRewritten: p.wasRewritten || false,
              isEdited: p.wasEdited || false,
              wasRewritten: undefined,
              wasEdited: undefined
            }
          : p
      )
    }));
  }, [manuscript]);

  const loadMockData = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      // Load all three files in parallel
      const [manuscriptRes, issuesRes, biasProfileRes] = await Promise.all([
        fetch('/static/manuscript_demo.json'),
        fetch('/static/issues_demo.json'),
        fetch('/static/bias_profile_demo.json')
      ]);

      if (!manuscriptRes.ok || !issuesRes.ok || !biasProfileRes.ok) {
        throw new Error('Failed to load demo data');
      }

      const [manuscriptData, issuesData, biasProfileData] = await Promise.all([
        manuscriptRes.json(),
        issuesRes.json(),
        biasProfileRes.json()
      ]);

      setManuscript(manuscriptData);
      setIssues(issuesData);
      setBiasProfile(biasProfileData);

      // Set first figure as active by default
      if (manuscriptData.figures?.length > 0) {
        setActiveFigureId(manuscriptData.figures[0].figure_id);
      }

      setLoading(false);
    } catch (err) {
      console.error('Error loading mock data:', err);
      setError(err.message);
      setLoading(false);
    }
  }, []);

  const getParagraphById = useCallback((paragraphId) => {
    if (!manuscript) return null;
    return manuscript.paragraphs.find(p => p.paragraph_id === paragraphId);
  }, [manuscript]);

  const getSectionById = useCallback((sectionId) => {
    if (!manuscript) return null;
    return manuscript.sections.find(s => s.section_id === sectionId);
  }, [manuscript]);

  const getIssuesByTrack = useCallback((track) => {
    if (track === 'all') return issues;
    return issues.filter(issue => issue.track === track);
  }, [issues]);

  const revertUserEdit = useCallback((paragraphId) => {
    if (!manuscript || !userEdits.has(paragraphId)) return;

    const edit = userEdits.get(paragraphId);
    const paragraph = manuscript.paragraphs.find(p => p.paragraph_id === paragraphId);
    if (!paragraph) return;

    // Remove from userEdits
    setUserEdits(prev => {
      const newEdits = new Map(prev);
      newEdits.delete(paragraphId);
      return newEdits;
    });

    // Revert to original text
    updateParagraph(paragraphId, edit.originalText, false, true);
  }, [manuscript, userEdits, updateParagraph]);

  const exportReview = useCallback(() => {
    if (!manuscript) return null;

    // Prepare export data
    const exportData = {
      metadata: {
        exportDate: new Date().toISOString(),
        documentTitle: manuscript.title || 'Untitled Document',
        totalIssues: issues.length,
        acceptedIssues: acceptedIssues.size,
        dismissedIssues: dismissedIssues.size,
        userEdits: userEdits.size
      },
      manuscript: {
        ...manuscript,
        // Include edited paragraphs with their current state
        paragraphs: manuscript.paragraphs.map(p => ({
          ...p,
          exportStatus: p.isRewritten ? 'rewritten' : p.isEdited ? 'edited' : p.isDeleted ? 'deleted' : 'original'
        }))
      },
      acceptedIssues: Array.from(acceptedIssues).map(issueId => {
        const issue = issues.find(i => i.id === issueId);
        return {
          ...issue,
          wasRewritten: acceptedWithRewrite.has(issueId)
        };
      }),
      dismissedIssues: Array.from(dismissedIssues),
      userEdits: Array.from(userEdits.values()),
      statistics: {
        totalParagraphs: manuscript.paragraphs.length,
        editedParagraphs: manuscript.paragraphs.filter(p => p.isEdited).length,
        rewrittenParagraphs: manuscript.paragraphs.filter(p => p.isRewritten).length,
        deletedParagraphs: manuscript.paragraphs.filter(p => p.isDeleted).length
      }
    };

    // Convert to JSON and trigger download
    const dataStr = JSON.stringify(exportData, null, 2);
    const dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr);

    const exportFileDefaultName = `peer_review_${new Date().toISOString().split('T')[0]}.json`;

    const linkElement = document.createElement('a');
    linkElement.setAttribute('href', dataUri);
    linkElement.setAttribute('download', exportFileDefaultName);
    linkElement.click();

    return exportData;
  }, [manuscript, issues, acceptedIssues, acceptedWithRewrite, dismissedIssues, userEdits]);

  const value = {
    // State
    manuscript,
    issues,
    biasProfile,
    lastRewrite,
    selectedIssue,
    activeFigureId,
    acceptedIssues,
    acceptedWithRewrite,
    dismissedIssues,
    userEdits,
    loading,
    error,

    // Actions
    updateParagraph,
    undoLastRewrite,
    restoreDeleted,
    revertUserEdit,
    exportReview,
    setSelectedIssue,
    setActiveFigureId,
    setAcceptedIssues,
    setAcceptedWithRewrite,
    setDismissedIssues,
    loadMockData,

    // Helpers
    getParagraphById,
    getSectionById,
    getIssuesByTrack,
  };

  return (
    <ManuscriptContext.Provider value={value}>
      {children}
    </ManuscriptContext.Provider>
  );
};
