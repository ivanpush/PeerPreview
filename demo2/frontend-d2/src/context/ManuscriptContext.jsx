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
  const [dismissedIssues, setDismissedIssues] = useState(new Set());
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const updateParagraph = useCallback((paragraphId, newText, isRewrite = false, isRevert = false, isDelete = false) => {
    if (!manuscript) return;

    // Find the paragraph to store previous state
    const paragraph = manuscript.paragraphs.find(p => p.paragraph_id === paragraphId);
    if (!paragraph) return;

    setLastRewrite({
      paragraphId,
      previousText: paragraph.text,
      newText,
      timestamp: Date.now()
    });

    // If deleting, mark as deleted and preserve previous state
    if (isDelete) {
      const originalText = paragraph.originalText || paragraph.text;
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

  const value = {
    // State
    manuscript,
    issues,
    biasProfile,
    lastRewrite,
    selectedIssue,
    activeFigureId,
    dismissedIssues,
    loading,
    error,

    // Actions
    updateParagraph,
    undoLastRewrite,
    restoreDeleted,
    setSelectedIssue,
    setActiveFigureId,
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
