import { useState } from 'react'
import RewriteModal from './RewriteModal'
import './IssuesPanel.css'

function IssuesPanel({ issues, selectedIssue, onSelectIssue }) {
  const [showRewriteModal, setShowRewriteModal] = useState(false)

  const severityColors = {
    high: '#dc3545',
    medium: '#ffc107',
    low: '#17a2b8'
  }

  return (
    <div className="issues-panel">
      <div className="panel-header">
        <h2>Issues Found ({issues.length})</h2>
        <div className="filters">
          <button className="filter-btn active">All</button>
          <button className="filter-btn">High</button>
          <button className="filter-btn">Medium</button>
          <button className="filter-btn">Low</button>
        </div>
      </div>

      <div className="issues-list">
        {issues.map((issue) => (
          <div
            key={issue.id}
            className={`issue-card ${selectedIssue?.id === issue.id ? 'selected' : ''}`}
            onClick={() => onSelectIssue(issue)}
          >
            <div className="issue-header">
              <span
                className="severity-badge"
                style={{ background: severityColors[issue.severity] }}
              >
                {issue.severity}
              </span>
              <span className="issue-type">{issue.type}</span>
            </div>

            <h3 className="issue-title">{issue.title}</h3>
            <p className="issue-description">{issue.description}</p>

            <div className="issue-location">
              📍 {issue.location.section} • Para {issue.location.paragraph + 1}
            </div>

            {selectedIssue?.id === issue.id && (
              <div className="issue-actions">
                <button
                  className="btn-rewrite"
                  onClick={(e) => {
                    e.stopPropagation()
                    setShowRewriteModal(true)
                  }}
                >
                  ✨ View AI Rewrite
                </button>
                <button className="btn-dismiss">Dismiss</button>
              </div>
            )}
          </div>
        ))}
      </div>

      {showRewriteModal && selectedIssue && (
        <RewriteModal
          issue={selectedIssue}
          onClose={() => setShowRewriteModal(false)}
          onAccept={() => {
            setShowRewriteModal(false)
            // TODO: Apply rewrite
          }}
        />
      )}
    </div>
  )
}

export default IssuesPanel
