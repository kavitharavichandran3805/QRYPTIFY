import React, { useState } from 'react';
import { Link } from 'react-router-dom'; // Import Link from react-router-dom for My Account navigation
import Logo from './Logo'; // Your full animated Logo.jsx component here
import {api} from './api'

// User icon SVG matching your sample (inside a circle user silhouette)
const User = ({ className = 'w-8 h-8' }) => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    className={className}
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
  >
    <circle cx="12" cy="8" r="4" stroke="black" strokeWidth="2" fill="black" />
    <path
      d="M4 20c0-4 4-6 8-6s8 2 8 6"
      stroke="black"
      strokeWidth="2"
      fill="none"
    />
    <circle cx="12" cy="12" r="10" stroke="black" strokeWidth="2" fill="none" />
  </svg>
);

// Simple Button component
const Button = ({ variant, children, ...rest }) => (
  <button
    className={`px-4 py-2 rounded ${
      variant === 'outline' ? 'border border-gray-400 bg-white' : 'bg-blue-500 text-white'
    }`}
    {...rest}
  >
    {children}
  </button>
);

// Simple page URL creator (unchanged for Home button)
const createPageUrl = (page) => (page === 'Home' ? '/' : '/analysis');

// Mock upload file API
async function UploadFile({ file }) {
  return new Promise((resolve) =>
    setTimeout(() => resolve({ file_url: 'https://example.com/uploaded/' + file.name }), 1000)
  );
}

// Mock extraction API
async function ExtractDataFromUploadedFile({ file_url, json_schema }) {
  return new Promise((resolve) =>
    setTimeout(
      () =>
        resolve({
          algorithms: [
            { name: 'AES-256', confidence_score: 0.95 },
            { name: 'RSA-2048', confidence_score: 0.78 },
            { name: 'ChaCha20', confidence_score: 0.65 },
          ],
        }),
      1500
    )
  );
}

