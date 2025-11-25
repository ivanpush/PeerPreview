import React from 'react';
import { useManuscript } from '../context/ManuscriptContext';

function BiasedReviewModal({ issue, onClose }) {
  const { biasProfile } = useManuscript();

  if (!issue) return null;

  const critique = issue.biased_critique || {};
  
  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4" onClick={onClose}>
      <div className="bg-white rounded-lg shadow-xl max-w-4xl w-full max-h-[90vh] overflow-hidden flex flex-col" onClick={(e) => e.stopPropagation()}>
        {/* Header */}
        <div className="px-6 py-4 border-b bg-amber-50 flex items-center justify-between">
          <div>
            <h2 className="text-xl font-semibold text-gray-800">Biased Reviewer Perspective (Track C)</h2>
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
          {/* Bias profile info */}
          {biasProfile && (
            <div className="mb-6 p-4 bg-amber-50 rounded-lg border border-amber-200">
              <div className="flex items-start gap-3 mb-3">
                <svg className="w-5 h-5 text-amber-600 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
                <div className="flex-1">
                  <p className="text-sm font-semibold text-amber-900">Simulated Reviewer Bias</p>
                  <p className="text-xs text-amber-700 mt-1">
                    Field: {biasProfile.field || 'Unknown'} | 
                    Orthodoxy: {biasProfile.orthodoxy_beliefs?.join(', ')}
                  </p>
                </div>
              </div>
            </div>
          )}

          {/* Issue description */}
          {issue.description && (
            <div className="mb-6 p-4 bg-gray-50 rounded-lg border border-gray-200">
              <p className="text-sm text-gray-700">
                <strong>Context:</strong> {issue.description}
              </p>
            </div>
          )}

          {/* Biased critique */}
          <div className="mb-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-3 flex items-center gap-2">
              <svg className="w-5 h-5 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-3l-4 4z" />
              </svg>
              Reviewer's Critique
            </h3>
            <div className="p-4 bg-amber-50 rounded-lg border border-amber-200">
              <p className="text-gray-700 leading-relaxed">
                {critique.comment || 'No specific critique provided.'}
              </p>
            </div>
          </div>

          {/* Bias indicators */}
          {critique.bias_indicators && critique.bias_indicators.length > 0 && (
            <div className="mb-6">
              <h3 className="text-lg font-semibold text-gray-800 mb-3">Bias Indicators</h3>
              <div className="space-y-2">
                {critique.bias_indicators.map((indicator, index) => (
                  <div key={index} className="flex items-start gap-2 p-3 bg-red-50 rounded-lg border border-red-200">
                    <svg className="w-4 h-4 text-red-600 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    <p className="text-sm text-gray-700">{indicator}</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Alternative perspectives */}
          {critique.alternative_view && (
            <div className="mb-6">
              <h3 className="text-lg font-semibold text-gray-800 mb-3 flex items-center gap-2">
                <svg className="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                </svg>
                More Balanced Perspective
              </h3>
              <div className="p-4 bg-green-50 rounded-lg border border-green-200">
                <p className="text-sm text-gray-700 leading-relaxed">
                  {critique.alternative_view}
                </p>
              </div>
            </div>
          )}

          {/* Suggested response */}
          {critique.suggested_response && (
            <div className="mb-6">
              <h3 className="text-lg font-semibold text-gray-800 mb-3">Suggested Response Strategy</h3>
              <div className="p-4 bg-blue-50 rounded-lg border border-blue-200">
                <p className="text-sm text-gray-700 leading-relaxed">
                  {critique.suggested_response}
                </p>
              </div>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="px-6 py-4 border-t bg-gray-50 flex items-center justify-between">
          <div className="text-xs text-gray-500">
            This simulates a biased review to help you prepare responses
          </div>
          <div className="flex gap-3">
            <button
              onClick={onClose}
              className="px-5 py-2 text-gray-600 hover:text-gray-800 hover:bg-gray-200 rounded-md transition"
            >
              Close
            </button>
            <button
              className="px-5 py-2 bg-amber-600 text-white rounded-md hover:bg-amber-700 transition shadow"
            >
              Draft Response
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default BiasedReviewModal;
