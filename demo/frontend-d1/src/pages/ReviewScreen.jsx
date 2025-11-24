import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useManuscript } from '../context/ManuscriptContext';

function ReviewScreen() {
  const navigate = useNavigate();
  const { manuscript, issues, loading } = useManuscript();

  if (loading || !manuscript) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading manuscript...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="h-screen flex flex-col bg-gray-100">
      {/* Header */}
      <div className="bg-white border-b px-6 py-3 flex items-center justify-between shadow-sm">
        <div className="flex items-center gap-4">
          <button
            onClick={() => navigate('/')}
            className="text-gray-600 hover:text-gray-800 flex items-center gap-2"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
            Back
          </button>
          <div className="h-6 w-px bg-gray-300"></div>
          <h1 className="text-xl font-semibold text-gray-800">PeerPreview - Manuscript Review</h1>
        </div>
        <div className="flex gap-3">
          <button className="px-4 py-2 text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded-md transition">
            Export
          </button>
          <button className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition shadow">
            Save Review
          </button>
        </div>
      </div>

      {/* Main content */}
      <div className="flex-1 flex overflow-hidden">
        {/* Manuscript view (left) - Placeholder */}
        <div className="flex-1 overflow-auto p-6 bg-white">
          <h1 className="text-3xl font-bold text-gray-900 mb-4">
            {manuscript.title}
          </h1>
          <p className="text-gray-600 mb-8 italic">
            Manuscript loaded successfully. {manuscript.sections?.length || 0} sections, {manuscript.paragraphs?.length || 0} paragraphs.
          </p>
          <div className="p-8 bg-blue-50 rounded-lg border border-blue-200">
            <p className="text-blue-800">
              Full manuscript view with sections will be implemented in the next phase.
              This placeholder confirms that data is loaded correctly.
            </p>
          </div>
        </div>

        {/* Issues panel (right) - Placeholder */}
        <div className="w-96 border-l bg-gray-50 p-6">
          <h2 className="text-xl font-semibold text-gray-800 mb-4">
            Issues ({issues.length})
          </h2>
          <div className="space-y-2">
            {issues.slice(0, 5).map((issue, idx) => (
              <div key={idx} className="p-3 bg-white rounded-lg border border-gray-200 shadow-sm">
                <div className="flex items-center gap-2 mb-1">
                  <span className={`
                    w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold text-white
                    ${issue.track === 'A' ? 'bg-blue-500' : issue.track === 'B' ? 'bg-purple-500' : 'bg-amber-500'}
                  `}>
                    {issue.track}
                  </span>
                  <span className="text-xs font-medium text-gray-500">{issue.severity}</span>
                </div>
                <p className="text-sm text-gray-700">{issue.title || issue.message}</p>
              </div>
            ))}
          </div>
          {issues.length > 5 && (
            <p className="text-sm text-gray-500 mt-4">
              +{issues.length - 5} more issues
            </p>
          )}
        </div>
      </div>
    </div>
  );
}

export default ReviewScreen;
