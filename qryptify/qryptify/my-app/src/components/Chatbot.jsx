import React, { useState, useCallback, useEffect, useRef } from "react";
import Groq from "groq-sdk";

const groq = new Groq({
  apiKey: import.meta.env.VITE_GROQ_API_KEY, 
  dangerouslyAllowBrowser: true,
});

// Compact Qryptify knowledge base (summarized)
const QRYPTIFY_KB = `
PROJECT OVERVIEW
- Qryptify is an AI-driven cryptographic algorithm detection platform with blockchain auditing.
- It analyzes ciphertext or encrypted network traffic to identify the underlying cryptographic algorithm, including classical, modern, and selected post-quantum schemes.
- It is designed as a defense tool against ransomware and encryption misuse, supporting digital forensics, compliance, and risk assessment.

CORE FEATURES
- Detects algorithms such as AES, DES, RSA, Blowfish and post-quantum algorithms like Kyber, based on statistical features of ciphertext.
- Uses NIST Statistical Test Suite (STS) metrics (entropy, frequency, runs, serial correlation, etc.) to turn ciphertext into feature vectors.
- Classifies algorithms with a machine learning model (XGBoost, with future extension to CNN) and outputs:
  - algorithm name
  - algorithm category (classical / modern / post-quantum)
  - confidence score.
- Stores hashes of predictions and reports on a blockchain audit layer to ensure tamper-proof, traceable logs for forensic and regulatory use.
- Implements Role-Based Access Control (RBAC) so only authorized cybersecurity professionals and auditors can access analysis features.

FRONTEND & WORKFLOW
- React + Tailwind UI with pages: Homepage, Login/Signup, Support/Help, File Upload, Result page.
- Users upload encrypted files; backend runs NIST STS + XGBoost and returns detected algorithm, category, and confidence score.

USE CASES
- Ransomware investigation when only ciphertext is available (e.g., WannaCry, healthcare attacks, LCRYX).
- Compliance and audits that require immutable logs of encryption analysis.
- Planning migration from legacy algorithms to post-quantum cryptography.

LIMITATIONS & FUTURE WORK
- Accuracy depends on good ciphertext datasets, especially for post-quantum algorithms.
- Full NIST STS is computationally heavy; real-time streaming is a planned enhancement.
- Future work: CNN models, live network traffic, richer dashboards, and tighter AI–blockchain integration.
`;

// System message: explicitly force 5–6 lines
const INITIAL_SYSTEM = {
  role: "system",
  content: `
You are Qryptify AI, the official assistant for the Qryptify platform.

Use the following Qryptify documentation to answer user questions:
${QRYPTIFY_KB}

INSTRUCTIONS
- When the user asks about Qryptify (features, modules, tech stack, architecture, use cases, limitations, future work), answer using this documentation.
- Explain concepts in clear, simple language suitable for students, security engineers, and non-experts.
- If the user asks something not defined, clearly say that detail is not specified instead of guessing.
- For general cryptography or security questions, you may answer normally but, where relevant, relate the explanation back to how Qryptify works.
- Keep answers concise: respond in 5–6 short lines maximum, unless the user explicitly asks for a longer, very detailed answer.
- Avoid bullet lists unless the user asks for them; prefer 5–6 plain text lines.
`,
};

// optional helper: hard-trim to ~6 lines if the model still talks too much
function trimToSixLines(text) {
  const lines = text.split("\n").filter((l) => l.trim() !== "");
  if (lines.length <= 6) return text.trim();
  return lines.slice(0, 6).join("\n").trim();
}

