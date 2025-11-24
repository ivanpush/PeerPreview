import './ManuscriptView.css'

function ManuscriptView({ manuscript, selectedIssue }) {
  return (
    <div className="manuscript-view">
      <div className="manuscript-content">
        <h1 className="manuscript-title">{manuscript.title}</h1>

        <div className="authors">{manuscript.authors.join(', ')}</div>

        {manuscript.sections.map((section, idx) => (
          <section key={idx} className="manuscript-section">
            <h2 className="section-heading">{section.title}</h2>

            {section.paragraphs.map((para, pIdx) => {
              const hasIssue = selectedIssue &&
                selectedIssue.location.section === section.title &&
                selectedIssue.location.paragraph === pIdx

              return (
                <p
                  key={pIdx}
                  className={`paragraph ${hasIssue ? 'highlighted' : ''}`}
                >
                  {para}
                </p>
              )
            })}
          </section>
        ))}
      </div>
    </div>
  )
}

export default ManuscriptView
