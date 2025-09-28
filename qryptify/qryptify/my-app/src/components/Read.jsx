import React from "react";

export default function Read() {
  return (
    <section className="min-h-screen bg-gradient-to-br from-cyan-50 via-blue-100 to-white flex justify-center items-center p-8">
      <div className="max-w-4xl w-full bg-white rounded-3xl shadow-2xl p-12 border border-gray-200">
        <h1 className="text-5xl font-extrabold mb-6 text-blue-800 tracking-tight">
          Whitepapers & Research
        </h1>
        <p className="text-lg text-gray-700 mb-8 leading-relaxed">
          Dive deep into the technical foundations and innovative research behind Qryptify’s
          cryptographic methods and data analysis framework.
        </p>
        <ul className="list-disc list-inside text-blue-700 space-y-3">
          <li><strong>Algorithmic Analysis Whitepaper</strong>: Comprehensive overview of AI-driven crypto analysis.</li>
          <li><strong>Quantum-Resistant Cryptography</strong>: Details on post-quantum cryptography integrations.</li>
          <li><strong>Performance Benchmarks</strong>: Detailed testing methodology and result reports.</li>
        </ul>
      </div>
    </section>
  );
}