import React from 'react';

function OutlineModal({ issue, onClose }) {
  if (!issue) return null;

  const outline = issue.outline_suggestion || [];
  
  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4" onClick={onClose}>
      <div className="bg-white rounded-lg shadow-xl max-w-4xl w-full max-h-[90vh] overflow-hidden flex flex-col" onClick={(e) => e.stopPropagation()}>
        {/* Header */}
        <div className="px-6 py-4 border-b bg-purple-50 flex items-center justify-between">
          <div>
            <h2 className="text-xl font-semibold text-gray-800">Section Outline Suggestion (Track B)</h2>
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
            <div className="mb-6 p-4 bg-purple-50 rounded-lg border border-purple-200">
              <p className="text-sm text-gray-700">
                <strong>Issue:</strong> {issue.description}
              </p>
            </div>
          )}

          {/* Suggested outline */}
          <div className="mb-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center gap-2">
              <svg className="w-5 h-5 text-purple-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
              Suggested Outline
            </h3>
            
            <div className="space-y-3">
              {outline.map((item, index) => (
                <div key={index} className="p-4 bg-purple-50 rounded-lg border border-purple-200">
                  <div className="flex items-start gap-3">
                    <span className="flex-shrink-0 w-8 h-8 bg-purple-600 text-white rounded-full flex items-center justify-center text-sm font-semibold">
                      {index + 1}
                    </span>
                    <div className="flex-1">
                      <h4 className="font-semibold text-gray-800 mb-1">{item.subsection}</h4>
                      <p className="text-sm text-gray-600">{item.content}</p>
                    </div>
                  </div>
                </div>
              ))}
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
            Close
          </button>
          <button
            className="px-5 py-2 bg-purple-600 text-white rounded-md hover:bg-purple-700 transition shadow"
          >
            Export as Template
          </button>
        </div>
      </div>
    </div>
  );
}

export default OutlineModal;
