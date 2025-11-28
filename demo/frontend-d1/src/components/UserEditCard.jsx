import React, { useState } from 'react';
import * as Diff from 'diff';

function UserEditCard({ edit, onRevert, onNavigate }) {
  const [isExpanded, setIsExpanded] = useState(false);

  // Format timestamp
  const formatTimestamp = (timestamp) => {
    const date = new Date(timestamp);
    const now = new Date();
    const diffInMinutes = Math.floor((now - date) / 60000);

    if (diffInMinutes < 1) return 'just now';
    if (diffInMinutes < 60) return `${diffInMinutes} min ago`;
    if (diffInMinutes < 1440) return `${Math.floor(diffInMinutes / 60)} hours ago`;
    return date.toLocaleDateString();
  };

  // Generate diff
  const renderDiff = () => {
    const diff = Diff.diffWords(edit.originalText, edit.currentText);

    return (
      <div className="p-3 bg-gray-800 rounded-lg overflow-x-auto">
        <div className="text-xs text-gray-500 mb-2">Changes:</div>
        <div className="text-sm leading-relaxed whitespace-pre-wrap text-gray-300">
          {diff.map((part, index) => {
            if (part.added) {
              return (
                <span key={index} className="bg-green-900 bg-opacity-50 text-green-400 px-0.5">
                  {part.value}
                </span>
              );
            }
            if (part.removed) {
              return (
                <span key={index} className="bg-red-900 bg-opacity-50 text-red-400 line-through px-0.5">
                  {part.value}
                </span>
              );
            }
            return <span key={index} className="text-gray-300">{part.value}</span>;
          })}
        </div>
      </div>
    );
  };

  const typeColor = edit.type === 'edited' ? 'bg-yellow-500' : 'bg-red-500';
  const typeLabel = edit.type === 'edited' ? 'EDITED' : 'DELETED';

  const bgColor = edit.type === 'edited'
    ? 'rgba(234, 179, 8, 0.05)'  // Yellow tint with 5% opacity
    : 'rgba(220, 38, 38, 0.05)'; // Red tint with 5% opacity

  const borderColor = edit.type === 'edited'
    ? 'rgba(234, 179, 8, 0.3)'
    : 'rgba(220, 38, 38, 0.3)';

  return (
    <div
      className="relative rounded cursor-pointer transition-all overflow-hidden"
      onClick={() => onNavigate && onNavigate(edit.paragraphId)}
      style={{
        opacity: 0.9,
        backgroundColor: bgColor,
        border: `1px solid ${borderColor}`
      }}>
      {/* Left indicator for edit type */}
      <div className="absolute left-0 top-0 bottom-0 w-[2px]" style={{ backgroundColor: typeColor === 'bg-yellow-500' ? '#EAB308' : '#DC2626' }}></div>

      {/* Collapsed view */}
      <div className="pl-3 pr-2 py-2">
        <div className="flex items-center gap-2">
          {/* Type dot */}
          <div
            className="w-1.5 h-1.5 rounded-full flex-shrink-0"
            style={{ backgroundColor: typeColor === 'bg-yellow-500' ? '#EAB308' : '#DC2626' }}
          ></div>

          {/* Type badge FIRST */}
          <span
            className="px-1.5 py-0.5 rounded text-[10px] font-medium border flex-shrink-0"
            style={{
              backgroundColor: typeColor === 'bg-yellow-500' ? 'rgba(234, 179, 8, 0.15)' : 'rgba(220, 38, 38, 0.15)',
              color: typeColor === 'bg-yellow-500' ? '#EAB308' : '#DC2626',
              borderColor: typeColor === 'bg-yellow-500' ? 'rgba(234, 179, 8, 0.3)' : 'rgba(220, 38, 38, 0.3)'
            }}
          >
            {typeLabel}
          </span>

          {/* Section and paragraph */}
          <span className="text-[10px] text-gray-500 flex-shrink-0">
            {edit.sectionName}
          </span>

          <span className="text-[10px] text-gray-500 flex-shrink-0">
            ¶{edit.paragraphNumber}
          </span>

          {/* Preview text - truncated */}
          <span className="text-[12px] flex-1 truncate text-gray-300">
            {edit.type === 'deleted' ? (
              <span className="line-through text-gray-500">
                {edit.originalText}
              </span>
            ) : (
              <span>
                {edit.currentText}
              </span>
            )}
          </span>

          {/* Timestamp */}
          <span className="text-[9px] text-gray-500 flex-shrink-0">
            {formatTimestamp(edit.timestamp)}
          </span>

          {/* Expand button */}
          <button
            onClick={(e) => {
              e.stopPropagation();
              setIsExpanded(!isExpanded);
            }}
            className="text-gray-400 hover:text-white transition flex-shrink-0 p-1"
          >
            <svg
              className={`w-3 h-3 transform transition-transform ${isExpanded ? 'rotate-180' : ''}`}
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
            </svg>
          </button>
        </div>
      </div>

      {/* Expanded Content */}
      {isExpanded && (
        <div className="px-3 pb-3 mt-2">
          {/* Content Display - Always show diff for edited, original for deleted */}
          {edit.type === 'edited' ? (
            renderDiff()
          ) : (
            <div className="p-2 bg-gray-800 rounded">
              <div className="text-xs text-gray-500 mb-1">Deleted Text:</div>
              <div className="text-sm text-gray-500 line-through leading-relaxed">
                {edit.originalText}
              </div>
            </div>
          )}

          {/* Actions */}
          <div className="mt-3 flex justify-end">
            <button
              onClick={(e) => {
                e.stopPropagation();
                onRevert(edit.paragraphId);
              }}
              className="px-3 py-1 bg-gray-700 hover:bg-gray-600 text-white text-xs rounded transition"
            >
              Revert to Original
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default UserEditCard;