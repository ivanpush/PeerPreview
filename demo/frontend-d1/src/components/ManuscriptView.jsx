import React, { useEffect, useRef } from 'react';
import { useManuscript } from '../context/ManuscriptContext';

function ManuscriptView() {
  const { manuscript, selectedIssue } = useManuscript();
  const paragraphRefs = useRef({});

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

    return (
      <div
        key={paragraphId}
        id={paragraphId}
        ref={el => paragraphRefs.current[paragraphId] = el}
        className={`mb-4 p-4 rounded-lg border transition-all duration-300 ${
          isHighlighted
            ? 'bg-[#1E1E1E] border-blue-500/60 shadow-lg shadow-blue-500/10'
            : 'bg-transparent border-[#2E2E2E] hover:bg-[#1E1E1E]/50 hover:border-[#3A3A3A]'
        }`}
      >
        <p className="text-[15px] text-gray-200 leading-[1.7] font-normal">
          {paragraph.text}
        </p>

        {/* Metadata indicators */}
        {(paragraph.metadata?.citations?.length > 0 || paragraph.metadata?.fig_refs?.length > 0) && (
          <div className="mt-3 flex gap-2 flex-wrap">
            {paragraph.metadata.citations?.length > 0 && (
              <span className="text-xs bg-blue-950/40 text-blue-400 px-2 py-1 rounded border border-blue-900/50">
                {paragraph.metadata.citations.length} citations
              </span>
            )}
            {paragraph.metadata.fig_refs?.length > 0 && (
              <span className="text-xs bg-purple-950/40 text-purple-400 px-2 py-1 rounded border border-purple-900/50">
                Figs: {paragraph.metadata.fig_refs.join(', ')}
              </span>
            )}
          </div>
        )}
      </div>
    );
  };

  return (
    <div className="h-full overflow-y-auto bg-[#1D1D1D]">
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
            <div key={section.section_id} className="mb-10">
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
