import React, { createContext, useContext, useState, useCallback } from 'react';

const DocumentContext = createContext();

// Helper function to generate mock issues based on document type
const generateMockIssues = (fixtureData) => {
  const issues = [];

  // Get first few paragraphs for realistic issue locations
  const firstPara = fixtureData.paragraphs?.[0]?.paragraph_id || 'p_1';
  const secondPara = fixtureData.paragraphs?.[1]?.paragraph_id || 'p_2';
  const firstSection = fixtureData.sections?.[0]?.section_id || 'introduction';
  const secondSection = fixtureData.sections?.[1]?.section_id || 'methods';

  // Generate a variety of issues based on document type
  if (fixtureData.document_type === 'academic_manuscript') {
    issues.push(
      {
        id: 'issue_001',
        track: 'A',
        persona: 'Methods Reviewer',
        severity: 'major',
        code: 'MISSING_STAT_DETAILS',
        title: 'Missing statistical details',
        message: 'Statistical test details missing. Need to specify multiple comparisons correction method.',
        paragraph_id: secondPara,
        section_id: secondSection,
        rationale: 'Statistical test details missing. Need to specify multiple comparisons correction method.',
        suggestion: 'Add details about Bonferroni or FDR correction used for multiple comparisons.',
        proposed_rewrite: null
      },
      {
        id: 'issue_002',
        track: 'B',
        persona: 'Clarity Reviewer',
        severity: 'moderate',
        code: 'UNCLEAR_TRANSITION',
        title: 'Unclear transition',
        message: 'Abrupt transition between background and hypothesis. Reader needs clearer connection.',
        paragraph_id: firstPara,
        section_id: firstSection,
        rationale: 'Abrupt transition between background and hypothesis. Reader needs clearer connection.',
        suggestion: 'Add a bridging sentence explaining how the background leads to your hypothesis.',
        proposed_rewrite: 'Given these limitations in current approaches, we hypothesized that...'
      },
      {
        id: 'issue_003',
        track: 'C',
        persona: 'Domain Expert',
        severity: 'major',
        code: 'ALTERNATIVE_EXPLANATION',
        title: 'Alternative explanation not addressed',
        message: 'The observed effect could be explained by confounding factors not addressed in the experimental design.',
        paragraph_id: secondPara,
        section_id: secondSection,
        rationale: 'The observed effect could be explained by confounding factors not addressed in the experimental design.',
        suggestion: 'Discuss alternative explanations and how your controls rule them out.',
        proposed_rewrite: null
      }
    );
  } else if (fixtureData.document_type === 'grant_proposal') {
    issues.push(
      {
        id: 'issue_001',
        track: 'A',
        persona: 'Study Section Member',
        severity: 'major',
        code: 'IMPACT_UNCLEAR',
        title: 'Impact not clearly articulated',
        message: 'Impact on field not clearly articulated. How will this change clinical practice?',
        paragraph_id: firstPara,
        section_id: firstSection,
        rationale: 'Impact on field not clearly articulated. How will this change clinical practice?',
        suggestion: 'Explicitly state how findings will translate to patient care improvements.',
        proposed_rewrite: null
      },
      {
        id: 'issue_002',
        track: 'B',
        persona: 'Innovation Reviewer',
        severity: 'moderate',
        code: 'INCREMENTAL_ADVANCE',
        title: 'Appears incremental',
        message: 'The proposed approach appears incremental rather than innovative.',
        paragraph_id: secondPara,
        section_id: secondSection,
        rationale: 'The proposed approach appears incremental rather than innovative.',
        suggestion: 'Emphasize what makes your approach novel compared to existing methods.',
        proposed_rewrite: null
      },
      {
        id: 'issue_003',
        track: 'C',
        persona: 'Budget Reviewer',
        severity: 'major',
        code: 'TIMELINE_UNREALISTIC',
        title: 'Unrealistic timeline',
        message: 'Timeline appears overly ambitious given the scope of proposed experiments.',
        paragraph_id: firstPara,
        section_id: firstSection,
        rationale: 'Timeline appears overly ambitious given the scope of proposed experiments.',
        suggestion: 'Consider extending timeline or reducing scope for Aims 2 and 3.',
        proposed_rewrite: null
      }
    );
  } else if (fixtureData.document_type === 'policy_brief') {
    issues.push(
      {
        id: 'issue_001',
        track: 'A',
        persona: 'Policy Analyst',
        severity: 'moderate',
        code: 'EVIDENCE_CHERRY_PICKED',
        title: 'Selective evidence',
        message: 'Evidence appears selectively chosen. Missing studies with contradictory findings.',
        paragraph_id: firstPara,
        section_id: firstSection,
        rationale: 'Evidence appears selectively chosen. Missing studies with contradictory findings.',
        suggestion: 'Include and address contradictory evidence to strengthen credibility.',
        proposed_rewrite: null
      },
      {
        id: 'issue_002',
        track: 'C',
        persona: 'Stakeholder Advocate',
        severity: 'major',
        code: 'IMPLEMENTATION_COSTS',
        title: 'Implementation costs not addressed',
        message: 'Implementation costs not adequately addressed. Budget-conscious legislators will object.',
        paragraph_id: secondPara,
        section_id: secondSection,
        rationale: 'Implementation costs not adequately addressed. Budget-conscious legislators will object.',
        suggestion: 'Add cost-benefit analysis showing long-term savings.',
        proposed_rewrite: null
      }
    );
  } else if (fixtureData.document_type === 'legal_brief') {
    issues.push(
      {
        id: 'issue_001',
        track: 'A',
        persona: 'Opposing Counsel',
        severity: 'major',
        code: 'DISTINGUISHABLE_PRECEDENT',
        title: 'Precedent is distinguishable',
        message: 'Cited precedent is distinguishable on material facts.',
        paragraph_id: firstPara,
        section_id: firstSection,
        rationale: 'Cited precedent is distinguishable on material facts.',
        suggestion: 'Address the factual distinctions or find more analogous precedent.',
        proposed_rewrite: null
      },
      {
        id: 'issue_002',
        track: 'B',
        persona: 'Senior Partner',
        severity: 'moderate',
        code: 'WEAK_OPENING',
        title: 'Weak opening argument',
        message: 'Opening argument buries the lede. Judge will lose interest.',
        paragraph_id: firstPara,
        section_id: firstSection,
        rationale: 'Opening argument buries the lede. Judge will lose interest.',
        suggestion: 'Lead with your strongest argument and most favorable facts.',
        proposed_rewrite: null
      }
    );
  } else {
    // Generic document type
    issues.push(
      {
        id: 'issue_001',
        track: 'B',
        persona: 'Editor',
        severity: 'moderate',
        code: 'UNCLEAR_PURPOSE',
        title: 'Purpose unclear',
        message: 'Document purpose not clear from opening. Reader may be confused about intent.',
        paragraph_id: firstPara,
        section_id: firstSection,
        rationale: 'Document purpose not clear from opening. Reader may be confused about intent.',
        suggestion: 'State the document\'s purpose clearly in the first paragraph.',
        proposed_rewrite: null
      }
    );
  }

  // Add some generic issues that work for any document
  issues.push(
    {
      id: `issue_${issues.length + 1}`,
      track: 'A',
      persona: 'Consistency Checker',
      severity: 'minor',
      code: 'INCONSISTENT_TERMINOLOGY',
      title: 'Inconsistent terminology',
      message: 'Inconsistent use of terminology throughout document.',
      paragraph_id: firstPara,
      section_id: firstSection,
      rationale: 'Inconsistent use of terminology throughout document.',
      suggestion: 'Use consistent terminology throughout the document.',
      proposed_rewrite: null
    }
  );

  return issues;
};