// Updated Header component with dropdown menu
const AppHeader = () => {
  const [menuOpen, setMenuOpen] = useState(false);

  const handleLogout = async () => {
    try{
      const result=await api('logout',"GET")
      if(result.status){
        alert('Logged out successfully');
      }
      else{
        alert('Error in logging out')
      }
    }
    catch(err){
      alert("Failed to logout")
    }
    setMenuOpen(false);
  };

  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-white/90 backdrop-blur-lg border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-6">
        <div className="flex items-center justify-between h-16">
          <Logo />
          <div className="flex items-center gap-4 relative">
            {/* Home button remains unchanged as an anchor tag */}
            <a href={createPageUrl('Home')}>
              <Button variant="outline">Home</Button>
            </a>

            {/* User Icon */}
            <div
              className="w-10 h-10 bg-gray-100 rounded-full flex items-center justify-center cursor-pointer"
              onClick={() => setMenuOpen((prev) => !prev)}
            >
              <User className="w-6 h-6" />
            </div>

            {/* Dropdown Menu */}
            {menuOpen && (
              <div className="absolute right-0 top-12 w-40 bg-white border border-gray-200 rounded-lg shadow-lg">
                {/* My Account now uses React Router Link for SPA navigation */}
                <Link
                  to="/account"
                  className="block px-4 py-2 hover:bg-gray-100"
                  onClick={() => setMenuOpen(false)}
                >
                  My Account
                </Link>
                <button
                  className="w-full text-left px-4 py-2 hover:bg-gray-100"
                  onClick={handleLogout}
                >
                  Logout
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </header>
  );
};


const FileUploadBox = ({ onFileSelect, isLoading }) => {
  const handleFileChange = (ev) => {
    if (ev.target.files.length > 0) onFileSelect(ev.target.files[0]);
  };

  return (
    <div className="bg-white rounded-2xl shadow-lg border border-gray-200 flex flex-col items-center justify-center p-8 h-full">
      <input
        type="file"
        id="file-upload"
        className="hidden"
        onChange={handleFileChange}
        disabled={isLoading}
      />
      <label
        htmlFor="file-upload"
        className={`w-full text-center group cursor-pointer ${
          isLoading ? 'cursor-not-allowed' : ''
        }`}
      >
        <div
          className={`relative border-2 border-dashed border-gray-300 rounded-xl p-10 transition-colors duration-300 ${
            !isLoading
              ? 'group-hover:border-blue-500 group-hover:bg-blue-50'
              : 'bg-gray-100'
          }`}
        >
          <div className="flex flex-col items-center text-gray-600">
            <svg
              className={`w-12 h-12 mb-4 text-gray-400 transition-transform duration-300 ${
                !isLoading ? 'group-hover:scale-110 group-hover:text-blue-600' : ''
              }`}
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M4 16v2a2 2 0 002 2h12a2 2 0 002-2v-2M7 10l5-5m0 0l5 5m-5-5v12"
              ></path>
            </svg>
            <h3 className="text-xl font-semibold mb-2">Upload Encrypted File</h3>
            <p className="text-sm">Click here to select your file</p>
          </div>
        </div>
      </label>
    </div>
  );
};

const ProcessingAnimation = () => (
  <div className="flex flex-col items-center justify-center h-full text-center">
    <style>{`
      .scanner {
        width: 100px;
        height: 2px;
        background-color: #3b82f6;
        box-shadow: 0 0 10px #3b82f6, 0 0 20px #3b82f6;
        animation: scan 3s linear infinite;
        position: absolute;
      }
      @keyframes scan {
        0% { top: 0; }
        50% { top: 100%; }
        100% { top: 0; }
      }
    `}</style>
    <div className="relative w-24 h-24 mb-6">
      <div className="w-full h-full border-4 border-dashed border-blue-200 rounded-full animate-spin-slow"></div>
      <div className="absolute inset-0 flex items-center justify-center overflow-hidden rounded-full">
        <div className="scanner"></div>
      </div>
    </div>
    <h3 className="text-2xl font-semibold text-gray-800">Processing...</h3>
    <p className="text-gray-500 mt-2">Our AI is analyzing the cryptographic patterns.</p>
  </div>
);

const ResultsDisplay = ({ result, isLoading, error }) => {
  if (isLoading)
    return (
      <div className="bg-white rounded-2xl shadow-lg border border-gray-200 p-8 h-full">
        <ProcessingAnimation />
      </div>
    );

  if (error)
    return (
      <div className="bg-white rounded-2xl shadow-lg border border-red-200 p-8 h-full flex flex-col items-center justify-center text-center">
        <h3 className="text-2xl font-semibold text-red-700">Analysis Failed</h3>
        <p className="text-red-500 mt-2">{error}</p>
      </div>
    );

  if (!result)
    return (
      <div className="bg-white rounded-2xl shadow-lg border border-gray-200 p-8 h-full flex flex-col items-center justify-center text-center">
        <h3 className="text-2xl font-semibold text-gray-800">Awaiting File</h3>
        <p className="text-gray-500 mt-2">Upload an encrypted file to begin the analysis.</p>
      </div>
    );

  const topAlgorithm = result.algorithms.reduce(
    (max, algo) => (algo.confidence_score > max.confidence_score ? algo : max),
    result.algorithms[0]
  );

  return (
    <div className="bg-gradient-to-br from-blue-600 to-cyan-500 rounded-2xl shadow-2xl p-8 h-full text-white flex flex-col items-center justify-center text-center">
      <h3 className="text-xl font-medium text-blue-100 mb-2">Top Algorithm Detected</h3>
      <h2 className="text-5xl font-bold mb-4">{topAlgorithm.name}</h2>
      <div className="text-7xl font-bold bg-white/20 rounded-full w-40 h-40 flex items-center justify-center border-4 border-white/50">
        {Math.round(topAlgorithm.confidence_score * 100)}
        <span className="text-3xl mt-2">%</span>
      </div>
      <p className="text-blue-200 mt-4">Confidence Score</p>
    </div>
  );
};

export default function AnalysisPage() {
  const [isLoading, setIsLoading] = useState(false);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [error, setError] = useState(null);

  const handleFileSelect = async (file) => {
    setIsLoading(true);
    setAnalysisResult(null);
    setError(null);

    try {
      const { file_url } = await UploadFile({ file });
      const schema = {
        type: 'object',
        properties: {
          algorithms: {
            type: 'array',
            items: {
              type: 'object',
              properties: {
                name: { type: 'string' },
                confidence_score: { type: 'number' },
              },
              required: ['name', 'confidence_score'],
            },
          },
        },
        required: ['algorithms'],
      };
      const output = await ExtractDataFromUploadedFile({ file_url, json_schema: schema });

      if (output && output.algorithms) {
        setAnalysisResult(output);
      } else {
        setError("AI could not process the file. Please ensure it's a valid encrypted text file.");
      }
    } catch (e) {
      console.error(e);
      setError('An unexpected error occurred during analysis.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 pt-24 pb-12">
      <AppHeader />
      <main className="max-w-7xl mx-auto px-6">
        <div className="grid lg:grid-cols-2 gap-8 h-[50vh]">
          <FileUploadBox onFileSelect={handleFileSelect} isLoading={isLoading} />
          <ResultsDisplay result={analysisResult} isLoading={isLoading} error={error} />
        </div>
      </main>
    </div>
  );
}