export default function Chatbot() {
  const [messages, setMessages] = useState([INITIAL_SYSTEM]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  // ref to the bottom of the messages list
  const bottomRef = useRef(null);

  // auto-scroll whenever messages change
  useEffect(() => {
    if (bottomRef.current) {
      bottomRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages]);

  const handleSend = useCallback(
    async (e) => {
      e.preventDefault();
      const text = input.trim();
      if (!text || loading) return;

      const nextMessages = [...messages, { role: "user", content: text }];
      setMessages(nextMessages);
      setInput("");
      setLoading(true);

      try {
        const completion = await groq.chat.completions.create({
          model: "llama-3.3-70b-versatile",
          messages: nextMessages,
          // small cap so it cannot write essays
          max_completion_tokens: 150,
          temperature: 0.5,
          top_p: 1,
        });

        let reply =
          completion.choices?.[0]?.message?.content ||
          "Sorry, I could not generate a response.";

        // enforce 5–6 lines on the client side too
        reply = trimToSixLines(reply);

        setMessages([...nextMessages, { role: "assistant", content: reply }]);
      } catch (err) {
        setMessages([
          ...nextMessages,
          {
            role: "assistant",
            content:
              "There was an error reaching Qryptify AI. Please check your API key and network.",
          },
        ]);
      } finally {
        setLoading(false);
      }
    },
    [messages, input, loading]
  );

  return (
    <div className="flex items-center justify-center min-h-[480px] bg-gradient-to-br from-sky-50 via-white to-cyan-50">
      <div className="w-full max-w-3xl mx-2">
        <div className="rounded-3xl bg-white/80 shadow-[0_20px_60px_rgba(15,23,42,0.12)] border border-sky-50 backdrop-blur">
          {/* Header */}
          <div className="flex items-center justify-between px-6 py-4 border-b border-slate-100">
            <div>
              <p className="text-xs font-semibold tracking-wide text-sky-500 uppercase">
                Qryptify AI Assistant
              </p>
              <h2 className="text-lg font-semibold text-slate-900">
                Live Cryptographic Advisor
              </h2>
              <p className="mt-1 text-xs text-slate-500">
                Ask anything about Qryptify, algorithm detection, ransomware, or
                blockchain auditing.
              </p>
            </div>
            <span className="inline-flex items-center gap-2 rounded-full bg-emerald-50 px-3 py-1 text-xs font-medium text-emerald-700">
              <span className="h-2 w-2 rounded-full bg-emerald-500 animate-pulse" />
              Online
            </span>
          </div>

          {/* Chat Area */}
          <div className="px-6 py-4 max-h-[420px] overflow-y-auto space-y-4 bg-gradient-to-b from-white via-sky-50/40 to-white">
            {messages
              .filter((m) => m.role !== "system")
              .map((msg, idx) => {
                const isUser = msg.role === "user";
                return (
                  <div
                    key={idx}
                    className={`flex ${
                      isUser ? "justify-end" : "justify-start"
                    }`}
                  >
                    <div
                      className={`max-w-[80%] rounded-2xl px-4 py-3 text-sm leading-relaxed shadow-sm ${
                        isUser
                          ? "bg-gradient-to-r from-sky-500 to-cyan-500 text-white rounded-br-sm"
                          : "bg-white text-slate-900 border border-sky-50 rounded-bl-sm"
                      }`}
                    >
                      {!isUser && (
                        <p className="mb-1 text-[10px] font-semibold uppercase tracking-wide text-sky-500">
                          Qryptify AI
                        </p>
                      )}
                      <p className="whitespace-pre-wrap">{msg.content}</p>
                    </div>
                  </div>
                );
              })}

            {loading && (
              <div className="flex justify-start">
                <div className="inline-flex items-center gap-2 rounded-2xl bg-white border border-sky-50 px-4 py-2 text-xs text-slate-600 shadow-sm">
                  <span className="h-2 w-2 rounded-full bg-sky-400 animate-ping" />
                  Qryptify AI is thinking...
                </div>
              </div>
            )}

            {/* invisible anchor for auto-scroll */}
            <div ref={bottomRef} />
          </div>

          {/* Input Area */}
          <form
            onSubmit={handleSend}
            className="flex items-center gap-3 px-4 py-4 border-t border-slate-100 bg-slate-50/60 rounded-b-3xl"
          >
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask about Qryptify features, NIST tests, ransomware cases, or blockchain logs..."
              className="flex-1 rounded-2xl border border-slate-200 bg-white px-4 py-2.5 text-sm text-slate-800 placeholder:text-slate-400 shadow-sm focus:outline-none focus:ring-2 focus:ring-sky-400 focus:border-sky-400"
            />
            <button
              type="submit"
              disabled={loading || !input.trim()}
              className="inline-flex items-center gap-2 rounded-2xl bg-gradient-to-r from-sky-500 to-cyan-500 px-4 py-2.5 text-sm font-semibold text-white shadow-md hover:shadow-lg hover:from-sky-600 hover:to-cyan-600 disabled:opacity-60 disabled:cursor-not-allowed transition"
            >
              <span>{loading ? "Sending..." : "Send"}</span>
              <span className="text-lg leading-none">↗</span>
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
