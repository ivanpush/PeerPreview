import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function UploadScreen() {
  const [fileName, setFileName] = useState('');
  const [isDragging, setIsDragging] = useState(false);
  const [selectedDemo, setSelectedDemo] = useState('');
  const navigate = useNavigate();

  const demoDocuments = [
    { id: 'manuscript_pdf', label: 'Academic Manuscript (PDF)', file: 'manuscript_pdf.json' },
    { id: 'grant_docx', label: 'Grant Proposal (DOCX)', file: 'grant_docx.json' },
    { id: 'policy_brief_pdf', label: 'Policy Brief (PDF)', file: 'policy_brief_pdf.json' },
    { id: 'latex_manuscript', label: 'LaTeX Manuscript (.tex)', file: 'latex_manuscript.json' }
  ];

  const handleDrop = (e) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    if (file && file.type === 'application/pdf') {
      setFileName(file.name);
      setSelectedDemo(''); // Clear demo selection if user uploads
    }
    setIsDragging(false);
  };

  const handleFileSelect = (e) => {
    const file = e.target.files[0];
    if (file) {
      setFileName(file.name);
      setSelectedDemo(''); // Clear demo selection if user uploads
    }
  };

  const handleDemoSelect = (e) => {
    const demoId = e.target.value;
    setSelectedDemo(demoId);
    if (demoId) {
      const demo = demoDocuments.find(d => d.id === demoId);
      setFileName(''); // Clear file upload if demo selected
      // Store selected demo in sessionStorage for next screen
      sessionStorage.setItem('selectedDemo', demoId);
      sessionStorage.setItem('demoFile', demo.file);
    } else {
      sessionStorage.removeItem('selectedDemo');
      sessionStorage.removeItem('demoFile');
    }
  };

  const handleNext = () => {
    if (fileName || selectedDemo) {
      // Navigate to new ReviewSetupScreen instead of directly to process
      navigate('/setup');
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 flex items-center justify-center p-8">
      {/* Small demo selector - top left, unobtrusive */}
      <div className="absolute top-4 left-4">
        <div className="bg-white/80 backdrop-blur-sm rounded-lg px-3 py-2 shadow-sm border border-gray-200">
          <label className="text-xs text-gray-500 block mb-1">Demo Document (V0)</label>
          <select
            value={selectedDemo}
            onChange={handleDemoSelect}
            className="text-sm text-gray-700 bg-transparent border-none focus:outline-none cursor-pointer pr-6"
          >
            <option value="">Select demo document...</option>
            {demoDocuments.map(doc => (
              <option key={doc.id} value={doc.id}>{doc.label}</option>
            ))}
          </select>
        </div>
      </div>

      <div className="max-w-2xl w-full">
        <h1 className="text-5xl font-bold text-gray-800 mb-2 text-center">
          PeerPreview
        </h1>
        <p className="text-gray-600 text-center mb-8 text-lg">
          AI-Powered Document Review System
        </p>

        <div
          className={`
            border-2 border-dashed rounded-xl p-12 text-center transition-all bg-white shadow-lg
            ${isDragging ? 'border-blue-500 bg-blue-50 scale-105' : 'border-gray-300'}
            ${fileName ? 'border-green-500' : ''}
            ${selectedDemo ? 'border-purple-500' : ''}
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
                onClick={handleNext}
                className="px-8 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition font-medium text-lg shadow-md hover:shadow-lg"
              >
                Continue to Setup
              </button>
            </div>
          ) : selectedDemo ? (
            <div className="space-y-4">
              <p className="text-lg font-medium text-purple-900">
                Demo: {demoDocuments.find(d => d.id === selectedDemo)?.label}
              </p>
              <button
                onClick={handleNext}
                className="px-8 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition font-medium text-lg shadow-md hover:shadow-lg"
              >
                Continue to Setup
              </button>
            </div>
          ) : (
            <div className="space-y-4">
              <h2 className="text-2xl font-semibold text-gray-800 mb-2">
                Upload your document
              </h2>
              <p className="text-lg text-gray-600 mb-6">
                Drag and drop your PDF/DOCX/LaTeX file here, or
              </p>
              <label className="inline-block">
                <input
                  type="file"
                  accept=".pdf,.docx,.tex"
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
              <p className="text-sm font-medium text-amber-900">V0 Demo Mode</p>
              <p className="text-sm text-amber-800">
                Upload functionality coming in V1. Use the demo selector (top-left) to test with curated documents.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default UploadScreen;