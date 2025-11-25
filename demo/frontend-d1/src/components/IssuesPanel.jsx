import React, { useState } from 'react';
import { useManuscript } from '../context/ManuscriptContext';
import { theme, withOpacity, getTrackColor, getSeverityColor } from '../styles/theme';

function IssuesPanel({ onOpenRewriteModal, onOpenOutlineModal, onOpenBiasedReviewModal }) {
  const { issues, setSelectedIssue, selectedIssue, manuscript } = useManuscript();
  const [filterTrack, setFilterTrack] = useState('all');
  const [dismissedIssues, setDismissedIssues] = useState(new Set());
  const [expandedDismissed, setExpandedDismissed] = useState(new Set());

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
    // Toggle selection - if already selected, deselect
    if (selectedIssue?.id === issue.id) {
      setSelectedIssue(null);
    } else {
      setSelectedIssue(issue);

      // Scroll based on issue type
      if (issue.paragraph_id) {
        // ManuscriptView will handle scrolling via useEffect
      } else if (issue.section_id) {
        const section = document.getElementById(issue.section_id);
        section?.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    }
  };

  const renderActionButton = (issue) => {
    const buttonStyle = {
      backgroundColor: 'rgba(91, 174, 184, 0.12)',
      color: '#5BAEB8',
      border: '1px solid rgba(91, 174, 184, 0.3)'
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
    <div className="h-full flex flex-col">
      {/* Header with filters - compact single row */}
      <div className="py-2.5 px-6 flex items-center justify-between gap-3" style={{ backgroundColor: theme.background.secondary, borderBottom: `1px solid ${theme.border.primary}` }}>
        <div className="flex gap-2">
          {/* All Tab */}
          <button
            onClick={() => setFilterTrack('all')}
            className="relative px-3 py-1.5 rounded text-xs font-medium transition flex items-center"
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
            className="relative px-3 py-1.5 rounded text-xs font-medium transition flex items-center"
            style={{
              backgroundColor: filterTrack === 'A' ? withOpacity(theme.track.rigor, 0.15) : 'transparent',
              color: filterTrack === 'A' ? theme.track.rigor : theme.text.tertiary,
              border: filterTrack === 'A' ? `1px solid ${theme.track.rigor}` : '1px solid transparent'
            }}
            onMouseEnter={(e) => {
              if (filterTrack !== 'A') e.currentTarget.style.backgroundColor = 'rgba(62, 99, 221, 0.1)';
            }}
            onMouseLeave={(e) => {
              if (filterTrack !== 'A') e.currentTarget.style.backgroundColor = 'transparent';
            }}
          >
            <span className="font-semibold">Rigor</span>
          </button>

          {/* Clarity Tab */}
          <button
            onClick={() => setFilterTrack('B')}
            className="relative px-3 py-1.5 rounded text-xs font-medium transition flex items-center"
            style={{
              backgroundColor: filterTrack === 'B' ? withOpacity(theme.track.clarity, 0.15) : 'transparent',
              color: filterTrack === 'B' ? theme.track.clarity : theme.text.tertiary,
              border: filterTrack === 'B' ? `1px solid ${theme.track.clarity}` : '1px solid transparent'
            }}
            onMouseEnter={(e) => {
              if (filterTrack !== 'B') e.currentTarget.style.backgroundColor = 'rgba(142, 78, 198, 0.1)';
            }}
            onMouseLeave={(e) => {
              if (filterTrack !== 'B') e.currentTarget.style.backgroundColor = 'transparent';
            }}
          >
            <span className="font-semibold">Clarity</span>
          </button>

          {/* Counterpoint Tab */}
          <button
            onClick={() => setFilterTrack('C')}
            className="relative px-3 py-1.5 rounded text-xs font-medium transition flex items-center"
            style={{
              backgroundColor: filterTrack === 'C' ? withOpacity(theme.track.counterpoint, 0.15) : 'transparent',
              color: filterTrack === 'C' ? theme.track.counterpoint : theme.text.tertiary,
              border: filterTrack === 'C' ? `1px solid ${theme.track.counterpoint}` : '1px solid transparent'
            }}
            onMouseEnter={(e) => {
              if (filterTrack !== 'C') e.currentTarget.style.backgroundColor = 'rgba(199, 138, 42, 0.1)';
            }}
            onMouseLeave={(e) => {
              if (filterTrack !== 'C') e.currentTarget.style.backgroundColor = 'transparent';
            }}
          >
            <span className="font-semibold">Counterpoint</span>
          </button>
        </div>

        {/* Issue count on the right */}
        <span className="text-[11px] font-medium px-2 py-1 rounded" style={{
          backgroundColor: theme.background.elevated,
          color: theme.text.tertiary
        }}>
          {filteredIssues.length}
        </span>
      </div>

      {/* Issues list */}
      <div className="flex-1 overflow-y-auto px-6 pt-4 pb-4">
        {/* Active issues */}
        <div className="space-y-3">
          {filteredIssues.filter(issue => !dismissedIssues.has(issue.id)).length === 0 ? (
            <div className="text-center py-8" style={{ color: theme.text.muted }}>
              No active issues in this track
            </div>
          ) : (
            filteredIssues.filter(issue => !dismissedIssues.has(issue.id)).map(issue => {
              const trackColor = getTrackColor(issue.track);
              const severityColor = getSeverityColor(issue.severity);

              const isSelected = selectedIssue?.id === issue.id;

              return (
                <div
                  key={issue.id}
                  onClick={() => handleIssueClick(issue)}
                  className="relative rounded-lg cursor-pointer transition-all overflow-hidden"
                  style={{
                    backgroundColor: isSelected ? '#1A2E2D' : theme.background.tertiary,
                    border: isSelected ? '2px solid #5BAEB8' : `1px solid ${theme.border.primary}`,
                    boxShadow: isSelected ? '0 0 20px rgba(91, 174, 184, 0.3)' : 'none'
                  }}
                >
                  {/* Left track indicator (2px border) - hide when selected */}
                  {!isSelected && (
                    <div className="absolute left-0 top-0 bottom-0 w-[2px]" style={{ backgroundColor: trackColor }}></div>
                  )}

                  <div className="pl-4 pr-3 py-3">
                    {/* Header row: Track dot + Severity + Dismiss toggle */}
                    <div className="flex items-center gap-2 mb-2">
                      {/* Track indicator dot - hide when selected */}
                      {!isSelected && (
                        <div
                          className="w-2 h-2 rounded-full"
                          style={{ backgroundColor: trackColor }}
                          title={`Track ${issue.track}`}
                        ></div>
                      )}

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
                        title="Dismiss issue"
                      >
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                        </svg>
                      </button>
                    </div>

                    {/* Title - PROMINENT */}
                    <h3 className="text-[17px] font-semibold mb-2 leading-snug" style={{ color: theme.text.primary }}>
                      {issue.title || issue.message}
                    </h3>

                    {/* Description - Clear and readable */}
                    {(issue.description || issue.message) && (
                      <p className="text-[13px] leading-relaxed mb-3" style={{
                        color: isSelected ? '#C8C8C8' : theme.text.tertiary,
                        opacity: 0.9
                      }}>
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
                  </div>
                </div>
              );
            })
          )}
        </div>

        {/* Dismissed issues section */}
        {dismissedIssues.size > 0 && (
          <div className="mt-6 pt-4 border-t" style={{ borderColor: theme.border.primary }}>
            <h3 className="text-[11px] font-semibold mb-2 px-1 uppercase tracking-wide" style={{ color: theme.text.muted }}>
              Dismissed ({dismissedIssues.size})
            </h3>
            <div className="space-y-1.5">
              {filteredIssues.filter(issue => dismissedIssues.has(issue.id)).map(issue => {
                const trackColor = getTrackColor(issue.track);
                const severityColor = getSeverityColor(issue.severity);
                const isExpanded = expandedDismissed.has(issue.id);

                const toggleExpanded = (e) => {
                  e.stopPropagation();
                  setExpandedDismissed(prev => {
                    const newSet = new Set(prev);
                    if (newSet.has(issue.id)) {
                      newSet.delete(issue.id);
                    } else {
                      newSet.add(issue.id);
                    }
                    return newSet;
                  });
                };

                return (
                  <div
                    key={issue.id}
                    className="relative rounded cursor-pointer transition-all overflow-hidden"
                    style={{
                      opacity: 0.5,
                      backgroundColor: theme.background.tertiary,
                      border: `1px solid ${theme.border.primary}`
                    }}
                  >
                    {/* Left track indicator */}
                    <div className="absolute left-0 top-0 bottom-0 w-[2px]" style={{ backgroundColor: trackColor }}></div>

                    {/* Collapsed header row */}
                    <div className="flex items-center gap-2 pl-3 pr-2 py-2" onClick={toggleExpanded}>
                      {/* Expand arrow */}
                      <svg
                        className={`w-3 h-3 transition-transform flex-shrink-0 ${isExpanded ? 'rotate-90' : 'rotate-0'}`}
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                        style={{ color: theme.text.muted }}
                      >
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                      </svg>

                      {/* Track dot */}
                      <div
                        className="w-1.5 h-1.5 rounded-full flex-shrink-0"
                        style={{ backgroundColor: trackColor }}
                      ></div>

                      {/* Severity badge */}
                      <span
                        className="px-1.5 py-0.5 rounded text-[10px] font-medium border flex-shrink-0"
                        style={{
                          backgroundColor: withOpacity(severityColor, 0.15),
                          color: severityColor,
                          borderColor: withOpacity(severityColor, 0.3)
                        }}
                      >
                        {issue.severity}
                      </span>

                      {/* Title - truncated */}
                      <span className="text-[12px] flex-1 truncate" style={{ color: theme.text.tertiary }}>
                        {issue.title || issue.message}
                      </span>

                      {/* Restore button */}
                      <button
                        onClick={(e) => toggleDismiss(issue.id, e)}
                        className="text-[9px] px-1.5 py-0.5 rounded hover:bg-gray-700 transition flex-shrink-0"
                        style={{ color: theme.text.muted }}
                        title="Restore issue"
                      >
                        Undo
                      </button>
                    </div>

                    {/* Expanded content */}
                    {isExpanded && (
                      <div className="px-3 pb-2 pt-1 border-t" style={{ borderColor: theme.border.primary }}>
                        {/* Description */}
                        {(issue.description || issue.message) && (
                          <p className="text-[12px] leading-relaxed mb-2" style={{ color: theme.text.tertiary, opacity: 0.9 }}>
                            {issue.description || (issue.title ? issue.message : '')}
                          </p>
                        )}

                        {/* Meta info row */}
                        <div className="flex items-center gap-2 text-[10px] mb-2" style={{ color: theme.text.muted }}>
                          <span className="px-1.5 py-0.5 rounded" style={{ backgroundColor: theme.background.elevated }}>
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
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default IssuesPanel;
