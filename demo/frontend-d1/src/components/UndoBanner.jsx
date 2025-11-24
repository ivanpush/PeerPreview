import './UndoBanner.css'

function UndoBanner({ message, onUndo, onDismiss }) {
  return (
    <div className="undo-banner">
      <span className="message">{message}</span>
      <div className="actions">
        <button className="undo-btn" onClick={onUndo}>
          ↶ Undo
        </button>
        <button className="dismiss-btn" onClick={onDismiss}>
          ✕
        </button>
      </div>
    </div>
  )
}

export default UndoBanner
