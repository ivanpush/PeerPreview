import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useManuscript } from '../context/ManuscriptContext';
import ManuscriptView from '../components/ManuscriptView';
import IssuesPanel from '../components/IssuesPanel';

function ReviewScreen() {
  const navigate = useNavigate();
  const { manuscript, issues, loading } = useManuscript();
  const [rewriteModalIssue, setRewriteModalIssue] = useState(null);
  const [outlineModalIssue, setOutlineModalIssue] = useState(null);
  const [biasedReviewModalIssue, setBiasedReviewModalIssue] = useState(null);

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
        {/* Manuscript view (left) */}
        <div className="flex-1 overflow-hidden">
          <ManuscriptView />
        </div>

        {/* Issues panel (right) */}
        <div className="w-96 border-l overflow-hidden">
          <IssuesPanel
            onOpenRewriteModal={setRewriteModalIssue}
            onOpenOutlineModal={setOutlineModalIssue}
            onOpenBiasedReviewModal={setBiasedReviewModalIssue}
          />
        </div>
      </div>

      {/* Modals - TODO: Implement in Phase 5 */}
      {/* {rewriteModalIssue && <RewriteModal issue={rewriteModalIssue} onClose={() => setRewriteModalIssue(null)} />} */}
      {/* {outlineModalIssue && <OutlineModal issue={outlineModalIssue} onClose={() => setOutlineModalIssue(null)} />} */}
      {/* {biasedReviewModalIssue && <BiasedReviewModal issue={biasedReviewModalIssue} onClose={() => setBiasedReviewModalIssue(null)} />} */}
    </div>
  );
}

export default ReviewScreen;
