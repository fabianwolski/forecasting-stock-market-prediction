import React, { useState } from 'react';
import { BsInfoCircle } from 'react-icons/bs';

const InfoTooltip = ({ content }) => {
  const [showTooltip, setShowTooltip] = useState(false);

  return (
    <div className="relative inline-block">
      <button
        onMouseEnter={() => setShowTooltip(true)}
        onMouseLeave={() => setShowTooltip(false)}
        onClick={() => setShowTooltip(!showTooltip)}
        className="text-gray-400 hover:text-sky-500 transition-colors duration-200 focus:outline-none ml-2"
        aria-label="More information"
      >
        <BsInfoCircle className="h-4 w-4" />
      </button>
      
      {showTooltip && (
        <div className="absolute z-10 bottom-full left-1/2 transform -translate-x-1/2 mb-2 w-72">
          <div className="bg-gray-800 border border-gray-700 rounded-md shadow-lg p-3 text-xs text-gray-300">
            {content}
            <div className="absolute w-3 h-3 bg-gray-800 border-b border-r border-gray-700 transform rotate-45 -bottom-1.5 left-1/2 -translate-x-1/2"></div>
          </div>
        </div>
      )}
    </div>
  );
};

export default InfoTooltip;