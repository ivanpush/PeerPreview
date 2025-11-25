import React from 'react';
import { useManuscript } from '../context/ManuscriptContext';

function RewriteModal({ issue, onClose }) {
  const { manuscript, updateParagraph } = useManuscript();

  if (!issue) return null;

  const paragraph = manuscript?.paragraphs?.find(p => p.paragraph_id === issue.paragraph_id);
  const originalText = paragraph?.text || '';
  const suggestedText = issue.suggested_rewrite || '';

  const handleAccept = () => {
    updateParagraph(issue.paragraph_id, suggestedText);
    onClose();
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4" onClick={onClose}>
      <div className="bg-white rounded-lg shadow-xl max-w-4xl w-full max-h-[90vh] overflow-hidden flex flex-col" onClick={(e) => e.stopPropagation()}>
        {/* Header */}
        <div className="px-6 py-4 border-b bg-blue-50 flex items-center justify-between">
          <div>
            <h2 className="text-xl font-semibold text-gray-800">Suggested Rewrite (Track A)</h2>
            <p className="text-sm text-gray-600 mt-1">{issue.title || issue.message}</p>
          </div>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 transition"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto p-6">
          {/* Issue description */}
          {issue.description && (
            <div className="mb-6 p-4 bg-blue-50 rounded-lg border border-blue-200">
              <p className="text-sm text-gray-700">
                <strong>Issue:</strong> {issue.description}
              </p>
            </div>
          )}

          {/* Original text */}
          <div className="mb-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-3 flex items-center gap-2">
              <svg className="w-5 h-5 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
              Original Text
            </h3>
            <div className="p-4 bg-red-50 rounded-lg border border-red-200">
              <p className="text-gray-700 leading-relaxed text-justify">
                {originalText}
              </p>
            </div>
          </div>

          {/* Suggested rewrite */}
          <div className="mb-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-3 flex items-center gap-2">
              <svg className="w-5 h-5 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
              Suggested Rewrite
            </h3>
            <div className="p-4 bg-green-50 rounded-lg border border-green-200">
              <p className="text-gray-700 leading-relaxed text-justify">
                {suggestedText}
              </p>
            </div>
          </div>

          {/* Rationale if available */}
          {issue.rationale && (
            <div className="mb-6">
              <h3 className="text-lg font-semibold text-gray-800 mb-3">Rationale</h3>
              <div className="p-4 bg-gray-50 rounded-lg border border-gray-200">
                <p className="text-sm text-gray-700 leading-relaxed">
                  {issue.rationale}
                </p>
              </div>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="px-6 py-4 border-t bg-gray-50 flex items-center justify-end gap-3">
          <button
            onClick={onClose}
            className="px-5 py-2 text-gray-600 hover:text-gray-800 hover:bg-gray-200 rounded-md transition"
          >
            Dismiss
          </button>
          <button
            onClick={handleAccept}
            className="px-5 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition shadow"
          >
            Accept Rewrite
          </button>
        </div>
      </div>
    </div>
  );
}

export default RewriteModal;
