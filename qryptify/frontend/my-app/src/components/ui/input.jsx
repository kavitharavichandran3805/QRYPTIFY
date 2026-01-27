import React from 'react';

export function Input({ className = '', ...props }) {
  return (
    <input
      className={`w-full border border-gray-300 rounded-xl px-4 py-3 text-gray-900 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition duration-200 ${className}`}
      {...props}
    />
  );
}
