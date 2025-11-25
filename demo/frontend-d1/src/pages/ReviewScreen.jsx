import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useManuscript } from '../context/ManuscriptContext';
import ManuscriptView from '../components/ManuscriptView';
import IssuesPanel from '../components/IssuesPanel';
import RewriteModal from '../components/RewriteModal';
import OutlineModal from '../components/OutlineModal';
import BiasedReviewModal from '../components/BiasedReviewModal';
import UndoBanner from '../components/UndoBanner';

function ReviewScreen() {
  const navigate = useNavigate();
  const { manuscript, issues, loading, lastRewrite, undoLastRewrite } = useManuscript();
  const [showUndoBanner, setShowUndoBanner] = useState(false);
  const [rewriteModalIssue, setRewriteModalIssue] = useState(null);
  const [outlineModalIssue, setOutlineModalIssue] = useState(null);
  const [biasedReviewModalIssue, setBiasedReviewModalIssue] = useState(null);

  // Show undo banner when a rewrite is made
  useEffect(() => {
    if (lastRewrite) {
      setShowUndoBanner(true);
    }
  }, [lastRewrite]);

  const handleUndo = () => {
    undoLastRewrite();
    setShowUndoBanner(false);
  };

  const handleDismissBanner = () => {
    setShowUndoBanner(false);
  };

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
    <div className="h-screen flex flex-col bg-gray-950">
      {/* Header */}
      <div className="bg-gray-900 border-b border-gray-800 px-6 py-3 flex items-center justify-between shadow-lg">
        <div className="flex items-center gap-4">
          <button
            onClick={() => navigate('/')}
            className="text-gray-400 hover:text-gray-200 flex items-center gap-2 transition"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
            Back
          </button>
          <div className="h-6 w-px bg-gray-700"></div>
          <h1 className="text-xl font-semibold text-gray-100">PeerPreview - Manuscript Review</h1>
        </div>
        <div className="flex gap-3">
          <button className="px-4 py-2 text-gray-400 hover:text-gray-200 hover:bg-gray-800 rounded-md transition">
            Export
          </button>
          <button className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition shadow">
            Save Review
          </button>
        </div>
      </div>

      {/* Main content area */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Top: Manuscript + Issues (2/3 + 1/3) */}
        <div className="flex-1 flex overflow-hidden">
          {/* Manuscript view (left - 2/3) */}
          <div className="w-2/3 overflow-hidden border-r border-gray-800">
            <ManuscriptView />
          </div>

          {/* Issues panel (right - 1/3) */}
          <div className="w-1/3 overflow-hidden bg-gray-900">
            <IssuesPanel
              onOpenRewriteModal={setRewriteModalIssue}
              onOpenOutlineModal={setOutlineModalIssue}
              onOpenBiasedReviewModal={setBiasedReviewModalIssue}
            />
          </div>
        </div>

        {/* Bottom: Figures panel */}
        <div className="h-48 border-t border-gray-800 bg-gray-900">
          <div className="h-full p-4">
            <div className="flex items-center gap-2 mb-3">
              <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              <h3 className="text-sm font-semibold text-gray-300">Figures</h3>
            </div>
            <div className="flex gap-2 overflow-x-auto">
              {manuscript?.figures?.map((fig, idx) => (
                <button
                  key={fig.figure_id || idx}
                  className="flex-shrink-0 px-4 py-2 bg-gray-800 hover:bg-gray-700 text-gray-300 text-sm rounded border border-gray-700 transition"
                >
                  {fig.label || `Figure ${idx + 1}`}
                </button>
              ))}
              {(!manuscript?.figures || manuscript.figures.length === 0) && (
                <p className="text-sm text-gray-500">No figures in this manuscript</p>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Modals */}
      {rewriteModalIssue && <RewriteModal issue={rewriteModalIssue} onClose={() => setRewriteModalIssue(null)} />}
      {outlineModalIssue && <OutlineModal issue={outlineModalIssue} onClose={() => setOutlineModalIssue(null)} />}
      {biasedReviewModalIssue && <BiasedReviewModal issue={biasedReviewModalIssue} onClose={() => setBiasedReviewModalIssue(null)} />}

      {/* Undo Banner */}
      {showUndoBanner && lastRewrite && (
        <UndoBanner
          message={`Paragraph updated: "${lastRewrite.paragraphId}"`}
          onUndo={handleUndo}
          onDismiss={handleDismissBanner}
        />
      )}
    </div>
  );
}

export default ReviewScreen;
