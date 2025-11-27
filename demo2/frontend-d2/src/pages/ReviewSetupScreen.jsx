import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import ConsensusToggle from '../components/ConsensusToggle';

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
  const [consensusReview, setConsensusReview] = useState(false);
  const typeMenuRef = useRef(null);

  // Depth configurations
  const depthSettings = [
    { key: 'light', label: 'First Pass', description: 'Core logic, structure, major issues.' },
    { key: 'medium', label: 'Full Review', description: 'Full-section critique with balanced depth.' },
    { key: 'heavy', label: 'Deep Analysis', description: 'Adversarial expert review of claims, methods, and reasoning.' }
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

  // Dynamic chips per document type (severity-first)
  const chipsByType = {
    academic_manuscript: [
      'Desk-reject risks',
      'Methods rigor',
      'Statistical validity',
      'Novelty & framing',
      'Clarity & flow'
    ],
    grant_proposal: [
      'Study section simulation',
      'Significance & impact',
      'Innovation claims',
      'Approach & methods',
      'Feasibility & timeline'
    ],
    policy_brief: [
      'Counterarguments',
      'Evidence quality',
      'Stakeholder objections',
      'Implementation feasibility',
      'Executive summary strength'
    ],
    legal_brief: [
      'Opposing counsel POV',
      'Precedent strength',
      'Factual record support',
      'Procedural vulnerabilities',
      'Persuasive force'
    ],
    memo: [
      'Action clarity',
      'Decision support',
      'Audience targeting',
      'Brevity check',
      'Tone appropriateness'
    ],
    technical_report: [
      'Conclusions vs evidence',
      'Methods reproducibility',
      'Technical accuracy',
      'Data presentation',
      'Clarity for non-specialists'
    ],
    generic: [
      'Overclaims & gaps',
      'Internal consistency',
      'Claim strength',
      'Clarity & structure',
      'Audience fit'
    ]
  };

  // Dynamic placeholder text per document type
  const placeholderByType = {
    academic_manuscript: 'e.g., "Targeting Nature Methods" or "Stats need scrutiny" or "Be harsh on discussion"',
    grant_proposal: 'e.g., "R01 resubmission" or "Aims 2-3 are weak" or "Reviewers hated the timeline last time"',
    policy_brief: 'e.g., "For skeptical legislators" or "Implementation section is rushed" or "Need stronger evidence"',
    legal_brief: 'e.g., "Opposition will attack standing" or "Weak on Smith v. Jones distinction" or "Judge is textualist"',
    memo: 'e.g., "For C-suite" or "Too long" or "Action items are buried"',
    technical_report: 'e.g., "External audience" or "Methods section is thin" or "Conclusions overreach"',
    generic: 'e.g., "Be harsh" or "Check logical flow" or "Audience is non-technical"'
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

  // Reset selected chips when document type changes
  useEffect(() => {
    setSelectedChips([]);
  }, [documentType]);

  // Reset consensus review when depth changes from Deep Analysis
  useEffect(() => {
    if (depth !== 2) {
      setConsensusReview(false);
    }
  }, [depth]);

  // Handle textarea auto-resize on mount and value changes
  useEffect(() => {
    const textarea = document.querySelector('textarea');
    if (textarea) {
      if (userPrompt) {
        textarea.style.height = 'auto';
        textarea.style.height = Math.min(textarea.scrollHeight, 200) + 'px';
      } else {
        textarea.style.height = '72px';
      }
    }
  }, [userPrompt]);


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
      reviewMode, // Include the mode
      consensusReview: depth === 2 && consensusReview // Only for Deep Analysis
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
      label: 'First Pass',
      description: 'Core logic, structure, major issues.',
      textColor: '#10b981', // emerald-400
      bgColor: '#10b981'
    },
    {
      key: 'medium',
      label: 'Full Review',
      description: 'Full-section critique with balanced depth.',
      textColor: '#3C82F6', // blue
      bgColor: '#3C82F6'
    },
    {
      key: 'heavy',
      label: 'Deep Analysis',
      description: 'Adversarial expert review of claims, methods, and reasoning.',
      textColor: '#a855f7', // purple-400
      bgColor: '#a855f7'
    }
  ];

  return (
    <div className="min-h-screen bg-[#0B0C0E] text-[#E8E9EB]">
      <div className="max-w-3xl mx-auto px-8 py-12">
        {/* Document title and stats - at the very top */}
        <div className="mb-4">
          <div className="text-xs text-[#6A6D73] mb-2">
            <div className="mb-1 truncate max-w-md" title={documentInfo?.title}>
              {documentInfo?.title}
            </div>
            <div>{documentInfo?.source_format?.toUpperCase()} • {documentInfo?.page_count} pages • ~{documentInfo?.word_count?.toLocaleString()} words</div>
          </div>

          {/* Document type detection - kept close to stats */}
          <p className="text-sm text-[#A1A5AC]">
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
                className="text-[10px] text-[#5BAEB8] hover:text-[#1C6D79] transition-colors ml-0.5"
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
          </p>
        </div>

        {/* Thin separator */}
        <div className="border-t border-[#1A1C1F] mb-8"></div>

        {/* Focus/Chat Area - moved towards center */}
        <div className="mb-10 mt-24">
          <div className="mb-4 text-center">
            <p className="text-lg font-medium text-[#E8E9EB]">What matters most for this review?</p>
          </div>

          {/* Custom instructions - now the visual focus */}
          <textarea
            value={userPrompt}
            onChange={(e) => {
              setUserPrompt(e.target.value);
              // Auto-resize textarea
              e.target.style.height = 'auto';
              e.target.style.height = Math.min(e.target.scrollHeight, 200) + 'px';
            }}
            onFocus={(e) => {
              // Expand on focus if there's content
              if (e.target.value) {
                e.target.style.height = 'auto';
                e.target.style.height = Math.min(e.target.scrollHeight, 200) + 'px';
              }
            }}
            placeholder={placeholderByType[documentType] || placeholderByType.generic}
            className="w-full min-h-[72px] max-h-[200px] px-5 py-3 bg-[#1A1C1F] border-2 border-[#2E2E2E] rounded-2xl text-base text-[#E8E9EB] placeholder:text-[#6A6D73] focus:outline-none focus:border-[#3C82F6] focus:bg-[#0F1012] transition-all duration-200 ease-out resize-none mb-4 overflow-y-auto"
            style={{ height: userPrompt ? 'auto' : '72px' }}
          />

          {/* Pills - moved below textarea */}
          <div className="flex flex-wrap gap-2">
            {promptChips.map(chip => {
              const currentTypeColor = documentTypes.find(t => t.value === documentType)?.color || '#6B7280';
              const isSelected = selectedChips.includes(chip);

              return (
                <button
                  key={chip}
                  onClick={() => handleChipClick(chip)}
                  className="px-3 py-1.5 text-sm rounded-full"
                  style={{
                    color: isSelected ? currentTypeColor : '#A1A5AC',
                    backgroundColor: isSelected ? `${currentTypeColor}30` : 'transparent',
                    borderColor: isSelected ? currentTypeColor : `${currentTypeColor}20`,
                    borderWidth: '1px',
                    transition: 'all 0.2s ease-out'
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
          <h2 className="text-lg font-medium text-[#E8E9EB] mb-6 text-center">How thorough should the review be?</h2>

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
                    className="font-medium text-sm mb-2"
                    style={{ color: depth === index ? config.textColor : '#E8E9EB' }}
                  >
                    {config.label}
                  </div>
                  <div className="text-xs text-[#A1A5AC] leading-relaxed">
                    {config.description}
                  </div>
                </div>
              </button>
            ))}
          </div>

          {/* Consensus Mode - appears below Deep Analysis when selected */}
          {depth === 2 && (
            <div className="mt-3 grid grid-cols-3 gap-3">
              <div className="col-start-3">
                <div className="pl-6 flex flex-col gap-2">
                  <div className="flex items-start gap-2">
                    <span className="text-xs text-[#6A6D73] mt-0.5">↳</span>
                    <div className="flex flex-col gap-1">
                      <ConsensusToggle
                        checked={consensusReview}
                        onChange={setConsensusReview}
                      />
                      <p className="text-[10px] text-[#6A6D73] leading-relaxed max-w-[160px]">
                        Three top models cross-check and reconcile disagreements
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Thin separator */}
        <div className="border-t border-[#1A1C1F] mb-10"></div>

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
                ? 'bg-[#5BAEB8] text-white hover:bg-[#1C6D79] shadow-lg hover:shadow-xl'
                : 'bg-[#1A1C1F] text-[#6A6D73] cursor-not-allowed'
              }
            `}
          >
            Run Review →
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

        {/* Review Mode Toggle - V0 only, hidden at bottom */}
        {hasStaticDemo && (
          <div className="mt-16 pt-8 border-t border-[#1A1C1F]/30">
            <div className="flex items-center gap-6 justify-center opacity-40 hover:opacity-60 transition-opacity">
              <label className="flex items-center cursor-pointer">
                <input
                  type="radio"
                  name="mode"
                  value="static"
                  checked={reviewMode === 'static'}
                  onChange={(e) => setReviewMode(e.target.value)}
                  className="sr-only"
                />
                <div className={`w-3 h-3 rounded-full border mr-2 transition-colors ${reviewMode === 'static' ? 'border-[#6A6D73] bg-[#6A6D73]' : 'border-[#3A3A3A]'}`}>
                  {reviewMode === 'static' && <div className="w-1.5 h-1.5 bg-[#0B0C0E] rounded-full m-0.5"></div>}
                </div>
                <span className={`text-xs ${reviewMode === 'static' ? 'text-[#A1A5AC]' : 'text-[#4A4A4A]'}`}>
                  Static Demo
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
                <div className={`w-3 h-3 rounded-full border mr-2 transition-colors ${reviewMode === 'dynamic' ? 'border-[#6A6D73] bg-[#6A6D73]' : 'border-[#3A3A3A]'}`}>
                  {reviewMode === 'dynamic' && <div className="w-1.5 h-1.5 bg-[#0B0C0E] rounded-full m-0.5"></div>}
                </div>
                <span className={`text-xs ${reviewMode === 'dynamic' ? 'text-[#A1A5AC]' : 'text-[#4A4A4A]'}`}>
                  Dynamic
                </span>
              </label>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default ReviewSetupScreen;