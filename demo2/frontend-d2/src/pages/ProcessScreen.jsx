import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useManuscript } from '../context/ManuscriptContext';

function ProcessScreen() {
  const navigate = useNavigate();
  const { loadMockData, loading, error } = useManuscript();
  const [status, setStatus] = useState('loading');
  const [progress, setProgress] = useState(0);
  const [reviewMode, setReviewMode] = useState('static');

  useEffect(() => {
    // Get review configuration from sessionStorage
    const reviewConfig = JSON.parse(sessionStorage.getItem('reviewConfig') || '{}');
    setReviewMode(reviewConfig.reviewMode || 'static');

    const loadData = async () => {
      setStatus('loading');
      setProgress(10);

      if (reviewConfig.reviewMode === 'static') {
        // Static mode - load pre-computed data quickly
        const progressInterval = setInterval(() => {
          setProgress(prev => {
            if (prev >= 90) {
              clearInterval(progressInterval);
              return 90;
            }
            return prev + 20;
          });
        }, 200);

        await loadMockData();

        clearInterval(progressInterval);
        setProgress(100);
        setStatus('complete');

        // Auto-navigate after a brief delay
        setTimeout(() => {
          navigate('/review');
        }, 800);
      } else {
        // Dynamic mode - would call backend API
        // Simulate longer processing for agents
        const stages = [
          { progress: 20, label: 'Parsing document structure', duration: 1000 },
          { progress: 40, label: 'Running Planning Agent', duration: 2000 },
          { progress: 60, label: 'Running Track A (Rigor)', duration: 3000 },
          { progress: 75, label: 'Running Track B (Clarity)', duration: 2500 },
          { progress: 90, label: 'Running Track C (Skeptic)', duration: 2000 },
          { progress: 100, label: 'Aggregating results', duration: 1000 }
        ];

        let currentStage = 0;

        const processStages = async () => {
          for (const stage of stages) {
            setProgress(stage.progress);
            await new Promise(resolve => setTimeout(resolve, stage.duration));
            currentStage++;
          }

          // In production, this would be:
          // const response = await fetch('/api/run-review', {
          //   method: 'POST',
          //   body: JSON.stringify(reviewConfig)
          // });
          // const data = await response.json();
          // setManuscriptData(data);

          // For demo, load mock data
          await loadMockData();
          setStatus('complete');

          setTimeout(() => {
            navigate('/review');
          }, 1000);
        };

        processStages();
      }
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
                {reviewMode === 'static' ? 'Loading Review' : 'Running AI Analysis'}
              </h2>
              <p className="text-gray-600 mb-6">
                {reviewMode === 'static'
                  ? 'Loading pre-computed review data...'
                  : 'AI agents analyzing your document...'}
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
                {reviewMode === 'static' ? (
                  <>
                    <div className={`flex items-center gap-2 ${progress >= 30 ? 'text-green-600' : 'text-gray-400'}`}>
                      <span>{progress >= 30 ? '✓' : '○'}</span>
                      <span className="text-sm">Loading manuscript data</span>
                    </div>
                    <div className={`flex items-center gap-2 ${progress >= 60 ? 'text-green-600' : 'text-gray-400'}`}>
                      <span>{progress >= 60 ? '✓' : '○'}</span>
                      <span className="text-sm">Loading review issues</span>
                    </div>
                    <div className={`flex items-center gap-2 ${progress >= 90 ? 'text-green-600' : 'text-gray-400'}`}>
                      <span>{progress >= 90 ? '✓' : '○'}</span>
                      <span className="text-sm">Preparing interface</span>
                    </div>
                  </>
                ) : (
                  <>
                    <div className={`flex items-center gap-2 ${progress >= 20 ? 'text-green-600' : 'text-gray-400'}`}>
                      <span>{progress >= 20 ? '✓' : '○'}</span>
                      <span className="text-sm">Parsing document structure</span>
                    </div>
                    <div className={`flex items-center gap-2 ${progress >= 40 ? 'text-green-600' : 'text-gray-400'}`}>
                      <span>{progress >= 40 ? '✓' : '○'}</span>
                      <span className="text-sm">Planning review strategy</span>
                    </div>
                    <div className={`flex items-center gap-2 ${progress >= 60 ? 'text-green-600' : 'text-gray-400'}`}>
                      <span>{progress >= 60 ? '✓' : '○'}</span>
                      <span className="text-sm">Track A: Rigor analysis</span>
                    </div>
                    <div className={`flex items-center gap-2 ${progress >= 75 ? 'text-green-600' : 'text-gray-400'}`}>
                      <span>{progress >= 75 ? '✓' : '○'}</span>
                      <span className="text-sm">Track B: Clarity analysis</span>
                    </div>
                    <div className={`flex items-center gap-2 ${progress >= 90 ? 'text-green-600' : 'text-gray-400'}`}>
                      <span>{progress >= 90 ? '✓' : '○'}</span>
                      <span className="text-sm">Track C: Skeptic analysis</span>
                    </div>
                    <div className={`flex items-center gap-2 ${progress >= 100 ? 'text-green-600' : 'text-gray-400'}`}>
                      <span>{progress >= 100 ? '✓' : '○'}</span>
                      <span className="text-sm">Aggregating results</span>
                    </div>
                  </>
                )}
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