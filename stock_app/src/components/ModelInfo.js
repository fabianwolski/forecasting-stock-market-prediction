import React, { useState, useRef, useEffect } from 'react';
import { BsInfoCircleFill } from 'react-icons/bs';
import modelDescriptions from '../data/modelDescription.json';

const ModelInfo = ({ selectedModel }) => {
  const [showInfo, setShowInfo] = useState(false);
  const infoRef = useRef(null);
  
  //closing popup when clicking outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (infoRef.current && !infoRef.current.contains(event.target)) {
        setShowInfo(false);
      }
    };

    if (showInfo) {
      document.addEventListener('mousedown', handleClickOutside);
    } else {
      document.removeEventListener('mousedown', handleClickOutside);
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [showInfo]);
  
  const info = modelDescriptions[selectedModel] || {
    name: "Unknown Model",
    description: "No information available for this model.",
    strengths: [],
    weaknesses: [],
    features: [],
    graphExpectation: ""
  };

  return (
    <div className="relative inline-block">
      <button 
        onClick={() => setShowInfo(!showInfo)}
        className="flex items-center text-sky-500 hover:text-sky-400 transition-colors duration-200 text-sm mt-2"
      >
        <BsInfoCircleFill className="mr-1" />
        <span>About {info.name}</span>
      </button>
      
      {showInfo && (
        <div 
          ref={infoRef}
          className="fixed inset-0 z-50 flex items-center justify-center bg-gray-900 bg-opacity-75"
          onClick={() => setShowInfo(false)}
        >
          <div 
            className="bg-gray-900 border border-gray-700 rounded-lg shadow-xl p-4 text-sm w-full max-w-xl m-4"
            onClick={(e) => e.stopPropagation()}
          >
            <h3 className="text-sky-500 font-medium mb-2">{info.name}</h3>
            <p className="text-gray-300 mb-3">{info.description}</p>
            
            <div className="mb-4 border-l-2 border-sky-600 pl-3">
              <h4 className="text-sky-400 font-medium mb-1">Graph Visualization</h4>
              <p className="text-gray-300">{info.graphExpectation}</p>
              <div className="flex items-center mt-2">
                <div className="flex items-center mr-3">
                  <span className="inline-block w-3 h-3 rounded-full bg-blue-500 mr-1"></span>
                  <span className="text-xs text-gray-400">Actual</span>
                </div>
                <div className="flex items-center mr-3">
                  <span className="inline-block w-3 h-3 rounded-full bg-green-400 mr-1"></span>
                  <span className="text-xs text-gray-400">Training</span>
                </div>
                <div className="flex items-center">
                  <span className="inline-block w-3 h-3 rounded-full bg-yellow-300 mr-1"></span>
                  <span className="text-xs text-gray-400">Test</span>
                </div>
              </div>
            </div>
            
            <div className="mb-3">
              <h4 className="text-green-400 font-medium mb-1">Strengths</h4>
              <ul className="list-disc pl-5 text-gray-300">
                {info.strengths.map((strength, i) => (
                  <li key={`strength-${i}`}>{strength}</li>
                ))}
              </ul>
            </div>
            
            <div className="mb-3">
              <h4 className="text-red-400 font-medium mb-1">Limitations</h4>
              <ul className="list-disc pl-5 text-gray-300">
                {info.weaknesses.map((weakness, i) => (
                  <li key={`weakness-${i}`}>{weakness}</li>
                ))}
              </ul>
            </div>
            
            <div>
              <h4 className="text-yellow-400 font-medium mb-1">Key Features</h4>
              <ul className="list-disc pl-5 text-gray-300">
                {info.features.map((feature, i) => (
                  <li key={`feature-${i}`}>{feature}</li>
                ))}
              </ul>
            </div>
            
            <button 
              onClick={() => setShowInfo(false)}
              className="mt-3 px-3 py-1 bg-gray-800 hover:bg-gray-700 text-gray-300 rounded transition-colors duration-200 text-xs"
            >
              Close
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default ModelInfo;