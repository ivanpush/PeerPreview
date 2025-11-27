import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { DocumentProvider } from './context/DocumentContext';
import UploadScreen from './pages/UploadScreen';
import ReviewSetupScreen from './pages/ReviewSetupScreen';
import ProcessScreen from './pages/ProcessScreen';
import ReviewScreen from './pages/ReviewScreen';

function App() {
  return (
    <BrowserRouter>
      <DocumentProvider>
        <Routes>
          <Route path="/" element={<UploadScreen />} />
          <Route path="/setup" element={<ReviewSetupScreen />} />
          <Route path="/process" element={<ProcessScreen />} />
          <Route path="/review" element={<ReviewScreen />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </DocumentProvider>
    </BrowserRouter>
  );
}

export default App;