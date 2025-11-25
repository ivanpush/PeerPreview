import React, { useState } from 'react';
import { useManuscript } from '../context/ManuscriptContext';
import { theme, getTrackColor } from '../styles/theme';

function RewriteModal({ issue, onClose }) {
  const { manuscript, updateParagraph } = useManuscript();

  if (!issue) return null;

  const paragraph = manuscript?.paragraphs?.find(p => p.paragraph_id === issue.paragraph_id);
  const originalText = paragraph?.text || '';

  // Check if this is a sentence-level issue
  const isSentenceLevel = issue.sentence_ids && issue.sentence_ids.length > 0;

  // Get the original sentence text if sentence-level
  const getOriginalSentenceText = () => {
    if (!isSentenceLevel || !paragraph?.sentences) return '';
    const sentenceId = issue.sentence_ids[0]; // Get first affected sentence
    const sentence = paragraph.sentences.find(s => s.sentence_id === sentenceId);
    return sentence?.text || '';
  };

  // Initialize edited text with suggested rewrite
  const [editedText, setEditedText] = useState(issue.suggested_rewrite || '');

  // For display: show original sentence if sentence-level, otherwise full paragraph
  const displayOriginalText = isSentenceLevel ? getOriginalSentenceText() : originalText;

  // Get track name
  const trackNames = {
    'A': 'Rigor',
    'B': 'Clarity',
    'C': 'Counterpoint'
  };
  const trackName = trackNames[issue.track] || 'Track ' + issue.track;
  const trackColor = getTrackColor(issue.track);

  const handleAccept = () => {
    if (isSentenceLevel && paragraph?.sentences) {
      // Replace only the affected sentence in the paragraph
      const sentenceId = issue.sentence_ids[0];
      const originalSentence = paragraph.sentences.find(s => s.sentence_id === sentenceId);

      if (originalSentence) {
        // Use the original_text from issue if available (more reliable than sentence.text)
        const textToReplace = issue.original_text || originalSentence.text;

        // Check if the text exists in the paragraph
        if (originalText.includes(textToReplace)) {
          const updatedParagraphText = originalText.replace(textToReplace, editedText);
          updateParagraph(issue.paragraph_id, updatedParagraphText, true);
        } else {
          // Fallback: if exact match fails, replace the whole paragraph
          console.warn('Sentence text not found in paragraph, using full paragraph replacement');
          updateParagraph(issue.paragraph_id, editedText, true);
        }
      }
    } else {
      // Full paragraph rewrite
      updateParagraph(issue.paragraph_id, editedText, true);
    }
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
              {issue.severity && (
                <span
                  className="ml-3 px-2 py-0.5 rounded text-xs font-medium border"
                  style={{
                    backgroundColor: `rgba(${issue.severity === 'major' ? '229,72,77' : '255,190,60'},0.15)`,
                    color: issue.severity === 'major' ? '#E5484D' : '#FFBE3C',
                    borderColor: `rgba(${issue.severity === 'major' ? '229,72,77' : '255,190,60'},0.3)`
                  }}
                >
                  {issue.severity}
                </span>
              )}
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
          {/* Original text (read-only) */}
          <div className="mb-6">
            <h3 className="text-[13px] font-semibold text-white uppercase tracking-wide mb-3" style={{ opacity: 0.75 }}>
              Original Text
            </h3>
            <div
              className="rounded-lg"
              style={{
                backgroundColor: 'rgba(229,72,77,0.08)',
                border: '1px solid rgba(229,72,77,0.2)',
                padding: '16px 18px'
              }}
            >
              <p className="text-[14px] text-gray-200 leading-relaxed">
                {displayOriginalText}
              </p>
            </div>
          </div>

          {/* Editable rewrite */}
          <div className="mb-6">
            <h3 className="text-[13px] font-semibold text-white uppercase tracking-wide mb-3" style={{ opacity: 0.75 }}>
              Suggested Rewrite <span className="text-xs text-gray-500 font-normal ml-2 normal-case">(editable)</span>
            </h3>
            <div
              className="rounded-lg"
              style={{
                backgroundColor: 'rgba(91,174,184,0.10)',
                border: '1px solid rgba(91,174,184,0.25)',
                padding: '4px'
              }}
            >
              <textarea
                value={editedText}
                onChange={(e) => setEditedText(e.target.value)}
                className="w-full text-[14px] text-gray-200 leading-relaxed bg-transparent resize-y min-h-[120px] focus:outline-none"
                style={{
                  border: 'none',
                  padding: '12px 14px',
                  borderRadius: '6px'
                }}
                onFocus={(e) => {
                  e.target.style.border = `2px solid #5BAEB8`;
                  e.target.style.padding = '11px 13px';
                }}
                onBlur={(e) => {
                  e.target.style.border = 'none';
                  e.target.style.padding = '12px 14px';
                }}
                rows={6}
              />
            </div>
          </div>

          {/* Full rationale block at bottom */}
          {issue.rationale && (
            <div>
              <h3 className="text-[13px] font-semibold text-white uppercase tracking-wide mb-3" style={{ opacity: 0.75 }}>
                Rationale
              </h3>
              <div
                className="rounded-lg"
                style={{
                  backgroundColor: 'rgba(255,255,255,0.03)',
                  border: '1px solid rgba(255,255,255,0.08)',
                  padding: '14px 18px'
                }}
              >
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
            className="px-5 py-2 text-white hover:opacity-80 transition font-medium"
            style={{
              backgroundColor: 'rgba(255, 255, 255, 0.08)',
              borderRadius: '6px',
              border: '1px solid rgba(255, 255, 255, 0.12)'
            }}
          >
            Cancel
          </button>
          <button
            onClick={handleAccept}
            className="px-5 py-2 text-white hover:opacity-90 transition shadow-lg font-medium"
            style={{
              backgroundColor: '#5BAEB8',
              borderRadius: '6px'
            }}
          >
            Save
          </button>
        </div>
      </div>
    </div>
  );
}

export default RewriteModal;
