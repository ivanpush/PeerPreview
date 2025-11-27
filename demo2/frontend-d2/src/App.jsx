import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { ManuscriptProvider } from './context/ManuscriptContext';
import UploadScreen from './pages/UploadScreen';
import ReviewSetupScreen from './pages/ReviewSetupScreen';
import ProcessScreen from './pages/ProcessScreen';
import ReviewScreen from './pages/ReviewScreen';

function App() {
  return (
    <BrowserRouter>
      <ManuscriptProvider>
        <Routes>
          <Route path="/" element={<UploadScreen />} />
          <Route path="/setup" element={<ReviewSetupScreen />} />
          <Route path="/process" element={<ProcessScreen />} />
          <Route path="/review" element={<ReviewScreen />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </ManuscriptProvider>
    </BrowserRouter>
  );
}

export default App;