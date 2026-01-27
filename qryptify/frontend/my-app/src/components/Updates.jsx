import React from "react";

export default function Updates() {
  return (
    <section className="min-h-screen bg-gradient-to-br from-cyan-50 via-blue-100 to-gray-100 flex justify-center items-center p-8">
      <div className="max-w-4xl w-full bg-gradient-to-tr from-white to-blue-100 rounded-3xl shadow-2xl p-12 border border-cyan-300">
        <h1 className="text-5xl font-extrabold mb-6 text-cyan-700 tracking-widest drop-shadow-md">
          Latest Updates
        </h1>
        <p className="text-lg text-cyan-900 mb-8 leading-relaxed">
          Stay ahead with our continuous advancements in cryptography and
          file analysis technology. Here’s what’s new at Qryptify:
        </p>
        <div className="space-y-6">
          <div className="bg-white bg-opacity-70 rounded-xl px-6 py-4 shadow-inner border border-cyan-200">
            <strong>🚀 Faster Processing:</strong> Significantly improved
            algorithm detection speeds for real-time analysis.
          </div>
          <div className="bg-white bg-opacity-70 rounded-xl px-6 py-4 shadow-inner border border-cyan-200">
            <strong>🔒 Enhanced Security:</strong> Introducing multi-factor
            authentication and encrypted session validation.
          </div>
          <div className="bg-white bg-opacity-70 rounded-xl px-6 py-4 shadow-inner border border-cyan-200">
            <strong>✨ New Features:</strong> Added support for post-quantum
            cryptography and detailed key management reports.
          </div>
        </div>
      </div>
    </section>
  );
}