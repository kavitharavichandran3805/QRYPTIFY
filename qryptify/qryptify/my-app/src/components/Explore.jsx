import React from "react";

export default function Explore() {
  return (
    <section className="min-h-screen bg-gradient-to-br from-white via-blue-50 to-cyan-100 flex justify-center items-center p-8">
      <div className="max-w-4xl w-full bg-white bg-opacity-50 backdrop-blur-lg rounded-3xl shadow-xl p-12 border border-blue-200">
        <h1 className="text-5xl font-extrabold mb-6 text-blue-900 tracking-tight drop-shadow-lg">
          Explore Resources
        </h1>
        <p className="text-lg text-blue-700 mb-8 leading-relaxed">
          Access a curated collection of comprehensive FAQs, hands-on tutorials,
          and top cryptography best practices designed to empower your journeys
          in data protection and analysis.
        </p>
        <ul className="list-disc list-inside space-y-4 text-blue-800 text-lg">
          <li>Detailed encryption tool guides with walkthroughs</li>
          <li>Use-case scenarios and practical workflows</li>
          <li>Step-by-step troubleshooting for frequent questions</li>
          <li>Interactive demos and video tutorials</li>
        </ul>
      </div>
    </section>
  );
}