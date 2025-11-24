import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useManuscript } from '../context/ManuscriptContext';

function ProcessScreen() {
  const navigate = useNavigate();
  const { loadMockData, loading, error } = useManuscript();
  const [status, setStatus] = useState('loading');
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    const loadData = async () => {
      setStatus('loading');
      setProgress(10);

      // Simulate progress
      const progressInterval = setInterval(() => {
        setProgress(prev => {
          if (prev >= 90) {
            clearInterval(progressInterval);
            return 90;
          }
          return prev + 10;
        });
      }, 300);

      await loadMockData();

      clearInterval(progressInterval);
      setProgress(100);
      setStatus('complete');

      // Auto-navigate after a brief delay
      setTimeout(() => {
        navigate('/review');
      }, 1000);
    };

    loadData();
  }, [loadMockData, navigate]);

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 flex items-center justify-center p-8">
        <div className="max-w-md w-full bg-white rounded-xl shadow-lg p-8">
          <div className="text-center">
            <div className="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-3xl">❌</span>
            </div>
            <h2 className="text-2xl font-semibold text-gray-800 mb-2">Error Loading Data</h2>
            <p className="text-gray-600 mb-4">{error}</p>
            <button
              onClick={() => navigate('/')}
              className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
            >
              Back to Upload
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 flex items-center justify-center p-8">
      <div className="max-w-md w-full bg-white rounded-xl shadow-lg p-8">
        <div className="text-center">
          {status === 'loading' ? (
            <>
              {/* Animated spinner */}
              <div className="relative w-24 h-24 mx-auto mb-6">
                <div className="absolute inset-0 border-4 border-blue-200 rounded-full"></div>
                <div className="absolute inset-0 border-4 border-blue-600 rounded-full border-t-transparent animate-spin"></div>
              </div>

              <h2 className="text-2xl font-semibold text-gray-800 mb-2">
                Processing Manuscript
              </h2>
              <p className="text-gray-600 mb-6">
                Analyzing content and detecting issues...
              </p>

              {/* Progress bar */}
              <div className="w-full bg-gray-200 rounded-full h-2 mb-2">
                <div
                  className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                  style={{ width: `${progress}%` }}
                ></div>
              </div>
              <p className="text-sm text-gray-500">{progress}%</p>

              {/* Status steps */}
              <div className="mt-6 space-y-2 text-left">
                <div className={`flex items-center gap-2 ${progress >= 20 ? 'text-green-600' : 'text-gray-400'}`}>
                  <span>{progress >= 20 ? '✓' : '○'}</span>
                  <span className="text-sm">Parsing document structure</span>
                </div>
                <div className={`flex items-center gap-2 ${progress >= 50 ? 'text-green-600' : 'text-gray-400'}`}>
                  <span>{progress >= 50 ? '✓' : '○'}</span>
                  <span className="text-sm">Analyzing sections and citations</span>
                </div>
                <div className={`flex items-center gap-2 ${progress >= 80 ? 'text-green-600' : 'text-gray-400'}`}>
                  <span>{progress >= 80 ? '✓' : '○'}</span>
                  <span className="text-sm">Running review agents (Tracks A, B, C)</span>
                </div>
              </div>
            </>
          ) : (
            <>
              <div className="w-20 h-20 bg-green-500 rounded-full flex items-center justify-center mx-auto mb-6 animate-bounce">
                <svg className="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <h2 className="text-2xl font-semibold text-gray-800 mb-2">
                Analysis Complete!
              </h2>
              <p className="text-gray-600 mb-4">
                Redirecting to review screen...
              </p>
            </>
          )}
        </div>
      </div>
    </div>
  );
}

export default ProcessScreen;
