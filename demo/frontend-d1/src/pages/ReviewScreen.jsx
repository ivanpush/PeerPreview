import { useState, useEffect } from 'react'
import { loadManuscript, loadIssues } from '../utils/mockLoader'
import ManuscriptView from '../components/ManuscriptView'
import IssuesPanel from '../components/IssuesPanel'
import './ReviewScreen.css'

function ReviewScreen({ onBack }) {
  const [manuscript, setManuscript] = useState(null)
  const [issues, setIssues] = useState([])
  const [selectedIssue, setSelectedIssue] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    Promise.all([loadManuscript(), loadIssues()])
      .then(([manuscriptData, issuesData]) => {
        setManuscript(manuscriptData)
        setIssues(issuesData)
        setLoading(false)
      })
  }, [])

  if (loading) {
    return <div className="review-screen loading">Loading...</div>
  }

  return (
    <div className="review-screen">
      <header className="review-header">
        <button className="back-btn" onClick={onBack}>← Back</button>
        <h1>Review: {manuscript.title}</h1>
        <div className="actions">
          <button className="btn-secondary">Export Report</button>
          <button className="btn-primary">Submit Revision</button>
        </div>
      </header>

      <div className="review-content">
        <ManuscriptView
          manuscript={manuscript}
          selectedIssue={selectedIssue}
        />
        <IssuesPanel
          issues={issues}
          selectedIssue={selectedIssue}
          onSelectIssue={setSelectedIssue}
        />
      </div>
    </div>
  )
}

export default ReviewScreen
