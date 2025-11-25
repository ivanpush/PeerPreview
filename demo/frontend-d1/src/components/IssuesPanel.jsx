import React, { useState } from 'react';
import { useManuscript } from '../context/ManuscriptContext';
import { theme, withOpacity, getTrackColor, getSeverityColor } from '../styles/theme';

function IssuesPanel({ onOpenRewriteModal, onOpenOutlineModal, onOpenBiasedReviewModal, onSelectIssue }) {
  const { issues, setSelectedIssue, selectedIssue, manuscript, updateParagraph, dismissedIssues, setDismissedIssues } = useManuscript();
  const [filterTrack, setFilterTrack] = useState('all');
  const [expandedIssues, setExpandedIssues] = useState(new Set());

  const filteredIssues = issues.filter(issue =>
    filterTrack === 'all' || issue.track === filterTrack
  );

  const toggleDismiss = (issueId, e) => {
    e?.stopPropagation();

    // If dismissing the currently selected issue, unselect it
    if (selectedIssue?.id === issueId) {
      setSelectedIssue(null);
    }

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

  const toggleExpanded = (issueId, e) => {
    e?.stopPropagation();
    setExpandedIssues(prev => {
      const newSet = new Set(prev);
      if (newSet.has(issueId)) {
        newSet.delete(issueId);
      } else {
        newSet.add(issueId);
      }
      return newSet;
    });
  };

  // Helper: Generate rationale preview (first 120 chars)
  const getRationalePreview = (rationale) => {
    if (!rationale) return '';
    return rationale.length > 120 ? rationale.slice(0, 120) + '…' : rationale;
  };

  // Helper: Generate rewrite preview (first ~180 chars or 2-4 lines)
  const getRewritePreview = (text) => {
    if (!text) return '';
    return text.length > 180 ? text.slice(0, 180) + '…' : text;
  };

  // Helper: Generate outline preview (first 2-3 items)
  const getOutlinePreview = (outlineArray) => {
    if (!outlineArray || !Array.isArray(outlineArray)) return '';
    const preview = outlineArray.slice(0, 2).join('\n');
    return outlineArray.length > 2 ? preview + '\n...' : preview;
  };

  // Helper: Get quoted excerpt from paragraph
  const getQuotedExcerpt = (issue) => {
    if (issue.original_text) {
      return issue.original_text;
    }
    if (issue.paragraph_id && manuscript?.paragraphs) {
      const para = manuscript.paragraphs.find(p => p.paragraph_id === issue.paragraph_id);
      if (para?.text) {
        // Return first ~2 sentences (~200 chars)
        const sentences = para.text.split(/\.\s+/).slice(0, 2);
        return sentences.join('. ') + (sentences.length > 0 ? '.' : '');
      }
    }
    return '';
  };

  // Helper: Get track name
  const getTrackName = (track) => {
    const names = { 'A': 'Rigor', 'B': 'Clarity', 'C': 'Counterpoint' };
    return names[track] || 'Track ' + track;
  };

  const handleIssueClick = (issue) => {
    // Toggle selection
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

  // Expose selectIssue function to parent for flag clicks
  React.useEffect(() => {
    if (onSelectIssue) {
      onSelectIssue.current = (issue) => {
        // Switch to appropriate track tab
        setFilterTrack(issue.track);
        // Select the issue
        setSelectedIssue(issue);
        // Expand if collapsed
        setExpandedIssues(prev => new Set(prev).add(issue.id));
        // Scroll to issue in sidebar after a brief delay for tab switch
        setTimeout(() => {
          const issueElement = document.querySelector(`[data-issue-id="${issue.id}"]`);
          if (issueElement) {
            issueElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
          }
        }, 100);
      };
    }
  }, [onSelectIssue, setSelectedIssue, setFilterTrack]);

  const handleAcceptRewrite = (issue, e) => {
    e?.stopPropagation();
    if (!issue.suggested_rewrite || !issue.paragraph_id) return;

    const paragraph = manuscript?.paragraphs?.find(p => p.paragraph_id === issue.paragraph_id);
    if (!paragraph) return;

    const isSentenceLevel = issue.sentence_ids && issue.sentence_ids.length > 0;

    if (isSentenceLevel && paragraph.sentences) {
      const sentenceId = issue.sentence_ids[0];
      const textToReplace = issue.original_text ||
        paragraph.sentences.find(s => s.sentence_id === sentenceId)?.text;

      if (textToReplace && paragraph.text.includes(textToReplace)) {
        const updatedText = paragraph.text.replace(textToReplace, issue.suggested_rewrite);
        updateParagraph(issue.paragraph_id, updatedText, true);
      } else {
        updateParagraph(issue.paragraph_id, issue.suggested_rewrite, true);
      }
    } else {
      updateParagraph(issue.paragraph_id, issue.suggested_rewrite, true);
    }

    // Dismiss the issue after accepting
    toggleDismiss(issue.id);
  };

  // Render collapsed issue card
  const renderCollapsedCard = (issue) => {
    const trackColor = getTrackColor(issue.track);
    const severityColor = getSeverityColor(issue.severity);
    const isSelected = selectedIssue?.id === issue.id;
    const rationalePreview = getRationalePreview(issue.rationale);

    return (
      <div
        key={issue.id}
        data-issue-id={issue.id}
        onClick={() => handleIssueClick(issue)}
        className="relative rounded-lg cursor-pointer transition-all overflow-hidden"
        style={{
          backgroundColor: isSelected ? '#1A2E2D' : theme.background.tertiary,
          border: isSelected ? '2px solid #5BAEB8' : `1px solid ${theme.border.primary}`,
          boxShadow: isSelected ? '0 0 20px rgba(91, 174, 184, 0.3)' : 'none'
        }}
      >
        {/* Left track indicator */}
        {!isSelected && (
          <div className="absolute left-0 top-0 bottom-0 w-[3px]" style={{ backgroundColor: trackColor }}></div>
        )}

        <div className="pl-4 pr-3 py-3">
          {/* Header row: Track dot + Severity badge + Dismiss */}
          <div className="flex items-center gap-2 mb-2">
            {!isSelected && (
              <div
                className="w-2 h-2 rounded-full"
                style={{ backgroundColor: trackColor }}
                title={getTrackName(issue.track)}
              ></div>
            )}

            <span
              className="px-2 py-0.5 rounded text-xs font-medium border"
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

          {/* Title */}
          <h3
            className="text-[15px] font-semibold mb-2 leading-snug"
            style={{ color: theme.text.primary }}
          >
            {issue.title || issue.message}
          </h3>

          {/* Section/Figure pills */}
          <div className="flex items-center gap-2 mb-2">
            {issue.section_id && (
              <span
                className="px-2 py-0.5 rounded text-[11px] font-medium"
                style={{
                  backgroundColor: withOpacity(theme.accent.uiBlue, 0.15),
                  color: theme.accent.uiBlue,
                  border: `1px solid ${withOpacity(theme.accent.uiBlue, 0.3)}`
                }}
              >
                {issue.section_id.replace('sec_', '')}
              </span>
            )}
            {issue.paragraph_id && (
              <span
                className="px-2 py-0.5 rounded text-[11px] font-medium"
                style={{
                  backgroundColor: withOpacity(theme.accent.uiBlue, 0.15),
                  color: theme.accent.uiBlue,
                  border: `1px solid ${withOpacity(theme.accent.uiBlue, 0.3)}`
                }}
              >
                {issue.paragraph_id}
              </span>
            )}
          </div>

          {/* Rationale preview (1 line, 120 chars) */}
          {rationalePreview && (
            <p
              className="text-[13px] leading-relaxed mb-3"
              style={{ color: theme.text.tertiary, opacity: 0.85 }}
            >
              {rationalePreview}
            </p>
          )}

          {/* Chevron to expand */}
          <button
            onClick={(e) => toggleExpanded(issue.id, e)}
            className="flex items-center gap-1 text-xs hover:opacity-70 transition mt-2"
            style={{ color: theme.accent.teal }}
          >
            <span>See details</span>
            <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
            </svg>
          </button>
        </div>
      </div>
    );
  };

  // Render expanded issue card
  const renderExpandedCard = (issue) => {
    const trackColor = getTrackColor(issue.track);
    const severityColor = getSeverityColor(issue.severity);
    const isSelected = selectedIssue?.id === issue.id;
    const quotedExcerpt = getQuotedExcerpt(issue);
    const rewritePreview = getRewritePreview(issue.suggested_rewrite);

    return (
      <div
        key={issue.id}
        data-issue-id={issue.id}
        onClick={() => handleIssueClick(issue)}
        className="relative rounded-lg transition-all overflow-hidden cursor-pointer"
        style={{
          backgroundColor: isSelected ? '#1A2E2D' : theme.background.tertiary,
          border: isSelected ? '2px solid #5BAEB8' : `1px solid ${theme.border.primary}`,
          boxShadow: isSelected ? '0 0 20px rgba(91, 174, 184, 0.3)' : 'none'
        }}
      >
        {/* Left track indicator */}
        {!isSelected && (
          <div className="absolute left-0 top-0 bottom-0 w-[3px]" style={{ backgroundColor: trackColor }}></div>
        )}

        <div className="pl-4 pr-3 py-3">
          {/* Header row */}
          <div className="flex items-center gap-2 mb-2">
            {!isSelected && (
              <div
                className="w-2 h-2 rounded-full"
                style={{ backgroundColor: trackColor }}
                title={getTrackName(issue.track)}
              ></div>
            )}

            <span
              className="px-2 py-0.5 rounded text-xs font-medium border"
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

          {/* Title */}
          <h3
            className="text-[15px] font-semibold mb-2 leading-snug"
            style={{ color: theme.text.primary }}
          >
            {issue.title || issue.message}
          </h3>

          {/* Section/Figure pills */}
          <div className="flex items-center gap-2 mb-3">
            {issue.section_id && (
              <span
                className="px-2 py-0.5 rounded text-[11px] font-medium"
                style={{
                  backgroundColor: withOpacity(theme.accent.uiBlue, 0.15),
                  color: theme.accent.uiBlue,
                  border: `1px solid ${withOpacity(theme.accent.uiBlue, 0.3)}`
                }}
              >
                {issue.section_id.replace('sec_', '')}
              </span>
            )}
            {issue.paragraph_id && (
              <span
                className="px-2 py-0.5 rounded text-[11px] font-medium"
                style={{
                  backgroundColor: withOpacity(theme.accent.uiBlue, 0.15),
                  color: theme.accent.uiBlue,
                  border: `1px solid ${withOpacity(theme.accent.uiBlue, 0.3)}`
                }}
              >
                {issue.paragraph_id}
              </span>
            )}
          </div>

          {/* Quoted excerpt */}
          {quotedExcerpt && (
            <div
              className="mb-3 pl-3 border-l-2 py-1"
              style={{
                borderColor: withOpacity(trackColor, 0.4),
                backgroundColor: withOpacity(trackColor, 0.05)
              }}
            >
              <p className="text-[13px] italic leading-relaxed" style={{ color: theme.text.secondary }}>
                "{quotedExcerpt}"
              </p>
            </div>
          )}

          {/* Full rationale */}
          {issue.rationale && (
            <div className="mb-3">
              <p className="text-[13px] leading-relaxed" style={{ color: theme.text.tertiary }}>
                {issue.rationale}
              </p>
            </div>
          )}

          {/* Rewrite preview (if available) */}
          {issue.suggested_rewrite && (
            <div
              className="mb-3 rounded p-2"
              style={{
                backgroundColor: withOpacity(theme.accent.teal, 0.08),
                border: `1px solid ${withOpacity(theme.accent.teal, 0.2)}`
              }}
            >
              <div className="text-[11px] font-semibold mb-1 uppercase tracking-wide" style={{ color: theme.accent.teal }}>
                Suggested Rewrite
              </div>
              <p className="text-[13px] leading-relaxed" style={{ color: theme.text.secondary }}>
                {rewritePreview}
              </p>
            </div>
          )}

          {/* Outline preview (if available) */}
          {issue.issue_type === 'section_outline' && issue.outline_suggestion && (
            <div
              className="mb-3 rounded p-3"
              style={{
                backgroundColor: withOpacity(theme.accent.teal, 0.08),
                border: `1px solid ${withOpacity(theme.accent.teal, 0.2)}`
              }}
            >
              <div className="text-[11px] font-semibold mb-2 uppercase tracking-wide" style={{ color: theme.accent.teal }}>
                Suggested Outline
              </div>
              <ol className="text-[13px] leading-relaxed space-y-1" style={{ color: theme.text.secondary, paddingLeft: '20px' }}>
                {issue.outline_suggestion.map((item, idx) => (
                  <li key={idx} className="list-decimal">{item}</li>
                ))}
              </ol>
            </div>
          )}

          {/* Action buttons */}
          <div className="flex items-center gap-2">
            {/* Paragraph rewrite actions */}
            {issue.suggested_rewrite && (
              <>
                <button
                  onClick={(e) => handleAcceptRewrite(issue, e)}
                  className="px-3 py-1.5 text-xs rounded font-medium hover:opacity-90 transition"
                  style={{
                    backgroundColor: theme.action.primary,
                    color: 'white'
                  }}
                >
                  Accept Rewrite
                </button>
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    onOpenRewriteModal(issue);
                  }}
                  className="px-3 py-1.5 text-xs rounded font-medium hover:opacity-80 transition"
                  style={{
                    backgroundColor: withOpacity(theme.accent.teal, 0.12),
                    color: theme.accent.teal,
                    border: `1px solid ${withOpacity(theme.accent.teal, 0.3)}`
                  }}
                >
                  Edit
                </button>
              </>
            )}

            {/* Section outline action */}
            {issue.issue_type === 'section_outline' && issue.outline_suggestion && (
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  onOpenOutlineModal(issue);
                }}
                className="px-3 py-1.5 text-xs rounded font-medium hover:opacity-90 transition"
                style={{
                  backgroundColor: theme.action.primary,
                  color: 'white'
                }}
              >
                View Outline
              </button>
            )}

            {/* Counterpoint/biased review action */}
            {issue.track === 'C' && issue.issue_type === 'biased_critique' && (
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  onOpenBiasedReviewModal(issue);
                }}
                className="px-3 py-1.5 text-xs rounded font-medium hover:opacity-90 transition"
                style={{
                  backgroundColor: theme.action.primary,
                  color: 'white'
                }}
              >
                View Review
              </button>
            )}

            <button
              onClick={(e) => toggleDismiss(issue.id, e)}
              className="px-3 py-1.5 text-xs rounded font-medium hover:opacity-80 transition ml-auto"
              style={{
                backgroundColor: 'rgba(255, 255, 255, 0.05)',
                color: theme.text.tertiary,
                border: `1px solid ${theme.border.primary}`
              }}
            >
              Dismiss
            </button>
          </div>

          {/* Chevron to collapse */}
          <button
            onClick={(e) => toggleExpanded(issue.id, e)}
            className="flex items-center gap-1 text-xs hover:opacity-70 transition mt-3"
            style={{ color: theme.text.muted }}
          >
            <span>Show less</span>
            <svg className="w-3 h-3 rotate-180" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
            </svg>
          </button>
        </div>
      </div>
    );
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
              const isExpanded = expandedIssues.has(issue.id);
              return isExpanded ? renderExpandedCard(issue) : renderCollapsedCard(issue);
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
                    <div className="flex items-center gap-2 pl-3 pr-2 py-2">
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
