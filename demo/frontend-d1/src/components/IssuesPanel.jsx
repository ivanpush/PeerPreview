import React, { useState } from 'react';
import { useManuscript } from '../context/ManuscriptContext';

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

  const getSeverityColor = (severity) => {
    switch(severity) {
      case 'major':
      case 'high': return 'bg-red-950/30 text-red-400 border-red-900/50';
      case 'minor':
      case 'medium': return 'bg-amber-950/30 text-amber-400 border-amber-900/50';
      case 'low': return 'bg-blue-950/30 text-blue-400 border-blue-900/50';
      default: return 'bg-gray-800 text-gray-400 border-gray-700';
    }
  };

  const getSeverityBarColor = (severity) => {
    switch(severity) {
      case 'major':
      case 'high': return 'bg-red-600';
      case 'minor':
      case 'medium': return 'bg-amber-500';
      case 'low': return 'bg-blue-500';
      default: return 'bg-gray-600';
    }
  };

  const getTrackColor = (track) => {
    switch(track) {
      case 'A': return 'bg-blue-500';
      case 'B': return 'bg-purple-500';
      case 'C': return 'bg-amber-500';
      default: return 'bg-gray-500';
    }
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
    if (issue.issue_type === 'paragraph_rewrite' || issue.suggested_rewrite) {
      return (
        <button
          onClick={(e) => {
            e.stopPropagation();
            onOpenRewriteModal(issue);
          }}
          className="mt-3 px-4 py-2 bg-blue-600 text-white text-sm rounded-md hover:bg-blue-700 transition w-full"
        >
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
          className="mt-3 px-4 py-2 bg-purple-600 text-white text-sm rounded-md hover:bg-purple-700 transition w-full"
        >
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
          className="mt-3 px-4 py-2 bg-amber-600 text-white text-sm rounded-md hover:bg-amber-700 transition w-full"
        >
          View Review
        </button>
      );
    }

    return null;
  };

  return (
    <div className="h-full flex flex-col bg-[#1D1D1D]">
      {/* Header with filters */}
      <div className="p-4 bg-[#232323] border-b border-[#2E2E2E]">
        <h2 className="text-base font-semibold text-gray-200 mb-4">
          Issues ({filteredIssues.length})
        </h2>

        <div className="flex gap-1">
          <button
            onClick={() => setFilterTrack('all')}
            className={`relative px-3 py-1.5 rounded text-xs font-medium transition ${
              filterTrack === 'all'
                ? 'bg-[#2A2A2A] text-white'
                : 'bg-transparent text-gray-400 hover:text-gray-200'
            }`}
          >
            All
            {filterTrack === 'all' && (
              <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-gray-400 rounded-full"></div>
            )}
          </button>
          <button
            onClick={() => setFilterTrack('A')}
            className={`relative px-3 py-1.5 rounded text-xs font-medium transition ${
              filterTrack === 'A'
                ? 'bg-blue-500/20 text-blue-400'
                : 'bg-transparent text-gray-400 hover:text-gray-200'
            }`}
          >
            Track A
            {filterTrack === 'A' && (
              <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-blue-500 rounded-full"></div>
            )}
          </button>
          <button
            onClick={() => setFilterTrack('B')}
            className={`relative px-3 py-1.5 rounded text-xs font-medium transition ${
              filterTrack === 'B'
                ? 'bg-purple-500/20 text-purple-400'
                : 'bg-transparent text-gray-400 hover:text-gray-200'
            }`}
          >
            Track B
            {filterTrack === 'B' && (
              <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-purple-500 rounded-full"></div>
            )}
          </button>
          <button
            onClick={() => setFilterTrack('C')}
            className={`relative px-3 py-1.5 rounded text-xs font-medium transition ${
              filterTrack === 'C'
                ? 'bg-amber-500/20 text-amber-400'
                : 'bg-transparent text-gray-400 hover:text-gray-200'
            }`}
          >
            Track C
            {filterTrack === 'C' && (
              <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-amber-500 rounded-full"></div>
            )}
          </button>
        </div>
      </div>

      {/* Issues list */}
      <div className="flex-1 overflow-y-auto p-4 space-y-3">
        {filteredIssues.length === 0 ? (
          <div className="text-center py-8 text-gray-500">
            No issues found in this track
          </div>
        ) : (
          filteredIssues.map(issue => {
            const isDismissed = dismissedIssues.has(issue.id);

            return (
              <div
                key={issue.id}
                onClick={() => handleIssueClick(issue)}
                className={`relative bg-[#252525] rounded-lg border cursor-pointer transition-all overflow-hidden ${
                  isDismissed ? 'opacity-40' : ''
                } ${
                  selectedIssue?.id === issue.id
                    ? 'border-blue-500/50 shadow-lg shadow-blue-500/10'
                    : 'border-[#2E2E2E] hover:border-gray-600'
                }`}
              >
                {/* Left severity bar */}
                <div className={`absolute left-0 top-0 bottom-0 w-1 ${getSeverityBarColor(issue.severity)}`}></div>

                <div className="pl-4 pr-3 py-3">
                  {/* Header row: Track badge + Severity + Dismiss toggle */}
                  <div className="flex items-center gap-2 mb-2">
                    <span className={`w-6 h-6 rounded-full flex items-center justify-center text-white text-xs font-bold ${getTrackColor(issue.track)}`}>
                      {issue.track}
                    </span>
                    <span className={`px-2 py-0.5 rounded text-xs font-medium border ${getSeverityColor(issue.severity)}`}>
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
                  <h3 className="text-[15px] font-semibold text-gray-100 mb-2 leading-snug">
                    {issue.title || issue.message}
                  </h3>

                  {/* Description - Clear and readable */}
                  {(issue.description || issue.message) && (
                    <p className="text-[13px] text-gray-400 leading-relaxed mb-3 opacity-90">
                      {issue.description || (issue.title ? issue.message : '')}
                    </p>
                  )}

                  {/* Meta info row */}
                  <div className="flex items-center gap-2 text-xs text-gray-500 mb-2">
                    <span className="px-2 py-0.5 bg-gray-800 rounded">
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
    </div>
  );
}

export default IssuesPanel;
