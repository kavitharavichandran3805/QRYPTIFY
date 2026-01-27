import React, { useState, useEffect, useRef } from "react";
import stringSimilarity from "string-similarity";
import '../App.css';

const faqAnswers = [
  {
    question: "What types of encrypted data can Qryptify analyze?",
    answer: "Qryptify can analyze encrypted files, network traffic, cryptographic keys, and digital signatures, including classical and post-quantum encryption.",
  },
  {
    question: "How accurate is the AI algorithm detection?",
    answer: "Our AI achieves 85% accuracy in cryptographic algorithm identification, continually improved by new encryption data.",
  },
  {
    question: "Is my data secure during analysis?",
    answer: "All data is processed in secure isolated environments with end-to-end encryption, and results are recorded on the blockchain. Data is never stored.",
  },
  {
    question: "Can I integrate Qryptify with my existing systems?",
    answer: "Qryptify is designed as a standalone platform without direct integration to ensure maximum security and prevent dependency risks.",
  },
  {
    question: "What encryption algorithms does Qryptify support?",
    answer: "Supports RSA, AES, Kyber, ECDSA, and evolving algorithms detected by AI.",
  },
  {
    question: "How long does analysis take?",
    answer: "Analysis times vary depending on data size, usually completing within seconds to a few minutes.",
  },
  {
    question: "Can Qryptify detect unknown or custom algorithms?",
    answer: "Our AI primarily identifies known classical and post-quantum algorithms and learns continuously from new data.",
  },
  {
    question: "Does Qryptify store my encrypted data?",
    answer: "No, Qryptify processes data temporarily with strict privacy protocols and never stores raw encrypted data.",
  },
  {
    question: "How is blockchain used in Qryptify?",
    answer: "Every analysis result is securely recorded on blockchain to ensure transparency, traceability, and tamper-proof audit trails.",
  },
  {
    question: "How do I start using Qryptify?",
    answer: "Sign up, upload your encrypted data, and let our AI analyze the cryptographic algorithms instantly.",
  },
  {
    question: "Is Qryptify suitable for enterprise use?",
    answer: "Yes, Qryptify offers high security and accurate analysis suited for enterprise cryptography compliance and security audits.",
  },
  {
    question: "What is post-quantum cryptography?",
    answer: "Encryption designed to be secure against attacks from quantum computers, included in Qryptify’s supported algorithms.",
  },
  {
    question: "Can I trust AI analysis over manual cryptography methods?",
    answer: "Qryptify’s AI combines machine learning with expert knowledge to deliver reliable and fast analysis.",
  },
  {
    question: "How often is Qryptify updated?",
    answer: "Our AI models and databases are regularly updated to include new algorithms and latest research.",
  },
  {
    question: "What platforms support Qryptify?",
    answer: "Qryptify is accessible via modern web browsers with cloud-based backend processing.",
  },
  {
    question: "Is there a free trial available?",
    answer: "Yes, new users can try Qryptify with limited features before subscribing.",
  },
  {
    question: "Who can I contact for support?",
    answer: "You can contact support through live chat or the contact section on the website.",
  },
  {
    question: "Does Qryptify comply with data protection regulations?",
    answer: "Yes, we ensure compliance with GDPR, CCPA, and other major data privacy laws.",
  },
  {
    question: "Can Qryptify analyze encrypted communications in real-time?",
    answer: "Yes, Qryptify supports real-time cryptographic analysis of network data streams.",
  },
  {
    question: "What should I do if I encounter issues using Qryptify?",
    answer: "Report issues via live chat or support email, and our expert team will assist promptly."
  }
];

export default function Ping() {
  const [chatOpen, setChatOpen] = useState(false);
  const [messages, setMessages] = useState([
    { from: "bot", text: "Hi! How can I assist you with Qryptify today?" },
  ]);
  const [inputValue, setInputValue] = useState("");
  const bottomRef = useRef(null);

  useEffect(() => {
    if (bottomRef.current) {
      bottomRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages, chatOpen]);

  const handleSend = () => {
    if (!inputValue.trim()) return;
    const userMessage = inputValue.trim();
    setMessages((prev) => [...prev, { from: "user", text: userMessage }]);

    // Find best matching question by similarity
    const questions = faqAnswers.map(faq => faq.question);
    const { bestMatch } = stringSimilarity.findBestMatch(userMessage, questions);

    let botResponse = "Sorry, I don't have an answer for that. Please contact support for further assistance.";
    if (bestMatch.rating > 0.4) {
      const matchedFAQ = faqAnswers.find(faq => faq.question === bestMatch.target);
      botResponse = matchedFAQ.answer;
    }

    setTimeout(() => {
      setMessages((prev) => [...prev, { from: "bot", text: botResponse }]);
    }, 800);

    setInputValue("");
  };

  return (
    <section className="wow-section bg-gradient-to-br from-blue-50 to-white min-h-screen flex flex-col items-center justify-center p-8">
      <div className="card-style max-w-xl w-full bg-white rounded-3xl shadow-lg border border-blue-200 p-8 text-center">
        <h1 className="text-4xl font-bold mb-4 text-blue-700">Live Support</h1>
        <p className="text-lg text-gray-700 mb-6">
          Get real-time assistance from our cryptography experts, available 24/7.
        </p>
        <button
          className="bg-blue-600 text-white font-semibold py-3 px-8 rounded-xl hover:bg-blue-700 transition-all duration-200 shadow"
          onClick={() => setChatOpen(true)}
          aria-label="Start live chat"
        >
          Start Live Chat
        </button>
      </div>

      {chatOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-60 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-3xl max-w-md w-full shadow-lg flex flex-col overflow-hidden">
            <div className="flex items-center justify-between bg-blue-600 px-6 py-3 text-white font-bold text-lg rounded-t-3xl">
              <span>Qryptify Support Bot</span>
              <button
                onClick={() => setChatOpen(false)}
                className="text-white hover:text-gray-200 transition"
                aria-label="Close chat"
              >
                &times;
              </button>
            </div>

            <div className="flex-1 overflow-y-auto px-6 py-4 space-y-3 max-h-96">
              {messages.map((msg, idx) => (
                <div
                  key={idx}
                  className={`flex ${msg.from === "user" ? "justify-end" : "justify-start"}`}
                >
                  <div
                    className={`rounded-xl px-4 py-2 max-w-xs break-words ${
                      msg.from === "user"
                        ? "bg-blue-600 text-white rounded-br-none"
                        : "bg-gray-200 text-gray-900 rounded-bl-none"
                    }`}
                  >
                    {msg.text}
                  </div>
                </div>
              ))}
              <div ref={bottomRef} />
            </div>

            <div className="flex items-center border-t border-gray-300 px-4 py-3">
              <input
                type="text"
                placeholder="Type your message..."
                className="flex-1 border border-gray-300 rounded-lg py-2 px-4 mr-4 focus:outline-none focus:ring-2 focus:ring-blue-600"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter") handleSend();
                }}
                autoFocus
              />
              <button
                className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition"
                onClick={handleSend}
                aria-label="Send message"
              >
                Send
              </button>
            </div>
          </div>
        </div>
      )}
    </section>
  );
}
