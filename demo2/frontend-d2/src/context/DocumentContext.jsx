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
      // Check session storage for demo selection
      const reviewResultStr = sessionStorage.getItem('reviewResult');
      const selectedDemo = sessionStorage.getItem('selectedDemo');
      const demoFile = sessionStorage.getItem('demoFile');

      console.log('loadMockData called with:', { reviewResultStr: !!reviewResultStr, selectedDemo, demoFile });

      if (reviewResultStr && demoFile) {
        // Dynamic mode: Use backend review results with selected fixture
        const reviewResult = JSON.parse(reviewResultStr);

        // Load the selected fixture file
        const fixtureRes = await fetch(`/fixtures/${demoFile}`);

        if (!fixtureRes.ok) {
          throw new Error('Failed to load selected demo fixture');
        }

        const fixtureData = await fixtureRes.json();

        // Extract document data from fixture
        const documentData = {
          document_id: fixtureData.manuscript_id || fixtureData.document_id,
          manuscript_id: fixtureData.manuscript_id,
          title: fixtureData.title,
          sections: fixtureData.sections || [],
          paragraphs: fixtureData.paragraphs || [],
          figures: fixtureData.figures || [],
          tables: fixtureData.tables || [],
          authors: fixtureData.authors || [],
          affiliations: fixtureData.affiliations || [],
          metadata: fixtureData.meta || {},
          source_format: fixtureData.source_format,
          document_type: fixtureData.document_type
        };

        // Backend will provide real bias analysis
        const mockBiasProfile = {
          document_id: fixtureData.manuscript_id || fixtureData.document_id,
          biases: []  // Backend will provide real bias analysis
        };

        // Use backend issues instead of fixture issues
        setDocument(documentData);
        setIssues(reviewResult.issues || []);
        setBiasProfile(mockBiasProfile);

        // Set first figure as active by default
        if (documentData.figures?.length > 0) {
          setActiveFigureId(documentData.figures[0].figure_id);
        }

        // Clear the review result from session
        sessionStorage.removeItem('reviewResult');
      } else if (selectedDemo && demoFile) {
        // Static demo mode: Load selected fixture
        console.log('Loading static demo fixture:', `/fixtures/${demoFile}`);
        const fixtureRes = await fetch(`/fixtures/${demoFile}`);

        if (!fixtureRes.ok) {
          console.error('Failed to load fixture:', fixtureRes.status, fixtureRes.statusText);
          throw new Error('Failed to load demo fixture');
        }

        const fixtureData = await fixtureRes.json();
        console.log('Fixture loaded:', fixtureData.title, fixtureData.document_type);

        // Extract document data from fixture
        const documentData = {
          document_id: fixtureData.manuscript_id || fixtureData.document_id,
          manuscript_id: fixtureData.manuscript_id,
          title: fixtureData.title,
          sections: fixtureData.sections || [],
          paragraphs: fixtureData.paragraphs || [],
          figures: fixtureData.figures || [],
          tables: fixtureData.tables || [],
          authors: fixtureData.authors || [],
          affiliations: fixtureData.affiliations || [],
          metadata: fixtureData.meta || {},
          source_format: fixtureData.source_format,
          document_type: fixtureData.document_type
        };

        // Try to load pre-generated review file based on depth
        let issuesData = null;
        let personaSummaries = null;

        // Get review config from session storage (contains depth setting)
        const reviewConfigStr = sessionStorage.getItem('reviewConfig');
        if (reviewConfigStr) {
          try {
            const reviewConfig = JSON.parse(reviewConfigStr);
            const depthKey = reviewConfig.depth || 'medium'; // Default to medium (Full Review)

            // Map depth keys from ReviewSetupScreen to file naming convention
            const depthMap = {
              'light': 'firstpass',
              'medium': 'fullreview',
              'heavy': 'deepanalysis'
            };
            const depth = depthMap[depthKey] || 'fullreview';

            // Build review file path: {document}_{tier}.json
            const fixtureBase = demoFile.replace('.json', '');
            const reviewPath = `/reviews/${fixtureBase}_${depth}.json`;

            console.log('Attempting to load review file:', reviewPath);
            const reviewRes = await fetch(reviewPath);

            if (reviewRes.ok) {
              const reviewData = await reviewRes.json();
              console.log('Review file loaded successfully:', reviewData.review_id);

              // Extract issues and persona summaries from review data
              issuesData = reviewData.issues || [];
              personaSummaries = reviewData.persona_summaries || null;

              // Store persona summaries in session storage for potential use
              if (personaSummaries) {
                sessionStorage.setItem('personaSummaries', JSON.stringify(personaSummaries));
              }
            } else {
              console.log('Review file not found, will use generated issues');
            }
          } catch (err) {
            console.warn('Could not load review file:', err);
          }
        }

        // Fall back to fixture issues or empty array if no review file
        if (!issuesData) {
          issuesData = fixtureData.issues || [];
          console.warn('No review file found and no issues in fixture');
        }

        // Backend will provide real bias analysis
        const mockBiasProfile = {
          document_id: fixtureData.manuscript_id || fixtureData.document_id,
          biases: []  // Backend will provide real bias analysis
        };

        setDocument(documentData);
        setIssues(issuesData);
        setBiasProfile(mockBiasProfile);

        // Set first figure as active by default
        if (documentData.figures?.length > 0) {
          setActiveFigureId(documentData.figures[0].figure_id);
        }
      } else {
        // Fallback: Load default static files
        console.log('No demo selected, loading fallback static files');
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
