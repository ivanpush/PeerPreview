import { useEffect } from 'react'
import { simulateProcessing } from '../utils/mockLoader'
import './ProcessScreen.css'

function ProcessScreen({ onComplete }) {
  useEffect(() => {
    simulateProcessing(3000).then(onComplete)
  }, [onComplete])

  return (
    <div className="process-screen">
      <div className="process-container">
        <div className="spinner"></div>
        <h2>Analyzing manuscript...</h2>
        <p>Our AI is reviewing your paper</p>

        <div className="steps">
          <div className="step active">✓ Parsing document</div>
          <div className="step active">✓ Extracting sections</div>
          <div className="step loading">⟳ Analyzing content</div>
          <div className="step">⏳ Generating suggestions</div>
        </div>
      </div>
    </div>
  )
}

export default ProcessScreen
