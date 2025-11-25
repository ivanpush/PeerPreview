import React, { useState } from 'react';
import { useManuscript } from '../context/ManuscriptContext';
import { theme, withOpacity, getTrackColor } from '../styles/theme';

function BiasedReviewModal({ issue, onClose }) {
  const { biasProfile, issues } = useManuscript();
  const [selectedCritiqueId, setSelectedCritiqueId] = useState(issue?.id);
  const contentRef = React.useRef(null);

  if (!issue || !biasProfile) return null;

  // Get all Track C issues for navigation
  const trackCIssues = issues.filter(i => i.track === 'C');
  const currentIndex = trackCIssues.findIndex(i => i.id === selectedCritiqueId);
  const currentIssue = trackCIssues[currentIndex] || issue;

  // Scroll to top when critique changes
  React.useEffect(() => {
    if (contentRef.current) {
      contentRef.current.scrollTop = 0;
    }
  }, [selectedCritiqueId]);

  // Separate major and minor critiques
  const majorCritiques = trackCIssues.filter(i => i.severity === 'major');
  const minorCritiques = trackCIssues.filter(i => i.severity === 'minor');

  const handlePrevious = () => {
    if (currentIndex > 0) {
      setSelectedCritiqueId(trackCIssues[currentIndex - 1].id);
    }
  };

  const handleNext = () => {
    if (currentIndex < trackCIssues.length - 1) {
      setSelectedCritiqueId(trackCIssues[currentIndex + 1].id);
    }
  };

  return (
    <div
      className="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center z-50 p-4"
      onClick={onClose}
    >
      <div
        className="rounded-xl shadow-2xl max-w-5xl w-full max-h-[90vh] overflow-hidden flex flex-col"
        style={{
          backgroundColor: '#1A1A1A',
          border: '1px solid rgba(255,255,255,0.07)'
        }}
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div
          className="px-6 py-4 flex items-center justify-between"
          style={{ borderBottom: '1px solid rgba(255,255,255,0.08)' }}
        >
          <div className="flex-1">
            <div className="flex items-center gap-3 mb-1">
              <span
                className="px-2 py-0.5 rounded text-xs font-bold uppercase tracking-wide"
                style={{
                  backgroundColor: withOpacity(getTrackColor('C'), 0.2),
                  color: getTrackColor('C'),
                  border: `1px solid ${getTrackColor('C')}`
                }}
              >
                Counterpoint Review
              </span>
              <span className="text-xs text-gray-500">Track C</span>
            </div>
            <h2 className="text-lg font-semibold text-white">
              {biasProfile.reviewer_archetype}
            </h2>
            <div className="mt-2 flex items-center gap-2 text-xs text-amber-400">
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
              <span>Simulated biased reviewer - stress test only</span>
            </div>
          </div>
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-300 transition ml-4"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto p-6 space-y-6">
          {/* Global Reviewer Positioning */}
          <div
            className="rounded-lg p-5"
            style={{
              backgroundColor: 'rgba(255,255,255,0.02)',
              border: '1px solid rgba(255,255,255,0.08)'
            }}
          >
            <h3 className="text-sm font-semibold text-gray-400 uppercase tracking-wide mb-3">
              Reviewer Summary
            </h3>
            <p className="text-sm text-gray-300 leading-relaxed mb-4">
              {biasProfile.summary_statement}
            </p>
            <p className="text-sm text-gray-300 leading-relaxed font-medium">
              <span className="text-amber-400">However, </span>
              {biasProfile.pivot_statement}
            </p>
          </div>

          {/* Navigation between critiques */}
          {trackCIssues.length > 1 && (
            <div
              className="flex items-center justify-between p-4 rounded-lg"
              style={{
                backgroundColor: 'rgba(255,255,255,0.03)',
                border: '1px solid rgba(255,255,255,0.08)'
              }}
            >
              <button
                onClick={handlePrevious}
                disabled={currentIndex === 0}
                className="flex items-center gap-2 px-3 py-1.5 rounded text-sm transition disabled:opacity-30 disabled:cursor-not-allowed"
                style={{
                  backgroundColor: currentIndex === 0 ? 'transparent' : 'rgba(255,255,255,0.05)',
                  color: '#A0A0A0'
                }}
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                </svg>
                Previous
              </button>
              <span className="text-sm text-gray-400">
                Critique {currentIndex + 1} of {trackCIssues.length}
              </span>
              <button
                onClick={handleNext}
                disabled={currentIndex === trackCIssues.length - 1}
                className="flex items-center gap-2 px-3 py-1.5 rounded text-sm transition disabled:opacity-30 disabled:cursor-not-allowed"
                style={{
                  backgroundColor: currentIndex === trackCIssues.length - 1 ? 'transparent' : 'rgba(255,255,255,0.05)',
                  color: '#A0A0A0'
                }}
              >
                Next
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
              </button>
            </div>
          )}

          {/* Current Critique */}
          <div>
            <div className="flex items-center gap-3 mb-4">
              <span
                className="px-2 py-0.5 rounded text-xs font-medium border"
                style={{
                  backgroundColor: currentIssue.severity === 'major'
                    ? 'rgba(229, 72, 77, 0.15)'
                    : 'rgba(255, 190, 60, 0.15)',
                  color: currentIssue.severity === 'major' ? '#E5484D' : '#FFBE3C',
                  borderColor: currentIssue.severity === 'major'
                    ? 'rgba(229, 72, 77, 0.3)'
                    : 'rgba(255, 190, 60, 0.3)'
                }}
              >
                {currentIssue.severity}
              </span>
              <span className="text-xs text-gray-500">{currentIssue.category}</span>
            </div>

            <h3 className="text-xl font-semibold text-white mb-4">
              {currentIssue.title}
            </h3>

            {/* Location */}
            {currentIssue.paragraph_id && (
              <div className="flex items-center gap-2 mb-4 text-xs">
                <svg className="w-4 h-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                <span
                  className="px-2 py-0.5 rounded"
                  style={{
                    backgroundColor: withOpacity(theme.accent.uiBlue, 0.15),
                    color: theme.accent.uiBlue,
                    border: `1px solid ${withOpacity(theme.accent.uiBlue, 0.3)}`
                  }}
                >
                  {currentIssue.section_id?.replace('sec_', '')}
                </span>
                <span
                  className="px-2 py-0.5 rounded"
                  style={{
                    backgroundColor: withOpacity(theme.accent.uiBlue, 0.15),
                    color: theme.accent.uiBlue,
                    border: `1px solid ${withOpacity(theme.accent.uiBlue, 0.3)}`
                  }}
                >
                  {currentIssue.paragraph_id}
                </span>
              </div>
            )}

            {/* Original text quoted */}
            {currentIssue.original_text && (
              <div
                className="mb-5 pl-4 border-l-2 py-2"
                style={{
                  borderColor: withOpacity(getTrackColor('C'), 0.4),
                  backgroundColor: withOpacity(getTrackColor('C'), 0.05)
                }}
              >
                <p className="text-sm italic text-gray-400 leading-relaxed">
                  "{currentIssue.original_text}"
                </p>
              </div>
            )}

            {/* Critique */}
            <div className="mb-5">
              <h4 className="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-3">
                Critique
              </h4>
              <div
                className="rounded-lg p-4"
                style={{
                  backgroundColor: 'rgba(199, 90, 122, 0.08)',
                  border: '1px solid rgba(199, 90, 122, 0.2)'
                }}
              >
                <p className="text-sm text-gray-300 leading-relaxed">
                  {currentIssue.critique}
                </p>
              </div>
            </div>

            {/* Strategic Solution */}
            {currentIssue.suggested_revision && (
              <div className="mb-5">
                <h4 className="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-3 flex items-center gap-2">
                  <svg className="w-4 h-4 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                  </svg>
                  Strategic Solution
                </h4>
                <div
                  className="rounded-lg p-4"
                  style={{
                    backgroundColor: 'rgba(91, 174, 184, 0.08)',
                    border: '1px solid rgba(91, 174, 184, 0.2)'
                  }}
                >
                  <p className="text-sm text-gray-300 leading-relaxed">
                    {currentIssue.suggested_revision}
                  </p>
                </div>
                {currentIssue.addressable !== undefined && (
                  <div className="mt-3 flex items-center gap-2 text-xs">
                    {currentIssue.addressable ? (
                      <>
                        <svg className="w-4 h-4 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        <span className="text-green-400">Addressable via additional experiments or revision</span>
                      </>
                    ) : (
                      <>
                        <svg className="w-4 h-4 text-amber-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                        </svg>
                        <span className="text-amber-400">Reflects philosophical preference - difficult to address</span>
                      </>
                    )}
                  </div>
                )}
              </div>
            )}

            {/* Rationale */}
            {currentIssue.rationale && (
              <div
                className="rounded-lg p-4"
                style={{
                  backgroundColor: 'rgba(255,255,255,0.02)',
                  border: '1px solid rgba(255,255,255,0.08)'
                }}
              >
                <p className="text-xs text-gray-500 italic">
                  <span className="font-semibold">Reviewer bias context: </span>
                  {currentIssue.rationale}
                </p>
              </div>
            )}
          </div>

          {/* Global Suggestions Section */}
          {biasProfile.global_suggestions && biasProfile.global_suggestions.length > 0 && (
            <div>
              <h3 className="text-sm font-semibold text-gray-400 uppercase tracking-wide mb-3 flex items-center gap-2">
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
                Global Strategic Suggestions
              </h3>
              <div className="space-y-3">
                {biasProfile.global_suggestions.map((suggestion, idx) => (
                  <div
                    key={suggestion.id}
                    className="rounded-lg p-4"
                    style={{
                      backgroundColor: 'rgba(101, 178, 232, 0.08)',
                      border: '1px solid rgba(101, 178, 232, 0.2)'
                    }}
                  >
                    <h4 className="text-sm font-medium text-gray-200 mb-2">
                      {suggestion.title}
                    </h4>
                    <p className="text-xs text-gray-400 leading-relaxed">
                      {suggestion.suggestion}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Summary of all critiques */}
          <div>
            <h3 className="text-sm font-semibold text-gray-400 uppercase tracking-wide mb-3">
              All Critiques ({trackCIssues.length})
            </h3>
            <div className="space-y-2">
              {/* Major Critiques */}
              {majorCritiques.length > 0 && (
                <div>
                  <h4 className="text-xs text-gray-500 mb-2">Major ({majorCritiques.length})</h4>
                  {majorCritiques.map((critique) => (
                    <button
                      key={critique.id}
                      onClick={() => setSelectedCritiqueId(critique.id)}
                      className="w-full text-left px-3 py-2 rounded transition mb-1"
                      style={{
                        backgroundColor: critique.id === selectedCritiqueId
                          ? 'rgba(229, 72, 77, 0.15)'
                          : 'rgba(255,255,255,0.03)',
                        border: critique.id === selectedCritiqueId
                          ? '1px solid rgba(229, 72, 77, 0.3)'
                          : '1px solid rgba(255,255,255,0.08)'
                      }}
                    >
                      <div className="flex items-center gap-2">
                        <span className="text-xs font-mono text-gray-500">{critique.id}</span>
                        <span className="text-xs text-gray-300 flex-1">{critique.title}</span>
                      </div>
                    </button>
                  ))}
                </div>
              )}

              {/* Minor Critiques */}
              {minorCritiques.length > 0 && (
                <div className="mt-3">
                  <h4 className="text-xs text-gray-500 mb-2">Minor ({minorCritiques.length})</h4>
                  {minorCritiques.map((critique) => (
                    <button
                      key={critique.id}
                      onClick={() => setSelectedCritiqueId(critique.id)}
                      className="w-full text-left px-3 py-2 rounded transition mb-1"
                      style={{
                        backgroundColor: critique.id === selectedCritiqueId
                          ? 'rgba(255, 190, 60, 0.15)'
                          : 'rgba(255,255,255,0.03)',
                        border: critique.id === selectedCritiqueId
                          ? '1px solid rgba(255, 190, 60, 0.3)'
                          : '1px solid rgba(255,255,255,0.08)'
                      }}
                    >
                      <div className="flex items-center gap-2">
                        <span className="text-xs font-mono text-gray-500">{critique.id}</span>
                        <span className="text-xs text-gray-300 flex-1">{critique.title}</span>
                      </div>
                    </button>
                  ))}
                </div>
              )}
            </div>
          </div>

          {/* Overall Recommendation */}
          <div
            className="rounded-lg p-5"
            style={{
              backgroundColor: 'rgba(229, 72, 77, 0.08)',
              border: '1px solid rgba(229, 72, 77, 0.2)'
            }}
          >
            <div className="flex items-center gap-3 mb-3">
              <svg className="w-5 h-5 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              <h3 className="text-sm font-semibold text-gray-200 uppercase tracking-wide">
                Overall Recommendation
              </h3>
            </div>
            <p className="text-lg font-semibold text-red-400 mb-2">
              {biasProfile.overall_recommendation}
            </p>
            <p className="text-sm text-gray-400 leading-relaxed">
              {biasProfile.recommendation_rationale}
            </p>
            <div className="mt-3 text-xs text-gray-500">
              <span className="font-medium">Reviewer Confidence: </span>
              {biasProfile.confidence_level}
            </div>
          </div>
        </div>

        {/* Footer */}
        <div
          className="px-6 py-4 flex items-center justify-end gap-3"
          style={{ borderTop: '1px solid rgba(255,255,255,0.08)' }}
        >
          <button
            onClick={onClose}
            className="px-5 py-2 text-white hover:opacity-80 transition font-medium"
            style={{
              backgroundColor: 'rgba(255, 255, 255, 0.08)',
              borderRadius: '6px',
              border: '1px solid rgba(255, 255, 255, 0.12)'
            }}
          >
            Close
          </button>
          <button
            className="px-5 py-2 text-white hover:opacity-90 transition shadow-lg font-medium"
            style={{
              backgroundColor: getTrackColor('C'),
              borderRadius: '6px'
            }}
          >
            Export Response Strategy
          </button>
        </div>
      </div>
    </div>
  );
}

export default BiasedReviewModal;
