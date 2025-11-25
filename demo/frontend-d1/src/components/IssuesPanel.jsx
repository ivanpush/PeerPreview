import React, { useState } from 'react';
import { useManuscript } from '../context/ManuscriptContext';

function IssuesPanel({ onOpenRewriteModal, onOpenOutlineModal, onOpenBiasedReviewModal }) {
  const { issues, setSelectedIssue, selectedIssue, manuscript } = useManuscript();
  const [filterTrack, setFilterTrack] = useState('all');

  const filteredIssues = issues.filter(issue =>
    filterTrack === 'all' || issue.track === filterTrack
  );

  const getSeverityColor = (severity) => {
    switch(severity) {
      case 'major':
      case 'high': return 'bg-red-100 text-red-700 border-red-200';
      case 'minor':
      case 'medium': return 'bg-yellow-100 text-yellow-700 border-yellow-200';
      case 'low': return 'bg-blue-100 text-blue-700 border-blue-200';
      default: return 'bg-gray-100 text-gray-700 border-gray-200';
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
    <div className="h-full flex flex-col bg-gray-50">
      {/* Header with filters */}
      <div className="p-4 bg-white border-b">
        <h2 className="text-xl font-semibold text-gray-800 mb-3">
          Issues ({filteredIssues.length})
        </h2>

        <div className="flex gap-2 flex-wrap">
          <button
            onClick={() => setFilterTrack('all')}
            className={`px-3 py-1 rounded-md text-sm font-medium transition ${
              filterTrack === 'all'
                ? 'bg-gray-800 text-white'
                : 'bg-gray-200 text-gray-600 hover:bg-gray-300'
            }`}
          >
            All
          </button>
          <button
            onClick={() => setFilterTrack('A')}
            className={`px-3 py-1 rounded-md text-sm font-medium transition ${
              filterTrack === 'A'
                ? 'bg-blue-600 text-white'
                : 'bg-gray-200 text-gray-600 hover:bg-gray-300'
            }`}
          >
            Track A
          </button>
          <button
            onClick={() => setFilterTrack('B')}
            className={`px-3 py-1 rounded-md text-sm font-medium transition ${
              filterTrack === 'B'
                ? 'bg-purple-600 text-white'
                : 'bg-gray-200 text-gray-600 hover:bg-gray-300'
            }`}
          >
            Track B
          </button>
          <button
            onClick={() => setFilterTrack('C')}
            className={`px-3 py-1 rounded-md text-sm font-medium transition ${
              filterTrack === 'C'
                ? 'bg-amber-600 text-white'
                : 'bg-gray-200 text-gray-600 hover:bg-gray-300'
            }`}
          >
            Track C
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
          filteredIssues.map(issue => (
            <div
              key={issue.id}
              onClick={() => handleIssueClick(issue)}
              className={`bg-white rounded-lg p-4 border cursor-pointer transition-all ${
                selectedIssue?.id === issue.id
                  ? 'border-blue-500 shadow-md'
                  : 'border-gray-200 hover:shadow-md'
              }`}
            >
              {/* Issue header */}
              <div className="flex items-center gap-2 mb-2">
                <span className={`w-8 h-8 rounded-full flex items-center justify-center text-white text-xs font-bold ${getTrackColor(issue.track)}`}>
                  {issue.track}
                </span>
                <span className={`px-2 py-1 rounded text-xs font-medium border ${getSeverityColor(issue.severity)}`}>
                  {issue.severity}
                </span>
                <span className="text-xs text-gray-500 ml-auto">
                  {issue.issue_type?.replace(/_/g, ' ') || issue.type}
                </span>
              </div>

              {/* Issue message */}
              <p className="text-gray-700 text-sm mb-2 font-medium">
                {issue.title || issue.message}
              </p>

              {/* Description if available */}
              {issue.description && (
                <p className="text-gray-600 text-xs mb-2">
                  {issue.description}
                </p>
              )}

              {/* Location info */}
              {issue.paragraph_id && (
                <p className="text-xs text-gray-500">
                  Paragraph: {issue.paragraph_id}
                </p>
              )}
              {issue.section_id && !issue.paragraph_id && (
                <p className="text-xs text-gray-500">
                  Section: {manuscript?.sections?.find(s => s.section_id === issue.section_id)?.heading || issue.section_id}
                </p>
              )}

              {/* Action button */}
              {renderActionButton(issue)}
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default IssuesPanel;
