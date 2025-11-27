import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

function ReviewSetupScreen() {
  const navigate = useNavigate();

  // Document metadata from selection/upload
  const [documentInfo, setDocumentInfo] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  // Review mode toggle
  const [reviewMode, setReviewMode] = useState('static'); // 'static' or 'dynamic'

  // Review configuration
  const [depth, setDepth] = useState('medium');
  const [userPrompt, setUserPrompt] = useState('');
  const [documentType, setDocumentType] = useState('');
  const [detectedType, setDetectedType] = useState('');

  // Cost estimates
  const depthCosts = {
    light: { min: 0.30, max: 0.50, description: 'Clarity focus, basic checks' },
    medium: { min: 0.80, max: 1.50, description: 'All tracks, balanced' },
    heavy: { min: 2.00, max: 4.00, description: 'Deep analysis, hostile review' }
  };

  // Document type options
  const documentTypes = [
    { value: 'academic_manuscript', label: 'Academic Manuscript' },
    { value: 'grant_proposal', label: 'Grant Proposal' },
    { value: 'policy_brief', label: 'Policy Brief' },
    { value: 'legal_brief', label: 'Legal Brief' },
    { value: 'memo', label: 'Memo' },
    { value: 'technical_report', label: 'Technical Report' },
    { value: 'generic', label: 'Generic Document' }
  ];

  // Prompt chips
  const promptChips = [
    'Desk-reject level review',
    'Focus on methods rigor',
    'Check statistical claims',
    'Clarity and flow only',
    'Hostile reviewer perspective',
    'Grant competitiveness',
    'Policy feasibility'
  ];

  useEffect(() => {
    // Load document info from previous screen
    const selectedDemo = sessionStorage.getItem('selectedDemo');
    const demoFile = sessionStorage.getItem('demoFile');

    if (selectedDemo && demoFile) {
      // Load the demo fixture to get metadata
      fetch(`/fixtures/${demoFile}`)
        .then(res => res.json())
        .then(data => {
          setDocumentInfo({
            title: data.title,
            source_format: data.source_format,
            page_count: data.meta.page_count,
            word_count: data.meta.word_count,
            document_type: data.document_type,
            fixture_file: demoFile,
            selectedDemo: selectedDemo
          });
          setDetectedType(data.document_type);
          setDocumentType(data.document_type);
          setIsLoading(false);
        })
        .catch(err => {
          console.error('Failed to load fixture:', err);
          setIsLoading(false);
        });
    } else {
      // Handle uploaded file (V1 feature)
      setDocumentInfo({
        title: 'Uploaded Document',
        source_format: 'pdf',
        page_count: 12,
        word_count: 4500,
        document_type: 'academic_manuscript',
        selectedDemo: null
      });
      setDetectedType('academic_manuscript');
      setDocumentType('academic_manuscript');
      setIsLoading(false);
    }
  }, []);

  const handleChipClick = (chip) => {
    if (userPrompt) {
      setUserPrompt(userPrompt + '\n' + chip);
    } else {
      setUserPrompt(chip);
    }
  };

  const handleStartReview = () => {
    // Store review configuration
    const reviewConfig = {
      depth,
      userPrompt,
      documentType,
      documentInfo,
      estimatedCost: depthCosts[depth],
      reviewMode // Include the mode
    };

    sessionStorage.setItem('reviewConfig', JSON.stringify(reviewConfig));

    // Navigate to appropriate screen based on mode
    if (reviewMode === 'static') {
      // Go directly to ReviewScreen with static data
      navigate('/review');
    } else {
      // Go to ProcessScreen which will call backend
      navigate('/process');
    }
  };

  const canProceed = documentInfo && depth;

  // Check if static demo data is available for this document
  const hasStaticDemo = documentInfo?.selectedDemo === 'manuscript_pdf';

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading document...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-6">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Review Setup</h1>
          <p className="text-gray-600">Configure your document review preferences</p>
        </div>

        {/* Document Info Card */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Document Information</h2>
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div>
              <span className="text-gray-500">Title:</span>
              <p className="font-medium text-gray-900 mt-1 line-clamp-2">{documentInfo?.title}</p>
            </div>
            <div>
              <span className="text-gray-500">Format:</span>
              <p className="font-medium text-gray-900 mt-1">{documentInfo?.source_format?.toUpperCase()}</p>
            </div>
            <div>
              <span className="text-gray-500">Pages:</span>
              <p className="font-medium text-gray-900 mt-1">{documentInfo?.page_count}</p>
            </div>
            <div>
              <span className="text-gray-500">Words:</span>
              <p className="font-medium text-gray-900 mt-1">~{documentInfo?.word_count?.toLocaleString()}</p>
            </div>
          </div>

          {/* Document Type Override */}
          <div className="mt-4 pt-4 border-t border-gray-100">
            <label className="text-sm text-gray-500 block mb-2">
              Detected: <span className="font-medium text-gray-900">{documentTypes.find(t => t.value === detectedType)?.label}</span>
            </label>
            <select
              value={documentType}
              onChange={(e) => setDocumentType(e.target.value)}
              className="w-full md:w-auto px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              {documentTypes.map(type => (
                <option key={type.value} value={type.value}>{type.label}</option>
              ))}
            </select>
          </div>
        </div>

        {/* Review Mode Toggle - Only show if static demo is available */}
        {hasStaticDemo && (
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Review Mode</h2>
            <div className="grid grid-cols-2 gap-4">
              <label
                className={`
                  relative rounded-lg border-2 p-4 cursor-pointer transition-all
                  ${reviewMode === 'static'
                    ? 'border-green-500 bg-green-50'
                    : 'border-gray-200 hover:border-gray-300 bg-white'
                  }
                `}
              >
                <input
                  type="radio"
                  name="mode"
                  value="static"
                  checked={reviewMode === 'static'}
                  onChange={(e) => setReviewMode(e.target.value)}
                  className="sr-only"
                />
                <div className="flex flex-col">
                  <span className="text-lg font-semibold text-gray-900">Static Demo</span>
                  <span className="text-sm text-gray-600 mt-1">Instant preview with pre-populated review</span>
                  <span className="text-sm font-medium text-green-600 mt-2">
                    ✓ Immediate results
                  </span>
                </div>
                {reviewMode === 'static' && (
                  <div className="absolute top-2 right-2">
                    <div className="w-6 h-6 bg-green-500 rounded-full flex items-center justify-center">
                      <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                      </svg>
                    </div>
                  </div>
                )}
              </label>

              <label
                className={`
                  relative rounded-lg border-2 p-4 cursor-pointer transition-all
                  ${reviewMode === 'dynamic'
                    ? 'border-blue-500 bg-blue-50'
                    : 'border-gray-200 hover:border-gray-300 bg-white'
                  }
                `}
              >
                <input
                  type="radio"
                  name="mode"
                  value="dynamic"
                  checked={reviewMode === 'dynamic'}
                  onChange={(e) => setReviewMode(e.target.value)}
                  className="sr-only"
                />
                <div className="flex flex-col">
                  <span className="text-lg font-semibold text-gray-900">Dynamic Review</span>
                  <span className="text-sm text-gray-600 mt-1">Full AI agent analysis</span>
                  <span className="text-sm font-medium text-blue-600 mt-2">
                    ~ 30-60 seconds
                  </span>
                </div>
                {reviewMode === 'dynamic' && (
                  <div className="absolute top-2 right-2">
                    <div className="w-6 h-6 bg-blue-500 rounded-full flex items-center justify-center">
                      <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                      </svg>
                    </div>
                  </div>
                )}
              </label>
            </div>

            {reviewMode === 'static' && (
              <div className="mt-4 p-3 bg-amber-50 border border-amber-200 rounded-lg">
                <div className="flex items-start gap-2">
                  <span className="text-amber-600 text-sm">ℹ️</span>
                  <p className="text-sm text-amber-800">
                    Static mode uses pre-computed review data for instant demonstration. Review options below are for display only.
                  </p>
                </div>
              </div>
            )}
          </div>
        )}

        {/* Review Depth Selection */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Review Depth</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {Object.entries(depthCosts).map(([key, config]) => (
              <label
                key={key}
                className={`
                  relative rounded-lg border-2 p-4 cursor-pointer transition-all
                  ${depth === key
                    ? 'border-blue-500 bg-blue-50'
                    : 'border-gray-200 hover:border-gray-300 bg-white'
                  }
                `}
              >
                <input
                  type="radio"
                  name="depth"
                  value={key}
                  checked={depth === key}
                  onChange={(e) => setDepth(e.target.value)}
                  className="sr-only"
                />
                <div className="flex flex-col">
                  <span className="text-lg font-semibold capitalize text-gray-900">{key}</span>
                  <span className="text-sm text-gray-600 mt-1">{config.description}</span>
                  <span className="text-lg font-medium text-blue-600 mt-2">
                    ${config.min.toFixed(2)} - ${config.max.toFixed(2)}
                  </span>
                </div>
                {depth === key && (
                  <div className="absolute top-2 right-2">
                    <div className="w-6 h-6 bg-blue-500 rounded-full flex items-center justify-center">
                      <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                      </svg>
                    </div>
                  </div>
                )}
              </label>
            ))}
          </div>
        </div>

        {/* Review Focus */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Review Focus (Optional)</h2>

          {/* Prompt Chips */}
          <div className="flex flex-wrap gap-2 mb-4">
            {promptChips.map(chip => (
              <button
                key={chip}
                onClick={() => handleChipClick(chip)}
                className="px-3 py-1.5 text-sm bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-full transition"
              >
                {chip}
              </button>
            ))}
          </div>

          {/* Custom Instructions */}
          <textarea
            value={userPrompt}
            onChange={(e) => setUserPrompt(e.target.value)}
            placeholder="Additional instructions for the review..."
            className="w-full h-24 px-4 py-3 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
          />
        </div>

        {/* Cost Summary & Actions */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center justify-between">
            <div>
              {reviewMode === 'static' ? (
                <>
                  <p className="text-sm text-gray-600">Demo mode:</p>
                  <p className="text-2xl font-bold text-green-600">Free Preview</p>
                </>
              ) : (
                <>
                  <p className="text-sm text-gray-600">Estimated cost:</p>
                  <p className="text-2xl font-bold text-gray-900">
                    ${depthCosts[depth].min.toFixed(2)} - ${depthCosts[depth].max.toFixed(2)}
                  </p>
                </>
              )}
            </div>
            <div className="flex gap-3">
              <button
                onClick={() => navigate('/')}
                className="px-6 py-3 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition font-medium"
              >
                Back
              </button>
              <button
                onClick={handleStartReview}
                disabled={!canProceed}
                className={`
                  px-8 py-3 rounded-lg font-medium transition shadow-md hover:shadow-lg
                  ${canProceed
                    ? reviewMode === 'static'
                      ? 'bg-green-600 hover:bg-green-700 text-white'
                      : 'bg-blue-600 hover:bg-blue-700 text-white'
                    : 'bg-gray-300 text-gray-500 cursor-not-allowed'
                  }
                `}
              >
                {reviewMode === 'static' ? 'View Demo Review →' : 'Start AI Review →'}
              </button>
            </div>
          </div>
        </div>

        {/* Warning for large documents */}
        {documentInfo?.page_count > 40 && (
          <div className="mt-4 p-4 bg-amber-50 border border-amber-200 rounded-lg">
            <div className="flex items-start gap-2">
              <span className="text-amber-600">⚠️</span>
              <div className="text-sm">
                <p className="font-medium text-amber-900">Large document detected</p>
                <p className="text-amber-800">
                  Documents over 40 pages may have limited review depth options or require section selection.
                </p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default ReviewSetupScreen;