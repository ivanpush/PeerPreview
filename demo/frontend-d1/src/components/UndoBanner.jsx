import React from 'react';

function UndoBanner({ message, onUndo, onDismiss }) {
  return (
    <div className="fixed bottom-6 left-1/2 transform -translate-x-1/2 bg-gray-800 text-white px-6 py-3 rounded-lg shadow-lg flex items-center gap-4 z-50 animate-slide-up">
      <span className="text-sm font-medium">{message}</span>
      <div className="flex gap-2">
        <button
          onClick={onUndo}
          className="px-3 py-1 bg-blue-600 hover:bg-blue-700 text-white text-sm rounded transition flex items-center gap-1"
        >
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 10h10a8 8 0 018 8v2M3 10l6 6m-6-6l6-6" />
          </svg>
          Undo
        </button>
        <button
          onClick={onDismiss}
          className="text-gray-400 hover:text-white transition"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
    </div>
  );
}

export default UndoBanner;
