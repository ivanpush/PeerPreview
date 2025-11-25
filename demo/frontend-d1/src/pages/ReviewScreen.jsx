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
  const [selectedFigureId, setSelectedFigureId] = useState(null);

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
    <div className="h-screen flex flex-col bg-[#151515]">
      {/* Header */}
      <div className="bg-[#1D1D1D] border-b border-[#2E2E2E] px-6 py-2.5 flex items-center justify-between">
        <div className="flex items-center gap-4">
          <button
            onClick={() => navigate('/')}
            className="text-gray-500 hover:text-gray-300 flex items-center gap-2 transition text-sm"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
            Back
          </button>
          <div className="h-5 w-px bg-gray-700"></div>
          <h1 className="text-lg font-medium text-gray-200">PeerPreview</h1>
        </div>
        <div className="flex gap-2">
          <button className="px-3 py-1.5 text-sm text-gray-400 hover:text-gray-200 hover:bg-gray-800 rounded border border-gray-700 transition">
            Export
          </button>
          <button className="px-3 py-1.5 text-sm bg-[#3D4EFF] bg-opacity-90 text-white rounded hover:bg-opacity-100 transition">
            Save Review
          </button>
        </div>
      </div>

      {/* Main content area */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Top: Manuscript + Issues (60% + 40%) */}
        <div className="flex-1 flex overflow-hidden">
          {/* Manuscript view (left - 60%) */}
          <div className="w-[60%] overflow-hidden border-r border-[#2E2E2E]">
            <ManuscriptView />
          </div>

          {/* Issues panel (right - 40%) */}
          <div className="w-[40%] overflow-hidden bg-[#1D1D1D]">
            <IssuesPanel
              onOpenRewriteModal={setRewriteModalIssue}
              onOpenOutlineModal={setOutlineModalIssue}
              onOpenBiasedReviewModal={setBiasedReviewModalIssue}
            />
          </div>
        </div>

        {/* Bottom: Figures panel */}
        <div className="h-56 border-t border-[#2E2E2E] bg-[#1D1D1D] flex flex-col">
          <div className="px-4 py-2 border-b border-[#2E2E2E]">
            <div className="flex items-center gap-2 mb-2">
              <svg className="w-4 h-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              <h3 className="text-xs font-semibold text-gray-400 tracking-wide">FIGURES</h3>
            </div>
            <div className="flex gap-1.5 overflow-x-auto pb-1">
              {manuscript?.figures?.map((fig, idx) => {
                const isSelected = selectedFigureId === fig.figure_id;
                return (
                  <button
                    key={fig.figure_id || idx}
                    onClick={() => setSelectedFigureId(isSelected ? null : fig.figure_id)}
                    className={`flex-shrink-0 px-2.5 py-1 text-xs rounded border transition ${
                      isSelected
                        ? 'bg-blue-500/20 border-blue-500/50 text-blue-400'
                        : 'bg-[#252525] hover:bg-[#2A2A2A] text-gray-400 border-[#2E2E2E]'
                    }`}
                  >
                    {fig.label || `Fig ${idx + 1}`}
                  </button>
                );
              })}
              {(!manuscript?.figures || manuscript.figures.length === 0) && (
                <p className="text-xs text-gray-600">No figures available</p>
              )}
            </div>
          </div>

          {/* Caption display */}
          <div className="flex-1 overflow-y-auto p-4">
            {selectedFigureId ? (
              <>
                {manuscript?.figures?.find(f => f.figure_id === selectedFigureId) && (
                  <div className="space-y-2">
                    <p className="text-sm text-gray-300 leading-relaxed">
                      {manuscript.figures.find(f => f.figure_id === selectedFigureId).caption}
                    </p>
                    {manuscript.figures.find(f => f.figure_id === selectedFigureId).mentions?.length > 0 && (
                      <div className="flex items-center gap-2 text-xs text-gray-500 mt-3">
                        <span>Referenced in:</span>
                        {manuscript.figures.find(f => f.figure_id === selectedFigureId).mentions.map((pid, idx) => (
                          <span key={pid} className="px-2 py-0.5 bg-gray-800 rounded">
                            {pid}
                          </span>
                        ))}
                      </div>
                    )}
                  </div>
                )}
              </>
            ) : (
              <p className="text-sm text-gray-500 text-center py-8">
                Select a figure to view its caption
              </p>
            )}
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
