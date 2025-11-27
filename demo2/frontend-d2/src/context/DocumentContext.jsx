import React, { createContext, useContext, useState, useCallback } from 'react';

const DocumentContext = createContext();

export const useDocument = () => {
  const context = useContext(DocumentContext);
  if (!context) {
    throw new Error('useDocument must be used within DocumentProvider');
  }
  return context;
};

export const DocumentProvider = ({ children }) => {
  const [document, setDocument] = useState(null);
  const [issues, setIssues] = useState([]);
  const [biasProfile, setBiasProfile] = useState(null);
  const [lastRewrite, setLastRewrite] = useState(null);
  const [selectedIssue, setSelectedIssue] = useState(null);
  const [activeFigureId, setActiveFigureId] = useState(null);
  const [dismissedIssues, setDismissedIssues] = useState(new Set());
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const updateParagraph = useCallback((paragraphId, newText, isRewrite = false, isRevert = false, isDelete = false) => {
    if (!document) return;

    // Find the paragraph to store previous state
    const paragraph = document.paragraphs.find(p => p.paragraph_id === paragraphId);
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
      setDocument(prev => ({
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
      setDocument(prev => ({
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
    setDocument(prev => ({
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
  }, [document]);

  const undoLastRewrite = useCallback(() => {
    if (!lastRewrite || !document) return;

    setDocument(prev => ({
      ...prev,
      paragraphs: prev.paragraphs.map(p =>
        p.paragraph_id === lastRewrite.paragraphId
          ? { ...p, text: lastRewrite.previousText, isRewritten: false, isEdited: false }
          : p
      )
    }));

    setLastRewrite(null);
  }, [lastRewrite, document]);

  const restoreDeleted = useCallback((paragraphId) => {
    if (!document) return;

    const paragraph = document.paragraphs.find(p => p.paragraph_id === paragraphId);
    if (!paragraph) return;

    setDocument(prev => ({
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
  }, [document]);

  const loadMockData = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      // Check if we have backend review results (from dynamic mode)
      const reviewResultStr = sessionStorage.getItem('reviewResult');

      if (reviewResultStr) {
        // Dynamic mode: Use backend review results
        const reviewResult = JSON.parse(reviewResultStr);

        // Load document and bias profile (but use backend issues)
        const [documentRes, biasProfileRes] = await Promise.all([
          fetch('/static/manuscript_demo.json'),  // Keep filename as is - it's a specific demo file
          fetch('/static/bias_profile_demo.json')
        ]);

        if (!documentRes.ok || !biasProfileRes.ok) {
          throw new Error('Failed to load demo data');
        }

        const [documentData, biasProfileData] = await Promise.all([
          documentRes.json(),
          biasProfileRes.json()
        ]);

        // Use backend issues instead of static ones
        setDocument(documentData);
        setIssues(reviewResult.issues || []);
        setBiasProfile(biasProfileData);

        // Clear the review result from session
        sessionStorage.removeItem('reviewResult');
      } else {
        // Static mode: Load all three files
        const [documentRes, issuesRes, biasProfileRes] = await Promise.all([
          fetch('/static/manuscript_demo.json'),  // Keep filename as is - it's a specific demo file
          fetch('/static/issues_demo.json'),
          fetch('/static/bias_profile_demo.json')
        ]);

        if (!documentRes.ok || !issuesRes.ok || !biasProfileRes.ok) {
          throw new Error('Failed to load demo data');
        }

        const [documentData, issuesData, biasProfileData] = await Promise.all([
          documentRes.json(),
          issuesRes.json(),
          biasProfileRes.json()
        ]);

        setDocument(documentData);
        setIssues(issuesData);
        setBiasProfile(biasProfileData);

        // Set first figure as active by default
        if (documentData.figures?.length > 0) {
          setActiveFigureId(documentData.figures[0].figure_id);
        }
      }

      setLoading(false);
    } catch (err) {
      console.error('Error loading mock data:', err);
      setError(err.message);
      setLoading(false);
    }
  }, []);

  const getParagraphById = useCallback((paragraphId) => {
    if (!document) return null;
    return document.paragraphs.find(p => p.paragraph_id === paragraphId);
  }, [document]);

  const getSectionById = useCallback((sectionId) => {
    if (!document) return null;
    return document.sections.find(s => s.section_id === sectionId);
  }, [document]);

  const getIssuesByTrack = useCallback((track) => {
    if (track === 'all') return issues;
    return issues.filter(issue => issue.track === track);
  }, [issues]);

  const value = {
    // State
    document,
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
    <DocumentContext.Provider value={value}>
      {children}
    </DocumentContext.Provider>
  );
};
