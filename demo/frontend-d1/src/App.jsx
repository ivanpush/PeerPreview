import { useState } from 'react'
import UploadScreen from './pages/UploadScreen'
import ProcessScreen from './pages/ProcessScreen'
import ReviewScreen from './pages/ReviewScreen'

function App() {
  const [screen, setScreen] = useState('upload') // 'upload' | 'process' | 'review'

  return (
    <div className="app">
      {screen === 'upload' && <UploadScreen onUpload={() => setScreen('process')} />}
      {screen === 'process' && <ProcessScreen onComplete={() => setScreen('review')} />}
      {screen === 'review' && <ReviewScreen onBack={() => setScreen('upload')} />}
    </div>
  )
}

export default App
