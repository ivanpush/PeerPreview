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
      <div className="h-full flex items-center justify-center">
        <p className="text-gray-500">Loading manuscript...</p>
      </div>
    );
  }

  const renderParagraph = (paragraphId) => {
    const paragraph = manuscript.paragraphs.find(p => p.paragraph_id === paragraphId);
    if (!paragraph) return null;

    const isHighlighted = selectedIssue?.paragraph_id === paragraphId;

    return (
      <div
        key={paragraphId}
        ref={el => paragraphRefs.current[paragraphId] = el}
        className={`mb-4 p-3 rounded transition-all duration-300 ${
          isHighlighted ? 'bg-yellow-100 border-l-4 border-yellow-500 shadow' : ''
        }`}
      >
        <p className="text-gray-800 leading-relaxed text-justify">
          {paragraph.text}
        </p>

        {/* Metadata indicators */}
        {(paragraph.metadata?.citations?.length > 0 || paragraph.metadata?.fig_refs?.length > 0) && (
          <div className="mt-2 flex gap-2 flex-wrap">
            {paragraph.metadata.citations?.length > 0 && (
              <span className="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded">
                {paragraph.metadata.citations.length} citations
              </span>
            )}
            {paragraph.metadata.fig_refs?.length > 0 && (
              <span className="text-xs bg-purple-100 text-purple-700 px-2 py-1 rounded">
                Refs: {paragraph.metadata.fig_refs.join(', ')}
              </span>
            )}
          </div>
        )}
      </div>
    );
  };

  return (
    <div className="h-full overflow-y-auto p-8 bg-white">
      {/* Title */}
      <h1 className="text-4xl font-bold text-gray-900 mb-6">
        {manuscript.title}
      </h1>

      {/* Abstract */}
      {manuscript.abstract && (
        <div className="mb-8 p-6 bg-gray-50 rounded-lg border border-gray-200">
          <h2 className="text-xl font-semibold text-gray-800 mb-3">Abstract</h2>
          <p className="text-gray-700 leading-relaxed text-justify">
            {manuscript.abstract}
          </p>
        </div>
      )}

      {/* Sections */}
      {manuscript.sections?.map(section => (
        <div key={section.section_id} className="mb-10">
          <h2
            id={section.section_id}
            className="text-2xl font-semibold text-gray-800 mb-4 pb-2 border-b-2 border-gray-300"
          >
            {section.heading}
          </h2>
          <div className="space-y-2">
            {section.paragraphs?.map(renderParagraph)}
          </div>
        </div>
      ))}

      {/* References (optional) */}
      {manuscript.references && (
        <div className="mt-12 pt-8 border-t-2 border-gray-300">
          <h2 className="text-2xl font-semibold text-gray-800 mb-4">References</h2>
          <div className="text-sm text-gray-600 whitespace-pre-wrap leading-relaxed">
            {manuscript.references}
          </div>
        </div>
      )}
    </div>
  );
}

export default ManuscriptView;
