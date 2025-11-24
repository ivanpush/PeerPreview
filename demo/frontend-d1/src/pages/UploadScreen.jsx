import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function UploadScreen() {
  const [fileName, setFileName] = useState('');
  const [isDragging, setIsDragging] = useState(false);
  const navigate = useNavigate();

  const handleDrop = (e) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    if (file && file.type === 'application/pdf') {
      setFileName(file.name);
    }
    setIsDragging(false);
  };

  const handleFileSelect = (e) => {
    const file = e.target.files[0];
    if (file) {
      setFileName(file.name);
    }
  };

  const handleParse = () => {
    if (fileName || true) { // Always allow in demo mode
      navigate('/process');
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 flex items-center justify-center p-8">
      <div className="max-w-2xl w-full">
        <h1 className="text-5xl font-bold text-gray-800 mb-2 text-center">
          PeerPreview
        </h1>
        <p className="text-gray-600 text-center mb-8 text-lg">
          AI-Powered Scientific Manuscript Review
        </p>

        <div
          className={`
            border-2 border-dashed rounded-xl p-12 text-center transition-all bg-white shadow-lg
            ${isDragging ? 'border-blue-500 bg-blue-50 scale-105' : 'border-gray-300'}
            ${fileName ? 'border-green-500' : ''}
          `}
          onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
          onDragLeave={() => setIsDragging(false)}
          onDrop={handleDrop}
        >
          <div className="text-6xl mb-4">📄</div>

          {fileName ? (
            <div className="space-y-4">
              <p className="text-lg font-medium text-gray-900">
                {fileName}
              </p>
              <button
                onClick={handleParse}
                className="px-8 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition font-medium text-lg shadow-md hover:shadow-lg"
              >
                Parse File
              </button>
            </div>
          ) : (
            <div className="space-y-4">
              <h2 className="text-2xl font-semibold text-gray-800 mb-2">
                Upload your manuscript
              </h2>
              <p className="text-lg text-gray-600 mb-6">
                Drag and drop your PDF here, or
              </p>
              <label className="inline-block">
                <input
                  type="file"
                  accept=".pdf"
                  onChange={handleFileSelect}
                  className="hidden"
                />
                <span className="px-8 py-3 bg-white border-2 border-gray-300 rounded-lg hover:bg-gray-50 cursor-pointer transition inline-block font-medium text-lg shadow hover:shadow-md">
                  Browse Files
                </span>
              </label>
            </div>
          )}
        </div>

        <div className="mt-6 p-4 bg-amber-50 border border-amber-200 rounded-lg">
          <div className="flex items-start gap-2">
            <span className="text-amber-600 text-xl">⚠️</span>
            <div>
              <p className="text-sm font-medium text-amber-900">Demo Mode</p>
              <p className="text-sm text-amber-800">
                This is a static demo with mock data. Upload any PDF to see the example manuscript.
              </p>
            </div>
          </div>
        </div>

        {/* Quick access for demo */}
        <div className="mt-4 text-center">
          <button
            onClick={handleParse}
            className="text-sm text-blue-600 hover:text-blue-700 underline"
          >
            Skip to demo →
          </button>
        </div>
      </div>
    </div>
  );
}

export default UploadScreen;
