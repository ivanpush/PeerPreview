import React, { useState } from 'react';
import { useManuscript } from '../context/ManuscriptContext';
import { theme, getTrackColor } from '../styles/theme';

function RewriteModal({ issue, onClose }) {
  const { manuscript, updateParagraph } = useManuscript();
  const [editedText, setEditedText] = useState(issue.suggested_rewrite || '');

  if (!issue) return null;

  const paragraph = manuscript?.paragraphs?.find(p => p.paragraph_id === issue.paragraph_id);
  const originalText = paragraph?.text || '';

  // Get track name
  const trackNames = {
    'A': 'Rigor',
    'B': 'Clarity',
    'C': 'Counterpoint'
  };
  const trackName = trackNames[issue.track] || 'Track ' + issue.track;
  const trackColor = getTrackColor(issue.track);

  const handleAccept = () => {
    updateParagraph(issue.paragraph_id, editedText, true); // Pass flag indicating this is a rewrite
    onClose();
  };

  return (
    <div
      className="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center z-50 p-4"
      onClick={onClose}
    >
      <div
        className="rounded-xl shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-hidden flex flex-col"
        style={{
          backgroundColor: '#1A1A1A',
          border: '1px solid rgba(255,255,255,0.07)'
        }}
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div
          className="px-6 py-5 flex items-center justify-between"
          style={{ borderBottom: '1px solid rgba(255,255,255,0.08)' }}
        >
          <div>
            <h2 className="text-[18px] font-semibold text-white">
              Suggested Rewrite — <span style={{ color: trackColor }}>{trackName}</span>
            </h2>
            <p className="text-[14px] text-white mt-1" style={{ opacity: 0.6 }}>
              {issue.title || issue.message}
            </p>
          </div>
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-300 transition"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto" style={{ padding: '24px' }}>
          {/* Original text */}
          <div className="mb-6">
            <h3 className="text-[15px] font-semibold text-white mb-3 flex items-center gap-2">
              <svg className="w-5 h-5" style={{ color: theme.severity.major }} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
              Original Text
            </h3>
            <div
              className="rounded-lg"
              style={{
                backgroundColor: 'rgba(229,72,77,0.10)',
                border: '1px solid rgba(229,72,77,0.25)',
                padding: '16px 18px'
              }}
            >
              <p className="text-[14px] text-gray-200 leading-relaxed">
                {originalText}
              </p>
            </div>
          </div>

          {/* Suggested rewrite - editable */}
          <div className="mb-6">
            <h3 className="text-[15px] font-semibold text-white mb-3 flex items-center gap-2">
              <svg className="w-5 h-5" style={{ color: theme.track.counterpoint }} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
              Suggested Rewrite
              <span className="text-xs text-gray-500 font-normal ml-2">(editable)</span>
            </h3>
            <div
              className="rounded-lg"
              style={{
                backgroundColor: 'rgba(58,168,160,0.12)',
                border: '1px solid rgba(58,168,160,0.25)',
                padding: '16px 18px'
              }}
            >
              <textarea
                value={editedText}
                onChange={(e) => setEditedText(e.target.value)}
                className="w-full text-[14px] text-gray-200 leading-relaxed bg-transparent resize-y min-h-[120px] focus:outline-none"
                style={{
                  border: 'none',
                  padding: '8px',
                  borderRadius: '6px'
                }}
                onFocus={(e) => {
                  e.target.style.border = `2px solid ${theme.action.primary}`;
                  e.target.style.padding = '7px';
                }}
                onBlur={(e) => {
                  e.target.style.border = 'none';
                  e.target.style.padding = '8px';
                }}
                rows={6}
              />
            </div>
          </div>

          {/* Rationale if available */}
          {issue.rationale && (
            <div>
              <div
                className="rounded-lg"
                style={{
                  backgroundColor: 'rgba(255,255,255,0.04)',
                  border: '1px solid rgba(255,255,255,0.06)',
                  padding: '14px 18px'
                }}
              >
                <h3 className="text-[12px] font-semibold text-white uppercase tracking-wide mb-2" style={{ opacity: 0.65 }}>
                  Rationale
                </h3>
                <p className="text-[14px] text-gray-300 leading-relaxed">
                  {issue.rationale}
                </p>
              </div>
            </div>
          )}
        </div>

        {/* Footer */}
        <div
          className="px-6 py-4 flex items-center justify-end gap-3"
          style={{ borderTop: '1px solid rgba(255,255,255,0.08)' }}
        >
          <button
            onClick={onClose}
            className="px-5 py-2 text-white hover:opacity-80 transition"
            style={{
              backgroundColor: theme.action.secondary,
              borderRadius: '6px'
            }}
          >
            Dismiss
          </button>
          <button
            onClick={handleAccept}
            className="px-5 py-2 text-white hover:opacity-90 transition shadow-lg"
            style={{
              backgroundColor: theme.action.primary,
              borderRadius: '6px'
            }}
          >
            Accept Rewrite
          </button>
        </div>
      </div>
    </div>
  );
}

export default RewriteModal;