// Helper function to generate mock bias profile
const generateMockBiases = (documentType) => {
  const biases = [];

  if (documentType === 'academic_manuscript') {
    biases.push(
      {
        bias_type: 'statistical_rigor',
        severity: 'high',
        description: 'Tendency to overlook multiple comparisons issues'
      },
      {
        bias_type: 'clarity',
        severity: 'medium',
        description: 'May miss unclear transitions between sections'
      }
    );
  } else if (documentType === 'grant_proposal') {
    biases.push(
      {
        bias_type: 'novelty_bias',
        severity: 'high',
        description: 'May overvalue novelty at expense of feasibility'
      }
    );
  }

  // Add generic biases
  biases.push(
    {
      bias_type: 'confirmation_bias',
      severity: 'low',
      description: 'General tendency to favor expected outcomes'
    }
  );

  return biases;
};

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

        // Generate mock bias profile based on document type
        const mockBiasProfile = {
          document_id: fixtureData.manuscript_id || fixtureData.document_id,
          biases: generateMockBiases(fixtureData.document_type)
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

        // Fall back to fixture issues or generate mock ones if no review file
        if (!issuesData) {
          issuesData = fixtureData.issues || generateMockIssues(fixtureData);
        }

        // Generate mock bias profile
        const mockBiasProfile = {
          document_id: fixtureData.manuscript_id || fixtureData.document_id,
          biases: generateMockBiases(fixtureData.document_type)
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
