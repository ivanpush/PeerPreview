import React, { useState } from 'react';
import { useManuscript } from '../context/ManuscriptContext';
import { theme, withOpacity, getTrackColor, getSeverityColor } from '../styles/theme';

function IssuesPanel({ onOpenRewriteModal, onOpenOutlineModal, onOpenBiasedReviewModal }) {
  const { issues, setSelectedIssue, selectedIssue, manuscript } = useManuscript();
  const [filterTrack, setFilterTrack] = useState('all');
  const [dismissedIssues, setDismissedIssues] = useState(new Set());

  const filteredIssues = issues.filter(issue =>
    filterTrack === 'all' || issue.track === filterTrack
  );

  const toggleDismiss = (issueId, e) => {
    e.stopPropagation();
    setDismissedIssues(prev => {
      const newSet = new Set(prev);
      if (newSet.has(issueId)) {
        newSet.delete(issueId);
      } else {
        newSet.add(issueId);
      }
      return newSet;
    });
  };

  // Severity badge styling (warm colors)
  const getSeverityBadgeClass = (severity) => {
    const color = getSeverityColor(severity);
    return `px-2 py-0.5 rounded text-xs font-medium border`;
  };

  // Track badge styling (cool colors)
  const getTrackBadgeClass = (track) => {
    return `w-6 h-6 rounded-full flex items-center justify-center text-white text-xs font-bold`;
  };

  const handleIssueClick = (issue) => {
    setSelectedIssue(issue);

    // Scroll based on issue type
    if (issue.paragraph_id) {
      // ManuscriptView will handle scrolling via useEffect
    } else if (issue.section_id) {
      const section = document.getElementById(issue.section_id);
      section?.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  };

  const renderActionButton = (issue) => {
    const buttonStyle = {
      backgroundColor: withOpacity(theme.action.primary, 0.12),
      color: theme.action.primary,
      border: `1px solid ${withOpacity(theme.action.primary, 0.3)}`
    };

    const buttonHoverClass = "hover:opacity-80 transition inline-flex items-center gap-1.5";

    if (issue.issue_type === 'paragraph_rewrite' || issue.suggested_rewrite) {
      return (
        <button
          onClick={(e) => {
            e.stopPropagation();
            onOpenRewriteModal(issue);
          }}
          className={`mt-3 px-3 py-1.5 text-xs rounded ${buttonHoverClass}`}
          style={buttonStyle}
        >
          <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
          </svg>
          View Rewrite
        </button>
      );
    }

    if (issue.issue_type === 'section_outline' || issue.outline_suggestion) {
      return (
        <button
          onClick={(e) => {
            e.stopPropagation();
            onOpenOutlineModal(issue);
          }}
          className={`mt-3 px-3 py-1.5 text-xs rounded ${buttonHoverClass}`}
          style={buttonStyle}
        >
          <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 10h16M4 14h16M4 18h16" />
          </svg>
          View Outline
        </button>
      );
    }

    if (issue.track === 'C' || issue.issue_type === 'biased_critique') {
      return (
        <button
          onClick={(e) => {
            e.stopPropagation();
            onOpenBiasedReviewModal(issue);
          }}
          className={`mt-3 px-3 py-1.5 text-xs rounded ${buttonHoverClass}`}
          style={buttonStyle}
        >
          <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
          </svg>
          View Review
        </button>
      );
    }

    return null;
  };

  return (
    <div className="h-full flex flex-col" style={{ backgroundColor: theme.background.primary }}>
      {/* Header with filters */}
      <div className="pt-5 pb-4 px-4" style={{ backgroundColor: theme.background.secondary, borderBottom: `1px solid ${theme.border.primary}` }}>
        <h2 className="text-[15px] font-semibold mb-3 px-1" style={{ color: theme.text.secondary }}>
          Issues ({filteredIssues.length})
        </h2>

        <div className="flex gap-2">
          {/* All Tab */}
          <button
            onClick={() => setFilterTrack('all')}
            className="relative px-4 py-2.5 rounded text-sm font-medium transition flex flex-col items-center"
            style={{
              backgroundColor: filterTrack === 'all' ? theme.background.elevated : 'transparent',
              color: filterTrack === 'all' ? theme.text.primary : theme.text.tertiary
            }}
          >
            <span className="font-semibold">All</span>
            {filterTrack === 'all' && (
              <div className="absolute bottom-0 left-0 right-0 h-0.5 rounded-full" style={{ backgroundColor: theme.text.tertiary }}></div>
            )}
          </button>

          {/* Rigor Tab */}
          <button
            onClick={() => setFilterTrack('A')}
            className="relative px-4 py-3 rounded text-sm font-medium transition flex flex-col items-center gap-1.5"
            style={{
              backgroundColor: 'transparent',
              color: filterTrack === 'A' ? theme.track.rigor : theme.text.tertiary,
              border: filterTrack === 'A' ? `1px solid ${theme.track.rigor}` : '1px solid transparent'
            }}
          >
            <span className="font-semibold">Rigor</span>
            <span className="text-[11px] whitespace-nowrap" style={{ opacity: 0.55 }}>Structure & reasoning</span>
          </button>

          {/* Clarity Tab */}
          <button
            onClick={() => setFilterTrack('B')}
            className="relative px-4 py-3 rounded text-sm font-medium transition flex flex-col items-center gap-1.5"
            style={{
              backgroundColor: 'transparent',
              color: filterTrack === 'B' ? theme.track.clarity : theme.text.tertiary,
              border: filterTrack === 'B' ? `1px solid ${theme.track.clarity}` : '1px solid transparent'
            }}
          >
            <span className="font-semibold">Clarity</span>
            <span className="text-[11px] whitespace-nowrap" style={{ opacity: 0.55 }}>Language & style</span>
          </button>

          {/* Counterpoint Tab */}
          <button
            onClick={() => setFilterTrack('C')}
            className="relative px-4 py-3 rounded text-sm font-medium transition flex flex-col items-center gap-1.5"
            style={{
              backgroundColor: 'transparent',
              color: filterTrack === 'C' ? theme.track.counterpoint : theme.text.tertiary,
              border: filterTrack === 'C' ? `1px solid ${theme.track.counterpoint}` : '1px solid transparent'
            }}
          >
            <span className="font-semibold">Counterpoint</span>
            <span className="text-[11px] whitespace-nowrap" style={{ opacity: 0.55 }}>Reviewer-style critique</span>
          </button>
        </div>
      </div>

      {/* Issues list */}
      <div className="flex-1 overflow-y-auto px-4 pt-4 pb-4 space-y-3">
        {filteredIssues.length === 0 ? (
          <div className="text-center py-8" style={{ color: theme.text.muted }}>
            No issues found in this track
          </div>
        ) : (
          filteredIssues.map(issue => {
            const isDismissed = dismissedIssues.has(issue.id);
            const trackColor = getTrackColor(issue.track);
            const severityColor = getSeverityColor(issue.severity);

            return (
              <div
                key={issue.id}
                onClick={() => handleIssueClick(issue)}
                className="relative rounded-lg cursor-pointer transition-all overflow-hidden"
                style={{
                  opacity: isDismissed ? 0.4 : 1,
                  backgroundColor: selectedIssue?.id === issue.id ? withOpacity(theme.action.primary, 0.08) : theme.background.tertiary,
                  border: selectedIssue?.id === issue.id ? `1px solid ${withOpacity(theme.action.primary, 0.5)}` : `1px solid ${theme.border.primary}`,
                  boxShadow: selectedIssue?.id === issue.id ? `0 4px 12px ${withOpacity(theme.action.primary, 0.15)}` : 'none'
                }}
              >
                {/* Left track indicator (2px border) */}
                <div className="absolute left-0 top-0 bottom-0 w-[2px]" style={{ backgroundColor: trackColor }}></div>

                <div className="pl-4 pr-3 py-3">
                  {/* Header row: Track dot + Severity + Dismiss toggle */}
                  <div className="flex items-center gap-2 mb-2">
                    {/* Track indicator dot */}
                    <div
                      className="w-2 h-2 rounded-full"
                      style={{ backgroundColor: trackColor }}
                      title={`Track ${issue.track}`}
                    ></div>

                    {/* Severity badge */}
                    <span
                      className={getSeverityBadgeClass(issue.severity)}
                      style={{
                        backgroundColor: withOpacity(severityColor, 0.15),
                        color: severityColor,
                        borderColor: withOpacity(severityColor, 0.3)
                      }}
                    >
                      {issue.severity}
                    </span>
                    <button
                      onClick={(e) => toggleDismiss(issue.id, e)}
                      className="ml-auto text-gray-500 hover:text-gray-300 transition"
                      title={isDismissed ? "Restore issue" : "Dismiss issue"}
                    >
                      {isDismissed ? (
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                        </svg>
                      ) : (
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                        </svg>
                      )}
                    </button>
                  </div>

                  {/* Title - PROMINENT */}
                  <h3 className="text-[17px] font-semibold mb-2 leading-snug" style={{ color: theme.text.primary }}>
                    {issue.title || issue.message}
                  </h3>

                  {/* Collapsible content - hidden when dismissed */}
                  {!isDismissed && (
                    <>
                      {/* Description - Clear and readable */}
                      {(issue.description || issue.message) && (
                        <p className="text-[13px] leading-relaxed mb-3" style={{ color: theme.text.tertiary, opacity: 0.9 }}>
                          {issue.description || (issue.title ? issue.message : '')}
                        </p>
                      )}

                      {/* Meta info row */}
                      <div className="flex items-center gap-2 text-xs mb-2" style={{ color: theme.text.muted }}>
                        <span className="px-2 py-0.5 rounded" style={{ backgroundColor: theme.background.elevated }}>
                          {issue.issue_type?.replace(/_/g, ' ') || 'general'}
                        </span>
                        {issue.paragraph_id && (
                          <span>• {issue.paragraph_id}</span>
                        )}
                        {issue.section_id && !issue.paragraph_id && (
                          <span>• Section</span>
                        )}
                      </div>

                      {/* Action button */}
                      {renderActionButton(issue)}
                    </>
                  )}
                </div>
              </div>
            );
          })
        )}
      </div>
    </div>
  );
}

export default IssuesPanel;
