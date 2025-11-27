import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';

function ReviewSetupScreen() {
  const navigate = useNavigate();

  // Document metadata from selection/upload
  const [documentInfo, setDocumentInfo] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  // Review mode toggle
  const [reviewMode, setReviewMode] = useState('static'); // 'static' or 'dynamic'

  // Review configuration
  const [depth, setDepth] = useState(1); // 0 = light, 1 = medium, 2 = heavy (using indices for slider)
  const [userPrompt, setUserPrompt] = useState('');
  const [selectedChips, setSelectedChips] = useState([]);
  const [documentType, setDocumentType] = useState('');
  const [detectedType, setDetectedType] = useState('');
  const [showTypeMenu, setShowTypeMenu] = useState(false);
  const [chipsAnimating, setChipsAnimating] = useState(false);
  const typeMenuRef = useRef(null);

  // Depth configurations
  const depthSettings = [
    { key: 'light', label: 'Light', description: 'Clarity + basic checks' },
    { key: 'medium', label: 'Medium', description: 'Balanced, all tracks' },
    { key: 'heavy', label: 'Heavy', description: 'Deep reasoning + hostile review' }
  ];

  // Document type options with colors
  const documentTypes = [
    { value: 'academic_manuscript', label: 'Academic Manuscript', color: '#10B981' },
    { value: 'grant_proposal', label: 'Grant Proposal', color: '#14B8A6' },
    { value: 'policy_brief', label: 'Policy Brief', color: '#F59E0B' },
    { value: 'legal_brief', label: 'Legal Brief', color: '#6366F1' },
    { value: 'memo', label: 'Memo', color: '#F43F5E' },
    { value: 'technical_report', label: 'Technical Report', color: '#06B6D4' },
    { value: 'generic', label: 'Generic Document', color: '#6B7280' }
  ];

  // Dynamic chips per document type
  const chipsByType = {
    academic_manuscript: [
      'Desk-reject risks',
      'Methods rigor',
      'Statistical validity',
      'Clarity & flow',
      'Novelty & framing',
      'Hostile reviewer POV'
    ],
    grant_proposal: [
      'Significance & impact',
      'Innovation claims',
      'Approach & methods',
      'Feasibility & timeline',
      'Investigator fit',
      'Study section simulation'
    ],
    policy_brief: [
      'Evidence quality',
      'Stakeholder objections',
      'Implementation feasibility',
      'Political framing',
      'Executive summary strength',
      'Counterarguments'
    ],
    legal_brief: [
      'Precedent strength',
      'Factual record support',
      'Procedural vulnerabilities',
      'Persuasive force',
      'Opposing counsel POV',
      'Jurisdictional issues'
    ],
    generic: [
      'Internal consistency',
      'Clarity & structure',
      'Claim strength',
      'Audience fit',
      'Overclaims & gaps'
    ],
    memo: [
      'Internal consistency',
      'Clarity & structure',
      'Claim strength',
      'Audience fit',
      'Overclaims & gaps'
    ],
    technical_report: [
      'Internal consistency',
      'Clarity & structure',
      'Claim strength',
      'Audience fit',
      'Overclaims & gaps'
    ]
  };

  // Get current chips based on document type
  const promptChips = chipsByType[documentType] || chipsByType.generic;

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

  // Handle click outside to close menu
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (typeMenuRef.current && !typeMenuRef.current.contains(event.target)) {
        setShowTypeMenu(false);
      }
    };

    if (showTypeMenu) {
      document.addEventListener('mousedown', handleClickOutside);
      return () => document.removeEventListener('mousedown', handleClickOutside);
    }
  }, [showTypeMenu]);

  // Reset selected chips and animate when document type changes
  useEffect(() => {
    setChipsAnimating(true);
    setSelectedChips([]);
    const timer = setTimeout(() => setChipsAnimating(false), 300);
    return () => clearTimeout(timer);
  }, [documentType]);

  const handleChipClick = (chip) => {
    if (selectedChips.includes(chip)) {
      setSelectedChips(selectedChips.filter(c => c !== chip));
    } else {
      setSelectedChips([...selectedChips, chip]);
    }
  };

  const handleStartReview = () => {
    // Combine selected chips with any custom text
    const combinedPrompt = [...selectedChips, userPrompt].filter(Boolean).join('\n');

    // Store review configuration
    const reviewConfig = {
      depth: depthSettings[depth].key,
      userPrompt: combinedPrompt,
      documentType,
      documentInfo,
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

  const canProceed = documentInfo && depth !== undefined;

  // Check if static demo data is available for this document
  // For now, enable toggle for all demos (we only have static data for manuscript_pdf)
  const hasStaticDemo = true; // Always show toggle for demo purposes

  if (isLoading) {
    return (
      <div className="min-h-screen bg-[#0B0C0E] flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-[#3C82F6] mx-auto mb-4"></div>
          <p className="text-[#A1A5AC]">Loading document...</p>
        </div>
      </div>
    );
  }

  // Updated depth configurations with clear value props
  const depthConfigs = [
    {
      key: 'light',
      label: 'Quick Scan',
      time: '~5 min',
      description: 'Surface issues • Grammar • Clarity',
      benefits: ['Basic readability check', 'Obvious errors', 'Quick turnaround'],
      textColor: '#10b981', // emerald-400
      bgColor: '#10b981'
    },
    {
      key: 'medium',
      label: 'Standard Review',
      time: '~15 min',
      description: 'All major issues • Balanced analysis',
      benefits: ['Logic & flow', 'Citation check', 'Best for most docs'],
      textColor: '#3C82F6', // blue
      bgColor: '#3C82F6'
    },
    {
      key: 'heavy',
      label: 'Deep Analysis',
      time: '~30 min',
      description: 'Hostile review • Edge cases • Full rigor',
      benefits: ['Methodological rigor', 'Hidden flaws', 'Pre-submission check'],
      textColor: '#a855f7', // purple-400
      bgColor: '#a855f7'
    }
  ];

  return (
    <div className="min-h-screen bg-[#0B0C0E] text-[#E8E9EB]">
      <div className="max-w-3xl mx-auto px-8 py-12">
        {/* Document title and stats - at the very top */}
        <div className="mb-8">
          <div className="text-xs text-[#6A6D73] mb-4">
            <div className="mb-1 truncate max-w-md" title={documentInfo?.title}>
              {documentInfo?.title}
            </div>
            <div>{documentInfo?.source_format?.toUpperCase()} • {documentInfo?.page_count} pages • ~{documentInfo?.word_count?.toLocaleString()} words</div>
          </div>
        </div>

        {/* Focus/Chat Area */}
        <div className="mb-10">
          <div className="relative mb-6">
            <p className="text-lg text-[#E8E9EB]">
              This looks like {documentTypes.find(t => t.value === documentType)?.label?.match(/^[aeiou]/i) ? 'an' : 'a'}{' '}
              <span
                className="inline-flex items-center gap-1.5 px-2 py-0.5 rounded-md font-medium"
                style={{
                  color: documentTypes.find(t => t.value === documentType)?.color,
                  backgroundColor: `${documentTypes.find(t => t.value === documentType)?.color}20`,
                  borderColor: `${documentTypes.find(t => t.value === documentType)?.color}40`,
                  borderWidth: '1px'
                }}
              >
                {documentTypes.find(t => t.value === documentType)?.label}
              </span>
              <sup className="relative" ref={typeMenuRef}>
                <button
                  onClick={() => setShowTypeMenu(!showTypeMenu)}
                  className="text-[10px] text-[#6A6D73] hover:text-[#A1A5AC] transition-colors ml-0.5"
                >
                  [change]
                </button>

                {/* Dropdown menu */}
                {showTypeMenu && (
                  <div className="absolute top-4 left-0 z-50 bg-[#1A1C1F] border border-[#2E2E2E] rounded-lg shadow-xl py-2 min-w-[200px]">
                    {documentTypes.map(type => (
                      <button
                        key={type.value}
                        onClick={() => {
                          setDocumentType(type.value);
                          setShowTypeMenu(false);
                        }}
                        className={`
                          w-full text-left px-4 py-2 text-sm transition-colors
                          ${documentType === type.value
                            ? 'bg-[#3C82F6] bg-opacity-20 text-[#3C82F6]'
                            : 'text-[#A1A5AC] hover:bg-[#2E2E2E] hover:text-[#E8E9EB]'
                          }
                        `}
                      >
                        {type.label}
                        {type.value === detectedType && type.value !== documentType && (
                          <span className="text-xs text-[#6A6D73] ml-2">(detected)</span>
                        )}
                      </button>
                    ))}
                  </div>
                )}
              </sup>
              . Should the review focus on anything in particular?
            </p>
          </div>

          {/* Custom instructions - optional, subtle */}
          <textarea
            value={userPrompt}
            onChange={(e) => setUserPrompt(e.target.value)}
            placeholder="Any other specific areas to examine..."
            className="w-full h-24 px-4 py-3 bg-[#1A1C1F] border border-[#2E2E2E] rounded-2xl text-sm text-[#E8E9EB] placeholder-[#6A6D73] focus:outline-none focus:border-[#3C82F6] transition-colors resize-none mb-4"
          />

          {/* Pills - moved below textarea */}
          <div className={`flex flex-wrap gap-2 transition-opacity duration-300 ${chipsAnimating ? 'opacity-0' : 'opacity-100'}`}>
            {promptChips.map(chip => {
              const currentTypeColor = documentTypes.find(t => t.value === documentType)?.color || '#6B7280';
              const isSelected = selectedChips.includes(chip);

              return (
                <button
                  key={chip}
                  onClick={() => handleChipClick(chip)}
                  className="px-3 py-1.5 text-sm rounded-full transition-all duration-200"
                  style={{
                    color: isSelected ? currentTypeColor : '#A1A5AC',
                    backgroundColor: isSelected ? `${currentTypeColor}30` : 'transparent',
                    borderColor: isSelected ? currentTypeColor : `${currentTypeColor}20`,
                    borderWidth: '1px'
                  }}
                  onMouseEnter={(e) => {
                    if (!isSelected) {
                      e.currentTarget.style.borderColor = currentTypeColor;
                      e.currentTarget.style.color = '#E8E9EB';
                    }
                  }}
                  onMouseLeave={(e) => {
                    if (!isSelected) {
                      e.currentTarget.style.borderColor = `${currentTypeColor}20`;
                      e.currentTarget.style.color = '#A1A5AC';
                    }
                  }}
                >
                  {chip}
                </button>
              );
            })}
          </div>
        </div>

        {/* Thin separator */}
        <div className="border-t border-[#1A1C1F] mb-10"></div>

        {/* Depth Selector - SEGMENTED BLOCKS */}
        <div className="mb-10">
          <h2 className="text-sm font-medium text-[#A1A5AC] mb-6">How thorough should the review be?</h2>

          {/* Segmented control blocks */}
          <div className="grid grid-cols-3 gap-3 mb-6">
            {depthConfigs.map((config, index) => (
              <button
                key={config.key}
                onClick={() => setDepth(index)}
                className="relative p-4 rounded-lg border transition-all duration-200"
                style={{
                  borderColor: depth === index ? config.bgColor : '#2E2E2E',
                  backgroundColor: depth === index ? `${config.bgColor}15` : 'transparent'
                }}
                onMouseEnter={(e) => {
                  if (depth !== index) {
                    e.currentTarget.style.borderColor = '#3C82F6';
                    e.currentTarget.style.backgroundColor = '#1A1C1F';
                  }
                }}
                onMouseLeave={(e) => {
                  if (depth !== index) {
                    e.currentTarget.style.borderColor = '#2E2E2E';
                    e.currentTarget.style.backgroundColor = 'transparent';
                  }
                }}
              >
                {/* Selected indicator */}
                {depth === index && (
                  <div
                    className="absolute top-2 right-2 w-2 h-2 rounded-full"
                    style={{ backgroundColor: config.bgColor }}
                  ></div>
                )}

                <div className="text-left">
                  <div
                    className="font-medium text-sm mb-1"
                    style={{ color: depth === index ? config.textColor : '#E8E9EB' }}
                  >
                    {config.label}
                  </div>
                  <div className="text-xs text-[#6A6D73] mb-2">{config.time}</div>
                  <div className="text-xs text-[#A1A5AC] leading-relaxed">
                    {config.description}
                  </div>
                </div>
              </button>
            ))}
          </div>

          {/* Detailed benefits for selected depth */}
          <div className="bg-[#1A1C1F] rounded-lg p-4">
            <div className="flex items-start gap-3">
              <div
                className="w-1 h-16 rounded-full"
                style={{ backgroundColor: depthConfigs[depth].bgColor }}
              ></div>
              <div>
                <p className="text-sm font-medium text-[#E8E9EB] mb-2">
                  {depthConfigs[depth].label} includes:
                </p>
                <ul className="space-y-1">
                  {depthConfigs[depth].benefits.map((benefit, i) => (
                    <li key={i} className="text-xs text-[#A1A5AC] flex items-center gap-2">
                      <span className="text-[#6A6D73]">•</span>
                      {benefit}
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        </div>

        {/* Thin separator */}
        <div className="border-t border-[#1A1C1F] mb-10"></div>

        {/* Review Mode Toggle - minimal, only for demo */}
        {hasStaticDemo && (
          <div className="mb-10">
            <div className="flex items-center gap-6">
              <label className="flex items-center cursor-pointer">
                <input
                  type="radio"
                  name="mode"
                  value="static"
                  checked={reviewMode === 'static'}
                  onChange={(e) => setReviewMode(e.target.value)}
                  className="sr-only"
                />
                <div className={`w-4 h-4 rounded-full border-2 mr-2 transition-colors ${reviewMode === 'static' ? 'border-[#3C82F6] bg-[#3C82F6]' : 'border-[#6A6D73]'}`}>
                  {reviewMode === 'static' && <div className="w-2 h-2 bg-[#0B0C0E] rounded-full m-0.5"></div>}
                </div>
                <span className={`text-sm ${reviewMode === 'static' ? 'text-[#E8E9EB]' : 'text-[#6A6D73]'}`}>
                  Static Demo <span className="text-xs text-[#4ADE80]">• Instant</span>
                </span>
              </label>

              <label className="flex items-center cursor-pointer">
                <input
                  type="radio"
                  name="mode"
                  value="dynamic"
                  checked={reviewMode === 'dynamic'}
                  onChange={(e) => setReviewMode(e.target.value)}
                  className="sr-only"
                />
                <div className={`w-4 h-4 rounded-full border-2 mr-2 transition-colors ${reviewMode === 'dynamic' ? 'border-[#3C82F6] bg-[#3C82F6]' : 'border-[#6A6D73]'}`}>
                  {reviewMode === 'dynamic' && <div className="w-2 h-2 bg-[#0B0C0E] rounded-full m-0.5"></div>}
                </div>
                <span className={`text-sm ${reviewMode === 'dynamic' ? 'text-[#E8E9EB]' : 'text-[#6A6D73]'}`}>
                  Dynamic <span className="text-xs text-[#3C82F6]">• ~30s</span>
                </span>
              </label>
            </div>

            {reviewMode === 'static' && (
              <p className="text-xs text-[#6A6D73] mt-3">
                Using pre-computed review data for instant demonstration
              </p>
            )}
          </div>
        )}

        {/* Actions - right-aligned, minimal */}
        <div className="flex justify-end gap-3 mb-10">
          <button
            onClick={() => navigate('/')}
            className="px-4 py-2 text-sm text-[#A1A5AC] hover:text-[#E8E9EB] transition-colors"
          >
            Back
          </button>
          <button
            onClick={handleStartReview}
            disabled={!canProceed}
            className={`
              px-6 py-2 rounded text-sm font-medium transition-all duration-200
              ${canProceed
                ? 'bg-[#3C82F6] text-white hover:bg-opacity-90 shadow-lg hover:shadow-xl'
                : 'bg-[#1A1C1F] text-[#6A6D73] cursor-not-allowed'
              }
            `}
          >
            Start Review →
          </button>
        </div>


        {/* Warning for large documents - subtle */}
        {documentInfo?.page_count > 40 && (
          <div className="mt-6 p-3 bg-[#FEF3C7] bg-opacity-10 border border-[#FEF3C7] border-opacity-20 rounded-lg">
            <p className="text-xs text-[#FEF3C7]">
              Large document detected • Some review options may be limited
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

export default ReviewSetupScreen;