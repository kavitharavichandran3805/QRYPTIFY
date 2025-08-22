import React from 'react';

export function Button({ children, className = '', ...props }) {
  return (
    <button
      className={`w-full h-12 bg-gradient-to-r from-blue-600 to-cyan-500 hover:from-blue-700 hover:to-cyan-600 text-white font-semibold rounded-xl shadow-lg flex items-center justify-center transition-colors ${className}`}
      {...props}
    >
      {children}
    </button>
  );
}
