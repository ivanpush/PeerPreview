import './UploadScreen.css'

function UploadScreen({ onUpload }) {
  return (
    <div className="upload-screen">
      <div className="upload-container">
        <h1>PeerPreview</h1>
        <p className="subtitle">AI-powered manuscript review assistant</p>

        <div className="upload-box">
          <div className="upload-icon">📄</div>
          <h2>Upload your manuscript</h2>
          <p>Drag and drop a PDF file or click to browse</p>

          <button
            className="upload-btn"
            onClick={onUpload}
          >
            Choose File (Demo)
          </button>
        </div>

        <div className="demo-note">
          ⚠️ This is a static demo with mock data
        </div>
      </div>
    </div>
  )
}

export default UploadScreen
