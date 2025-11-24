import './RewriteModal.css'

function RewriteModal({ issue, onClose, onAccept }) {
  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>AI-Suggested Rewrite</h2>
          <button className="close-btn" onClick={onClose}>✕</button>
        </div>

        <div className="modal-body">
          <div className="comparison">
            <div className="original">
              <h3>Original Text</h3>
              <div className="text-box">{issue.originalText}</div>
            </div>

            <div className="arrow">→</div>

            <div className="rewritten">
              <h3>Suggested Rewrite</h3>
              <div className="text-box rewrite">{issue.suggestedRewrite}</div>
            </div>
          </div>

          <div className="rationale">
            <h4>Why this change?</h4>
            <p>{issue.rationale}</p>
          </div>
        </div>

        <div className="modal-footer">
          <button className="btn-cancel" onClick={onClose}>
            Cancel
          </button>
          <button className="btn-accept" onClick={onAccept}>
            Accept Rewrite
          </button>
        </div>
      </div>
    </div>
  )
}

export default RewriteModal
