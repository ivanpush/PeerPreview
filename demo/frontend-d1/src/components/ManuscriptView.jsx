import React, { useEffect, useRef, useState } from 'react';
import { useManuscript } from '../context/ManuscriptContext';

function ManuscriptView({ onFigureClick }) {
  const { manuscript, selectedIssue, updateParagraph } = useManuscript();
  const paragraphRefs = useRef({});
  const sectionRefs = useRef({});
  const [activeSection, setActiveSection] = useState(null);
  const [editingParagraph, setEditingParagraph] = useState(null);
  const [editText, setEditText] = useState('');
  const [showOriginal, setShowOriginal] = useState(null);

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

  // Track active section based on scroll position (75% threshold)
  useEffect(() => {
    const handleScroll = () => {
      const scrollContainer = document.querySelector('.manuscript-scroll-container');
      if (!scrollContainer) return;

      const scrollTop = scrollContainer.scrollTop;
      const containerHeight = scrollContainer.clientHeight;
      const threshold = scrollTop + (containerHeight * 0.25); // 75% from top = 25% from bottom

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
    const isEditing = editingParagraph === paragraphId;
    const isShowingOriginal = showOriginal === paragraphId;

    const handleEdit = () => {
      setEditingParagraph(paragraphId);
      setEditText(paragraph.text);
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
        updateParagraph(paragraphId, paragraph.originalText, false);
      }
      setShowOriginal(null);
    };

    return (
      <div
        key={paragraphId}
        id={paragraphId}
        ref={el => paragraphRefs.current[paragraphId] = el}
        className={`group mb-4 p-4 rounded-lg border transition-all duration-300 relative ${
          isHighlighted
            ? 'bg-[#1E1E1E] border-blue-500/60 shadow-lg shadow-blue-500/10'
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
          {!isEditing && (
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

        {/* Editing mode */}
        {isEditing ? (
          <div className="space-y-2">
            <textarea
              value={editText}
              onChange={(e) => setEditText(e.target.value)}
              className="w-full text-[15px] text-gray-200 leading-[1.7] bg-[#1A1A1A] border border-blue-500/50 rounded p-3 resize-none focus:outline-none focus:ring-2 focus:ring-blue-500 min-h-[100px]"
              rows={5}
            />
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
          </div>
        ) : isShowingOriginal && paragraph.originalText ? (
          /* Show original text with revert option */
          <div className="space-y-3">
            <div className="p-3 bg-[#2A2A2A] rounded border border-gray-700">
              <p className="text-[13px] text-gray-400 mb-2 font-semibold">Original:</p>
              <p className="text-[15px] text-gray-300 leading-[1.7]">
                {paragraph.originalText}
              </p>
            </div>
            <div className="p-3 bg-[#1E1E1E] rounded border border-gray-700">
              <p className="text-[13px] text-gray-400 mb-2 font-semibold">Current:</p>
              <p className={`text-[15px] leading-[1.7] ${
                isRewritten ? 'text-green-300' : isEdited ? 'text-yellow-300' : 'text-gray-200'
              }`}>
                {paragraph.text}
              </p>
            </div>
            <button
              onClick={handleRevert}
              className="px-3 py-1.5 text-xs bg-red-600 text-white rounded hover:bg-red-700 transition"
            >
              Revert to Original
            </button>
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
      {/* Active section indicator - fixed on left */}
      {activeSection && (
        <div className="fixed left-4 top-20 z-10">
          <div className="bg-[#2A2A2A] border border-[#3A3A3A] rounded px-3 py-1.5 shadow-lg">
            <span className="text-[11px] text-gray-300 font-semibold tracking-wide">
              {getFullSectionName(activeSection)}
            </span>
          </div>
        </div>
      )}

      <div className="max-w-4xl mx-auto p-8">
        {/* Title */}
        <h1 className="text-2xl font-semibold text-white mb-6 leading-tight tracking-tight">
          {manuscript.title}
        </h1>

        {/* Abstract */}
        {manuscript.abstract && (
          <div className="mb-8 p-6 bg-[#232323] rounded-lg border border-[#2E2E2E]">
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
