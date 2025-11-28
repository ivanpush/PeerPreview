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
  const { manuscript, issues, loading, lastRewrite, undoLastRewrite, loadMockData, exportReview } = useManuscript();
  const [showUndoBanner, setShowUndoBanner] = useState(false);
  const [rewriteModalIssue, setRewriteModalIssue] = useState(null);
  const [outlineModalIssue, setOutlineModalIssue] = useState(null);
  const [biasedReviewModalIssue, setBiasedReviewModalIssue] = useState(null);
  const [selectedFigureId, setSelectedFigureId] = useState(null);
  const [figuresPanelExpanded, setFiguresPanelExpanded] = useState(false);
  const selectIssueRef = React.useRef(null);

  // Load mock data if manuscript is not already loaded (for direct navigation/refresh)
  useEffect(() => {
    if (!manuscript && !loading) {
      loadMockData();
    }
  }, [manuscript, loading, loadMockData]);

  // Handler to open figure panel and select a figure
  const handleFigureClick = (figureId) => {
    setSelectedFigureId(figureId);
    setFiguresPanelExpanded(true);
  };

  // Handler to scroll to a paragraph from figure panel
  const handleParagraphClick = (paragraphId) => {
    const element = document.getElementById(paragraphId);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  };

  // Show undo banner when a rewrite is made and auto-hide after 3 seconds
  useEffect(() => {
    if (lastRewrite) {
      setShowUndoBanner(true);

      // Auto-hide after 3 seconds
      const timeout = setTimeout(() => {
        setShowUndoBanner(false);
      }, 3000);

      return () => clearTimeout(timeout);
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
          <button
            onClick={exportReview}
            className="px-3 py-1.5 text-sm text-gray-400 hover:text-gray-200 hover:bg-gray-800 rounded border border-gray-700 transition"
          >
            Export
          </button>
          <button className="px-3 py-1.5 text-sm bg-[#3D4EFF] bg-opacity-90 text-white rounded hover:bg-opacity-100 transition">
            Save Review
          </button>
        </div>
      </div>

      {/* Main content area */}
      <div className="flex-1 flex flex-col overflow-hidden bg-[#1D1D1D]">
        {/* Top: Manuscript + Issues */}
        <div className="flex-1 flex overflow-hidden justify-center">
          {/* Manuscript view (left - flexible with max width) */}
          <div className="flex-1 max-w-5xl overflow-hidden">
            <ManuscriptView onFigureClick={handleFigureClick} selectIssueRef={selectIssueRef} />
          </div>

          {/* Issues panel (right - fixed width) */}
          <div className="w-[480px] overflow-hidden border-l border-[rgba(255,255,255,0.08)]">
            <IssuesPanel
              onOpenRewriteModal={setRewriteModalIssue}
              onOpenOutlineModal={setOutlineModalIssue}
              onOpenBiasedReviewModal={setBiasedReviewModalIssue}
              onSelectIssue={selectIssueRef}
            />
          </div>
        </div>

        {/* Bottom: Figures panel - Collapsible */}
        <div className={`border-t border-[#2E2E2E] bg-[#1D1D1D] flex flex-col transition-all duration-300 ${
          figuresPanelExpanded ? 'h-56' : 'h-12'
        }`}>
          {/* Header row with toggle */}
          <div className="px-4 py-2 flex items-center gap-2">
            <button
              onClick={() => setFiguresPanelExpanded(!figuresPanelExpanded)}
              className="text-gray-500 hover:text-gray-300 transition mr-1"
            >
              <svg className={`w-4 h-4 transition-transform ${figuresPanelExpanded ? '' : 'rotate-180'}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
              </svg>
            </button>
            <svg className="w-4 h-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
            <h3 className="text-xs font-semibold text-gray-400 tracking-wide">FIGURES</h3>

            {/* Inline tabs when collapsed */}
            {!figuresPanelExpanded && (
              <div className="flex gap-1.5 overflow-x-auto ml-4 flex-1">
                {manuscript?.figures?.slice(0, 10).map((fig, idx) => {
                  const isSelected = selectedFigureId === fig.figure_id;
                  return (
                    <button
                      key={fig.figure_id || idx}
                      onClick={() => {
                        setSelectedFigureId(isSelected ? null : fig.figure_id);
                        if (!isSelected) setFiguresPanelExpanded(true);
                      }}
                      className="flex-shrink-0 px-2 py-0.5 text-xs rounded border transition"
                      style={isSelected ? {
                        backgroundColor: 'rgba(101, 178, 232, 0.2)',
                        borderColor: 'rgba(101, 178, 232, 0.5)',
                        color: '#65B2E8'
                      } : {
                        backgroundColor: '#252525',
                        borderColor: '#2E2E2E',
                        color: '#A0A0A0'
                      }}
                      onMouseEnter={(e) => {
                        if (!isSelected) e.currentTarget.style.backgroundColor = '#2A2A2A';
                      }}
                      onMouseLeave={(e) => {
                        if (!isSelected) e.currentTarget.style.backgroundColor = '#252525';
                      }}
                    >
                      {fig.label || `Fig ${idx + 1}`}
                    </button>
                  );
                })}
              </div>
            )}
          </div>

          {/* Expanded content */}
          {figuresPanelExpanded && (
            <>
              <div className="px-4 pb-2 border-b border-[#2E2E2E]">
                <div className="flex gap-1.5 overflow-x-auto pb-1">
                  {manuscript?.figures?.map((fig, idx) => {
                    const isSelected = selectedFigureId === fig.figure_id;
                    return (
                      <button
                        key={fig.figure_id || idx}
                        onClick={() => setSelectedFigureId(isSelected ? null : fig.figure_id)}
                        className="flex-shrink-0 px-2.5 py-1 text-xs rounded border transition"
                        style={isSelected ? {
                          backgroundColor: 'rgba(101, 178, 232, 0.2)',
                          borderColor: 'rgba(101, 178, 232, 0.5)',
                          color: '#65B2E8'
                        } : {
                          backgroundColor: '#252525',
                          borderColor: '#2E2E2E',
                          color: '#A0A0A0'
                        }}
                        onMouseEnter={(e) => {
                          if (!isSelected) e.currentTarget.style.backgroundColor = '#2A2A2A';
                        }}
                        onMouseLeave={(e) => {
                          if (!isSelected) e.currentTarget.style.backgroundColor = '#252525';
                        }}
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
                              <button
                                key={pid}
                                onClick={() => handleParagraphClick(pid)}
                                className="px-2 py-0.5 bg-gray-800 hover:bg-gray-700 rounded transition cursor-pointer"
                              >
                                {pid}
                              </button>
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
            </>
          )}
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
