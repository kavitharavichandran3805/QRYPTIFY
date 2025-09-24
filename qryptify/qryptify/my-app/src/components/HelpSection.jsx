import React, { useContext, useState } from 'react'
import {
  MessageCircle,
  FileText,
  Video,
  Users,
  ArrowRight,
  HelpCircle,
  Sparkles,
  CheckCircle,
} from "lucide-react";
import { Button } from "../components/ui/button";
import { api } from "./api.js";
import { AuthContext } from '../AuthContext.jsx';
import { useNavigate } from 'react-router-dom'

export default function HelpSection() {
  const [showContactForm, setShowContactForm] = useState(false);
  const [showSuccessPopup, setShowSuccessPopup] = useState(false);
  const [query, setQuery] = useState("");
  const { accessToken } = useContext(AuthContext)
  const navigate = useNavigate()

  const checkUser = async () => {
    try {
      const result = await api("user-details", "GET", null, accessToken);
      if (result.status) {
        setShowContactForm(true)
      } else {
        handleContactClick()
      }
    } catch (err) {
      handleContactClick()
    }
  }

  const handleSendQuery = async () => {
    try {
      const send_mail = await api("issue-mail", "POST", { message: query }, accessToken);
      if (send_mail.status) {
        setShowContactForm(false);
        setShowSuccessPopup(true);
        setTimeout(() => {
          setShowSuccessPopup(false);
          setQuery("");
        }, 2500);
      }
    } catch (err) {
      navigate("/login");
    }
  };

  const helpResources = [
    {
      icon: <FileText className="w-6 h-6" />,
      title: "Knowledge Base",
      description:
        "Access a curated collection of FAQs, troubleshooting tips, and best practices to help you resolve common questions quickly.",
      action: "Explore Resources",
      path: "/explore"
    },
    {
      icon: <Video className="w-6 h-6" />,
      title: "Product Updates",
      description:
        "Stay informed with the latest Qryptify enhancements, feature releases, and cryptography insights directly from our team.",
      action: "See Updates",
      path: "/updates"
    },
    {
      icon: <MessageCircle className="w-6 h-6" />,
      title: "Live Support",
      description:
        "Get real-time assistance from our cryptography experts available 24/7 to help with your analysis needs.",
      action: "Ping Us",
      path: "/ping"
    },
    {
      icon: <Users className="w-6 h-6" />,
      title: "Whitepapers & Research",
      description:
        "Dive into in-depth papers and technical research highlighting cryptographic methodologies behind Qryptify.",
      action: "Read More",
      path: "/read"
    },
  ];

  const faqs = [
    {
      question: "What types of encrypted data can Qryptify analyze?",
      answer:
        "Qryptify can analyze various forms of encrypted data including files, network traffic, cryptographic keys, and digital signatures. It supports both classical and post-quantum encryption methods.",
    },
    {
      question: "How accurate is the AI algorithm detection?",
      answer:
        "Our AI achieves 85% accuracy in cryptographic algorithm identification, trained on thousands of encryption implementations and continuously updated with new cryptographic methods.",
    },
    {
      question: "Is my data secure during analysis?",
      answer:
        "Absolutely. All data is processed in secure, isolated environments with end-to-end encryption. We never store your encrypted data, and all analysis results are recorded on blockchain for transparency.",
    },
    {
      question: "Can I integrate Qryptify with my existing systems?",
      answer:
        "No, Qryptify is designed as a standalone platform with its own secure environment. To maintain maximum security and prevent dependency risks, it does not integrate directly with external systems or third-party infrastructures.",
    },
  ];

  const handleContactClick = () => {
    const loginSection = document.getElementById('login');
    if (loginSection) {
      loginSection.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <section
      id="help"
      className="py-20 bg-gradient-to-br from-gray-50 to-blue-50 relative"
    >
      <div className="max-w-7xl mx-auto px-6">
        {/* Header */}
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-gray-900 mb-4">
            Get the Help You Need
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Whether you're new to cryptographic analysis or an experienced
            researcher, we provide comprehensive support to help you succeed
            with Qryptify.
          </p>
        </div>

        {/* Help Resources Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mb-20">
          {helpResources.map((resource, index) => (
            <div
              key={index}
              className="bg-white p-6 rounded-2xl border border-gray-200 hover:shadow-lg transition-all duration-300 group cursor-pointer"
              onClick={() => navigate(resource.path)}
            >
              <div className="text-blue-600 mb-4 group-hover:scale-110 transition-transform duration-300">
                {resource.icon}
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-3">
                {resource.title}
              </h3>
              <p className="text-gray-600 mb-4 leading-relaxed">
                {resource.description}
              </p>
              <div className="flex items-center text-blue-600 font-medium group-hover:text-blue-700">
                <span>{resource.action}</span>
                <ArrowRight className="w-4 h-4 ml-2 group-hover:translate-x-1 transition-transform duration-200" />
              </div>
            </div>
          ))}
        </div>

        {/* FAQs + Support Section */}
        <div className="grid lg:grid-cols-2 gap-12 items-stretch">
          {/* FAQ Section */}
          <div>
            <h3 className="text-3xl font-bold text-gray-900 mb-8 flex items-center gap-3">
              <HelpCircle className="w-8 h-8 text-blue-600" />
              Frequently Asked Questions
            </h3>
            <div className="space-y-6">
              {faqs.map((faq, index) => (
                <div
                  key={index}
                  className="bg-white p-6 rounded-xl border border-gray-200"
                >
                  <h4 className="text-lg font-semibold text-gray-900 mb-3">
                    {faq.question}
                  </h4>
                  <p className="text-gray-600 leading-relaxed">{faq.answer}</p>
                </div>
              ))}
            </div>
          </div>

          {/* Personalized Support Section */}
          <div className="bg-gradient-to-br from-blue-600 to-cyan-500 p-8 rounded-3xl text-white flex flex-col justify-between min-h-full">

            <h3 className="text-2xl font-bold mb-4">
              Need Personalized Support?
            </h3>
            <div className="space-y-6 mb-8">
              <div className="flex items-start gap-3">
                <Sparkles className="w-5 h-5 text-cyan-300 animate-pulse flex-shrink-0" />
                <p className="text-blue-100 leading-relaxed">
                  Our team of cryptography experts is here — not just to provide
                  technology, but to truly understand your challenges and craft
                  a Qryptify experience that fits your world.
                </p>
              </div>
              <div className="flex items-start gap-3">
                <Sparkles className="w-5 h-5 text-cyan-300 animate-pulse flex-shrink-0" />
                <p className="text-blue-100 leading-relaxed">
                  From the very first conversation, we work alongside you,
                  listening to your goals and mapping out how Qryptify can best
                  protect what matters most.
                </p>
              </div>
              <div className="flex items-start gap-3">
                <Sparkles className="w-5 h-5 text-cyan-300 animate-pulse flex-shrink-0" />
                <p className="text-blue-100 leading-relaxed">
                  Every organization is different, and so is the way we approach
                  your implementation — with care, precision, and solutions
                  designed exclusively for you.
                </p>
              </div>
            </div>

            <div className="flex items-start gap-3 mb-8">
              <Sparkles className="w-5 h-5 text-cyan-300 animate-pulse flex-shrink-0" />
              <p className="text-blue-100 leading-relaxed">
                With our dedicated guidance, you gain more than support; you
                gain a trusted partner who ensures Qryptify becomes a seamless
                part of your ecosystem, empowering you with confidence,
                resilience, and peace of mind.
              </p>
            </div>

            {/* Extra Benefits List */}
            <ul className="list-disc list-inside space-y-2 mb-8 text-blue-100">
              <li>1-on-1 implementation guidance</li>
              <li>Custom integration solutions</li>
              <li>Priority technical support</li>
            </ul>

            {/* Call to Action Button */}
            <Button
              onClick={() => checkUser()}
              className="bg-white text-blue-600 hover:bg-blue-50 px-8"
            >
              Contact Expert Team
            </Button>
          </div>
        </div>
      </div>

      {/* Contact Form Modal */}
      {showContactForm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 transition-opacity">
          <div className="bg-white rounded-2xl shadow-2xl p-8 max-w-md w-full animate-fadeIn">
            <h3 className="text-2xl font-bold text-gray-900 mb-6">
              Contact Expert Team
            </h3>
            <textarea
              placeholder="Write your query..."
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              rows={6}
              className="w-full border border-gray-300 rounded-lg p-3 mb-6 focus:outline-none focus:ring-2 focus:ring-blue-500"
            ></textarea>
            <div className="flex justify-end gap-4">
              <Button
                onClick={() => setShowContactForm(false)}
                className="bg-gray-100 text-gray-700 hover:bg-gray-200"
              >
                Cancel
              </Button>
              <Button
                onClick={handleSendQuery}
                className="bg-blue-600 text-white hover:bg-blue-700"
              >
                Send Query
              </Button>
            </div>
          </div>
        </div>
      )}

      {/* Success Popup */}
      {showSuccessPopup && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 transition-opacity">
          <div className="bg-white rounded-2xl shadow-2xl p-8 text-center animate-fadeIn max-w-sm w-full">
            <div className="flex items-center justify-center mb-4">
              <div className="bg-green-100 p-3 rounded-full">
                <CheckCircle className="w-12 h-12 text-green-500 animate-bounce" />
              </div>
            </div>
            <h3 className="text-xl font-semibold text-gray-900">
              Query Sent Successfully!
            </h3>
            <p className="mt-2 text-gray-600">
              Our experts will reach out to you shortly.
            </p>
          </div>
        </div>
      )}
    </section>
  );
}
