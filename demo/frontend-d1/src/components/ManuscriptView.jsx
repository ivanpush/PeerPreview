import React, { useEffect, useRef, useState } from 'react';
import { useManuscript } from '../context/ManuscriptContext';
import * as Diff from 'diff';

function ManuscriptView({ onFigureClick }) {
  const { manuscript, selectedIssue, updateParagraph, restoreDeleted } = useManuscript();
  const paragraphRefs = useRef({});
  const sectionRefs = useRef({});
  const [activeSection, setActiveSection] = useState(null);
  const [editingParagraph, setEditingParagraph] = useState(null);
  const [editText, setEditText] = useState('');
  const [showOriginal, setShowOriginal] = useState(null);
  const [collapsedDeleted, setCollapsedDeleted] = useState(new Set());
  const [authorsExpanded, setAuthorsExpanded] = useState(false);
  const [expandedMetaSections, setExpandedMetaSections] = useState(new Set());

  // Extract paragraph number from paragraph_id (e.g., "p_res_5" -> "5")
  const getParagraphNumber = (paragraphId) => {
    const match = paragraphId.match(/_(\d+)$/);
    return match ? match[1] : paragraphId.split('_').pop();
  };

  // Extract full section name from paragraph_id or section_id
  const getFullSectionName = (id) => {
    // Map abbreviated section names to full words
    const sectionMap = {
      'abs': 'ABSTRACT',
      'int': 'INTRO',
      'intro': 'INTRO',
      'res': 'RESULTS',
      'results': 'RESULTS',
      'disc': 'DISCUSSION',
      'discussion': 'DISCUSSION',
      'met': 'METHODS',
      'methods': 'METHODS',
      'conc': 'CONCLUSION',
      'conclusion': 'CONCLUSION',
      'ack': 'ACKNOWLEDGEMENTS',
      'ref': 'REFERENCES',
      'front': 'FRONT'
    };

    const parts = id.split('_');
    if (parts.length >= 2) {
      const sectionPart = parts[1].toLowerCase();
      return sectionMap[sectionPart] || sectionPart.toUpperCase();
    }
    return id.toUpperCase();
  };

  // Track active section based on scroll position (80% threshold), only show for actual sections (skip abstract)
  useEffect(() => {
    const handleScroll = () => {
      const scrollContainer = document.querySelector('.manuscript-scroll-container');
      if (!scrollContainer) return;

      const scrollTop = scrollContainer.scrollTop;
      const containerHeight = scrollContainer.clientHeight;
      const threshold = scrollTop + (containerHeight * 0.2); // 80% from top = 20% from bottom

      // Find the first real section (introduction or first body section)
      const firstSection = Object.entries(sectionRefs.current).find(([sectionId]) => {
        return sectionId.includes('int') || sectionId.includes('res') || sectionId.includes('met') || sectionId.includes('disc');
      });

      // Only show section indicator after scrolling to the first real section
      if (firstSection) {
        const [, firstElement] = firstSection;
        if (firstElement) {
          const rect = firstElement.getBoundingClientRect();
          const containerRect = scrollContainer.getBoundingClientRect();
          const firstElementTop = rect.top - containerRect.top + scrollTop;

          // Don't show until we reach the first real section
          if (scrollTop < firstElementTop - 100) {
            setActiveSection(null);
            return;
          }
        }
      }

      let currentSection = null;

      Object.entries(sectionRefs.current).forEach(([sectionId, element]) => {
        if (element) {
          const rect = element.getBoundingClientRect();
          const containerRect = scrollContainer.getBoundingClientRect();
          const elementTop = rect.top - containerRect.top + scrollTop;

          if (elementTop <= threshold) {
            currentSection = sectionId;
          }
        }
      });

      setActiveSection(currentSection);
    };

    const scrollContainer = document.querySelector('.manuscript-scroll-container');
    if (scrollContainer) {
      scrollContainer.addEventListener('scroll', handleScroll);
      handleScroll(); // Initial check
      return () => scrollContainer.removeEventListener('scroll', handleScroll);
    }
  }, [manuscript]);

  useEffect(() => {
    // Scroll to paragraph when issue is selected
    if (selectedIssue?.paragraph_id) {
      const element = paragraphRefs.current[selectedIssue.paragraph_id];
      if (element) {
        element.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
    } else if (selectedIssue?.section_id && !selectedIssue.paragraph_id) {
      // Scroll to section if no specific paragraph
      const section = document.getElementById(selectedIssue.section_id);
      if (section) {
        section.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    }
  }, [selectedIssue]);

  if (!manuscript) {
    return (
      <div className="h-full flex items-center justify-center bg-gray-900">
        <p className="text-gray-400">Loading manuscript...</p>
      </div>
    );
  }

  const renderParagraph = (paragraphId) => {
    const paragraph = manuscript.paragraphs?.find(p => p.paragraph_id === paragraphId);
    if (!paragraph) return null;

    const isHighlighted = selectedIssue?.paragraph_id === paragraphId;
    const isRewritten = paragraph.isRewritten === true;
    const isEdited = paragraph.isEdited === true;
    const isDeleted = paragraph.isDeleted === true;
    const isEditing = editingParagraph === paragraphId;
    const isShowingOriginal = showOriginal === paragraphId;

    const handleEdit = () => {
      setEditingParagraph(paragraphId);
      setEditText(paragraph.text);
    };

    // Calculate textarea rows based on text length
    const calculateRows = (text) => {
      const lines = text.split('\n').length;
      const estimatedWrappedLines = Math.ceil(text.length / 80); // Estimate ~80 chars per line
      return Math.max(lines, estimatedWrappedLines, 5); // Minimum 5 rows
    };

    const handleSaveEdit = () => {
      if (editText.trim() && editText !== paragraph.text) {
        updateParagraph(paragraphId, editText, false);
      }
      setEditingParagraph(null);
    };

    const handleCancelEdit = () => {
      setEditingParagraph(null);
      setEditText('');
    };

    const handleRevert = () => {
      if (paragraph.originalText) {
        updateParagraph(paragraphId, paragraph.originalText, false, true); // Pass isRevert=true
      }
      setShowOriginal(null);
    };

    const handleDelete = () => {
      updateParagraph(paragraphId, '', false, false, true); // Pass isDelete=true
    };

    const handleRestoreDeleted = () => {
      restoreDeleted(paragraphId);
    };

    const toggleDeletedCollapse = () => {
      setCollapsedDeleted(prev => {
        const newSet = new Set(prev);
        if (newSet.has(paragraphId)) {
          newSet.delete(paragraphId);
        } else {
          newSet.add(paragraphId);
        }
        return newSet;
      });
    };

    const isCollapsed = collapsedDeleted.has(paragraphId);

    return (
      <div
        key={paragraphId}
        id={paragraphId}
        ref={el => paragraphRefs.current[paragraphId] = el}
        className={`group mb-4 p-4 rounded-lg border transition-all duration-300 relative ${
          isHighlighted
            ? 'bg-[#1E1E1E] border-blue-500/60 shadow-lg shadow-blue-500/10'
            : isDeleted
            ? 'bg-transparent border-red-900/30 hover:border-red-800/40'
            : isRewritten
            ? 'bg-[#1A2B1A] border-green-900/50 hover:bg-[#1E331E] hover:border-green-800/50'
            : isEdited
            ? 'bg-[#2A1E1E] border-yellow-900/50 hover:bg-[#331E1E] hover:border-yellow-800/50'
            : 'bg-transparent border-[#2E2E2E] hover:bg-[#1E1E1E]/50 hover:border-[#3A3A3A]'
        }`}
      >
        {/* Top right controls - Edit button only */}
        <div className="absolute top-2 right-2 flex items-center gap-2">
          {/* Edit button - show on hover */}
          {!isEditing && !isDeleted && (
            <button
              onClick={handleEdit}
              className="opacity-0 group-hover:opacity-100 transition-opacity text-[10px] text-gray-500 hover:text-blue-400 px-2 py-1 rounded bg-[#2A2A2A] hover:bg-[#333333] border border-[#3A3A3A] hover:border-blue-800/50"
              title="Edit paragraph"
            >
              Edit
            </button>
          )}
        </div>

        {/* Paragraph number - inside block, bottom right, only on hover */}
        <div className="absolute bottom-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity">
          <span className="text-[10px] text-gray-600 font-mono">
            {getParagraphNumber(paragraphId)}
          </span>
        </div>

        {/* Deleted state - strikethrough with badge, collapsible */}
        {isDeleted ? (
          <>
            {!isCollapsed && (
              <p className="text-[15px] leading-[1.7] font-normal text-gray-400 opacity-50 line-through mb-3">
                {paragraph.text}
              </p>
            )}
            <div className="flex items-center gap-2">
              <button
                onClick={toggleDeletedCollapse}
                className="inline-flex items-center gap-1 text-gray-500 hover:text-gray-400 transition"
                title={isCollapsed ? "Expand deleted text" : "Collapse deleted text"}
              >
                <svg
                  className={`w-3 h-3 transition-transform ${isCollapsed ? 'rotate-0' : 'rotate-90'}`}
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
              </button>
              <button
                onClick={handleRestoreDeleted}
                className="inline-flex items-center gap-1.5 text-[9px] font-semibold px-2 py-1 rounded border bg-red-900/30 text-red-400 border-red-800/50 hover:bg-red-900/50 transition cursor-pointer"
                title="Click to restore"
              >
                <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
                DELETED
              </button>
            </div>
          </>
        ) : isEditing ? (
          /* Editing mode */
          <div className="space-y-2">
            <textarea
              value={editText}
              onChange={(e) => setEditText(e.target.value)}
              className="w-full text-[15px] text-gray-200 leading-[1.7] bg-[#1A1A1A] border border-blue-500/50 rounded p-3 resize-y focus:outline-none focus:ring-2 focus:ring-blue-500 min-h-[100px]"
              rows={calculateRows(editText)}
            />
            <div className="flex items-center justify-between gap-2">
              <div className="flex items-center gap-2">
                <button
                  onClick={handleSaveEdit}
                  className="px-3 py-1.5 text-xs bg-blue-600 text-white rounded hover:bg-blue-700 transition"
                >
                  Save
                </button>
                <button
                  onClick={handleCancelEdit}
                  className="px-3 py-1.5 text-xs bg-gray-700 text-gray-300 rounded hover:bg-gray-600 transition"
                >
                  Cancel
                </button>
              </div>
              <button
                onClick={handleDelete}
                className="px-3 py-1.5 text-xs bg-red-600 text-white rounded hover:bg-red-700 transition"
                title="Delete this paragraph"
              >
                Delete
              </button>
            </div>
          </div>
        ) : isShowingOriginal && paragraph.originalText ? (
          /* Show diff view with word-level highlighting */
          <div className="space-y-3">
            <div className="p-3 bg-[#1A1A1A] rounded border border-gray-700">
              <p className="text-[11px] text-gray-500 mb-3 font-semibold uppercase tracking-wider">
                Changes (red = removed, green = added)
              </p>
              <div className="text-[15px] leading-[1.7] font-normal">
                {Diff.diffWords(paragraph.originalText, paragraph.text).map((part, index) => (
                  <span
                    key={index}
                    className={
                      part.added
                        ? 'bg-green-900/40 text-green-300'
                        : part.removed
                        ? 'bg-red-900/40 text-red-300 line-through'
                        : 'text-gray-300'
                    }
                  >
                    {part.value}
                  </span>
                ))}
              </div>
            </div>
            <div className="flex items-center gap-2">
              <button
                onClick={handleRevert}
                className="px-3 py-1.5 text-xs bg-red-600 text-white rounded hover:bg-red-700 transition"
              >
                Revert to Original
              </button>
              <button
                onClick={handleEdit}
                className="px-3 py-1.5 text-xs bg-blue-600 text-white rounded hover:bg-blue-700 transition"
              >
                Edit Current
              </button>
              <button
                onClick={() => setShowOriginal(null)}
                className="px-3 py-1.5 text-xs bg-gray-700 text-gray-300 rounded hover:bg-gray-600 transition"
              >
                Close Diff
              </button>
            </div>
          </div>
        ) : (
          /* Normal display */
          <>
            <p className={`text-[15px] leading-[1.7] font-normal ${
              isRewritten ? 'text-green-300' : isEdited ? 'text-yellow-300' : 'text-gray-200'
            }`}>
              {paragraph.text}
            </p>

            {/* Status badge - below text */}
            {(isRewritten || isEdited) && (
              <div className="mt-3 flex items-center">
                <button
                  onClick={() => setShowOriginal(isShowingOriginal ? null : paragraphId)}
                  className={`inline-flex items-center gap-1.5 text-[9px] font-semibold px-2 py-1 rounded border transition cursor-pointer ${
                    isRewritten
                      ? 'text-green-400 bg-green-900/30 border-green-800/50 hover:bg-green-900/50'
                      : 'text-yellow-400 bg-yellow-900/30 border-yellow-800/50 hover:bg-yellow-900/50'
                  }`}
                  title="Click to view original"
                >
                  <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                  </svg>
                  {isRewritten ? 'REWRITTEN' : 'EDITED'}
                </button>
              </div>
            )}
          </>
        )}

        {/* Metadata indicators */}
        {(paragraph.metadata?.citations?.length > 0 || paragraph.metadata?.fig_refs?.length > 0) && (
          <div className="mt-3 flex gap-2 flex-wrap">
            {paragraph.metadata.citations?.length > 0 && (
              <span className="text-xs bg-blue-950/40 text-blue-400 px-2 py-1 rounded border border-blue-900/50">
                {paragraph.metadata.citations.length} citations
              </span>
            )}
            {paragraph.metadata.fig_refs?.length > 0 && (
              <div className="flex items-center gap-1.5">
                <span className="text-xs text-gray-500">Figs:</span>
                {paragraph.metadata.fig_refs.map(figRef => {
                  // Find the corresponding figure
                  const figure = manuscript?.figures?.find(f =>
                    f.label?.includes(figRef) || f.figure_id?.includes(figRef)
                  );

                  return figure ? (
                    <button
                      key={figRef}
                      onClick={(e) => {
                        e.stopPropagation();
                        onFigureClick(figure.figure_id);
                      }}
                      className="text-xs bg-purple-950/40 text-purple-400 px-2 py-1 rounded border border-purple-900/50 hover:bg-purple-900/40 hover:border-purple-800/50 transition cursor-pointer"
                    >
                      {figRef}
                    </button>
                  ) : (
                    <span key={figRef} className="text-xs bg-purple-950/40 text-purple-400 px-2 py-1 rounded border border-purple-900/50">
                      {figRef}
                    </span>
                  );
                })}
              </div>
            )}
          </div>
        )}
      </div>
    );
  };

  return (
    <div className="h-full overflow-y-auto bg-[#1D1D1D] manuscript-scroll-container relative">
      {/* Active section indicator - fixed left side, semi-transparent */}
      {activeSection && activeSection !== 'front' && (
        <div className="fixed left-8 top-20 z-50">
          <div className="bg-[#2A2A2A]/80 backdrop-blur-sm border border-[#3A3A3A]/60 rounded px-4 py-2 shadow-lg">
            <span className="text-[13px] text-gray-300 font-semibold tracking-wide">
              {getFullSectionName(activeSection)}
            </span>
          </div>
        </div>
      )}

      <div className="max-w-4xl mx-auto p-8">
        {/* Title */}
        <h1 className="text-xl font-semibold text-white mb-3 leading-tight tracking-tight">
          {manuscript.title}
        </h1>

        {/* Section Pills - Canonical + Other Sections */}
        <div className="flex items-center flex-wrap gap-2 mb-8">
          {/* Canonical sections (required) */}
          {['abstract', 'introduction', 'methods', 'results', 'discussion', 'references'].map((required) => {
            const hasSection = required === 'abstract'
              ? manuscript.abstract
              : manuscript.sections?.some(
                  s => s.section_id?.includes(required) ||
                       s.section_title?.toLowerCase().includes(required) ||
                       s.heading?.toLowerCase().includes(required) ||
                       (required === 'methods' && (
                         s.section_id?.includes('materials') ||
                         s.section_title?.toLowerCase().includes('materials') ||
                         s.section_title?.toLowerCase().includes('experimental')
                       ))
                );

            return (
              <span
                key={required}
                className={`px-2 py-1 rounded text-xs font-medium flex items-center gap-1 ${
                  hasSection
                    ? 'bg-blue-500/20 text-blue-400 border border-blue-500/40'
                    : 'bg-red-500/20 text-red-400 border border-red-500/40'
                }`}
              >
                {hasSection ? (
                  <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                ) : (
                  <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                )}
                {required}
              </span>
            );
          })}

          {/* Other sections present but not canonical (gray) */}
          {manuscript.sections
            ?.filter(s => {
              const sectionName = (s.section_id || s.section_title || s.heading || '').toLowerCase();
              const isCanonical = ['abstract', 'introduction', 'methods', 'results', 'discussion', 'references',
                                   'materials', 'experimental', 'bibliography', 'intro', 'int', 'res', 'disc', 'met', 'ref'].some(
                canonical => sectionName.includes(canonical)
              );
              return !isCanonical && s.paragraph_ids && s.paragraph_ids.length > 0;
            })
            .map((section) => (
              <span
                key={section.section_id}
                className="px-2 py-1 bg-gray-700/30 text-gray-400 border border-gray-600/40 rounded text-xs font-medium"
              >
                {section.section_title || section.heading}
              </span>
            ))}
        </div>

        {/* Authors Section - Collapsible */}
        {(manuscript.authors || manuscript.affiliations) && (
          <div className="mb-6">
            <button
              onClick={() => setAuthorsExpanded(!authorsExpanded)}
              className="flex items-center gap-2 text-sm text-gray-400 hover:text-gray-300 transition"
            >
              <svg
                className={`w-4 h-4 transition-transform ${authorsExpanded ? 'rotate-90' : 'rotate-0'}`}
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
              <span className="font-semibold">Authors & Affiliations</span>
            </button>

            {authorsExpanded && (
              <div className="mt-3 p-4 bg-[#232323] rounded-lg border border-[#2E2E2E]">
                {manuscript.authors && (
                  <div className="mb-3">
                    <h3 className="text-xs font-semibold text-gray-400 mb-2 uppercase tracking-wide">Authors</h3>
                    <p className="text-sm text-gray-300 leading-relaxed whitespace-pre-line">
                      {manuscript.authors}
                    </p>
                  </div>
                )}
                {manuscript.affiliations && (
                  <div>
                    <h3 className="text-xs font-semibold text-gray-400 mb-2 uppercase tracking-wide">Affiliations</h3>
                    <p className="text-sm text-gray-300 leading-relaxed whitespace-pre-line">
                      {manuscript.affiliations}
                    </p>
                  </div>
                )}
              </div>
            )}
          </div>
        )}

        {/* Abstract */}
        {manuscript.abstract && (
          <div className="abstract-section mb-8 p-6 bg-[#232323] rounded-lg border border-[#2E2E2E]">
            <h2 className="text-[15px] font-semibold text-gray-300 mb-3 tracking-wide">ABSTRACT</h2>
            <p className="text-[15px] text-gray-200 leading-[1.7]">
              {manuscript.abstract}
            </p>
          </div>
        )}

        {/* Sections - reconstruct from section.paragraph_ids */}
        {manuscript.sections?.map(section => {
          // Skip sections with no paragraphs
          if (!section.paragraph_ids || section.paragraph_ids.length === 0) return null;

          // Identify meta sections (acknowledgements, funding, etc.)
          const sectionName = (section.section_title || section.heading || '').toLowerCase();
          const isMetaSection = ['acknowledgement', 'funding', 'conflict', 'contribution', 'author contribution',
                                  'data availability', 'code availability', 'supplementary'].some(
            meta => sectionName.includes(meta)
          );

          // Regular section rendering
          if (!isMetaSection) {
            return (
              <div
                key={section.section_id}
                ref={el => sectionRefs.current[section.section_id] = el}
                className="mb-10 relative"
              >
                <h2
                  id={section.section_id}
                  className="text-[17px] font-semibold text-gray-200 mb-5 pb-2 border-b border-[#2E2E2E] tracking-wide"
                >
                  {section.section_title || section.heading}
                </h2>
                <div className="space-y-2">
                  {section.paragraph_ids.map(pid => renderParagraph(pid))}
                </div>
              </div>
            );
          }

          // Meta section - collapsible
          const isExpanded = expandedMetaSections.has(section.section_id);
          const toggleMetaSection = () => {
            setExpandedMetaSections(prev => {
              const newSet = new Set(prev);
              if (newSet.has(section.section_id)) {
                newSet.delete(section.section_id);
              } else {
                newSet.add(section.section_id);
              }
              return newSet;
            });
          };

          return (
            <div
              key={section.section_id}
              ref={el => sectionRefs.current[section.section_id] = el}
              className="mb-6 relative"
            >
              <button
                onClick={toggleMetaSection}
                className="flex items-center gap-2 text-sm text-gray-400 hover:text-gray-300 transition mb-3"
              >
                <svg
                  className={`w-4 h-4 transition-transform ${isExpanded ? 'rotate-90' : 'rotate-0'}`}
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
                <span className="font-semibold">{section.section_title || section.heading}</span>
              </button>

              {isExpanded && (
                <div className="pl-6 space-y-2">
                  {section.paragraph_ids.map(pid => renderParagraph(pid))}
                </div>
              )}
            </div>
          );
        })}

        {/* References (optional) */}
        {manuscript.references && (
          <div className="mt-12 pt-8 border-t border-[#2E2E2E]">
            <h2 className="text-[17px] font-semibold text-gray-200 mb-4 tracking-wide">REFERENCES</h2>
            <div className="text-sm text-gray-400 whitespace-pre-wrap leading-relaxed">
              {manuscript.references}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default ManuscriptView;
