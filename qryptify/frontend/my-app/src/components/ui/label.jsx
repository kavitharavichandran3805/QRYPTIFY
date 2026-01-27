import React from 'react';

export function Label({ children, className = '', ...props }) {
  return (
    <label
      className={`block text-gray-700 font-semibold mb-1 ${className}`}
      {...props}
    >
      {children}
    </label>
  );
}
