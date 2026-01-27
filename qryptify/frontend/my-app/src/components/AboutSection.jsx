import React from 'react';
import { Cpu, Shield, Zap, Database, CheckCircle, Lock } from 'lucide-react';

export default function AboutSection() {
  const features = [
    {
      icon: <Cpu className="w-8 h-8" />,
      title: "AI-Powered Analysis",
      description: "Advanced machine learning algorithms identify cryptographic patterns with unprecedented accuracy, supporting both classical and post-quantum encryption methods."
    },
    {
      icon: <Database className="w-8 h-8" />,
      title: "Blockchain Security",
      description: "Every analysis result is immutably recorded on blockchain, providing transparent, tamper-proof verification of cryptographic discoveries."
    },
    {
      icon: <Zap className="w-8 h-8" />,
      title: "Real-time Processing",
      description: "Get instant results with our optimized processing engine that can handle complex encrypted datasets in seconds, not hours."
    },
    {
      icon: <Shield className="w-8 h-8" />,
      title: "Enterprise Security",
      description: "Built with enterprise-grade security standards, ensuring your sensitive data remains protected throughout the analysis process."
    }
  ];

  const capabilities = [
    "Classical encryption algorithms (RSA, AES, DES)",
    "Post-quantum cryptography (Kyber, Dilithium, SPHINCS+)",
    "Elliptic curve cryptography (ECDSA, ECDH)",
    "Hash functions and digital signatures",
    "Hybrid encryption schemes",
    "Custom and proprietary algorithms"
  ];

  return (
    <section id="about" className="py-20 bg-white">
      <div className="max-w-7xl mx-auto px-6">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-gray-900 mb-4">
            Advanced Cryptographic Intelligence
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Qryptify represents the next generation of cryptographic analysis, combining artificial intelligence 
            with blockchain technology to provide unparalleled insights into encrypted data systems.
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8 mb-20">
          {features.map((feature, index) => (
            <div key={index} className="group">
              <div className="bg-gradient-to-br from-blue-50 to-cyan-50 p-8 rounded-2xl border border-blue-100 hover:shadow-lg transition-all duration-300 h-full">
                <div className="text-blue-600 mb-4 group-hover:scale-110 transition-transform duration-300">
                  {feature.icon}
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-3">
                  {feature.title}
                </h3>
                <p className="text-gray-600 leading-relaxed">
                  {feature.description}
                </p>
              </div>
            </div>
          ))}
        </div>

        <div className="grid lg:grid-cols-2 gap-12 items-center">
          <div>
            <h3 className="text-3xl font-bold text-gray-900 mb-6">
              Comprehensive Algorithm Detection
            </h3>
            <p className="text-lg text-gray-600 mb-8">
              Our AI engine is trained on thousands of cryptographic implementations, 
              enabling it to identify and classify both traditional and cutting-edge encryption methods.
            </p>
            
            <div className="space-y-3">
              {capabilities.map((capability, index) => (
                <div key={index} className="flex items-center gap-3">
                  <CheckCircle className="w-5 h-5 text-green-500 flex-shrink-0" />
                  <span className="text-gray-700">{capability}</span>
                </div>
              ))}
            </div>
          </div>

          <div className="relative">
            <div className="absolute inset-0 bg-gradient-to-br from-blue-400 to-purple-500 rounded-3xl blur-2xl opacity-20"></div>
            <div className="relative bg-gradient-to-br from-gray-900 to-blue-900 p-8 rounded-3xl text-white">
              <div className="flex items-center gap-3 mb-6">
                <Lock className="w-6 h-6 text-blue-400" />
                <span className="font-semibold">Blockchain Verification</span>
              </div>
              
              <div className="space-y-4 font-mono text-sm">
                <div className="bg-black/20 p-3 rounded-lg">
                  <div className="text-green-400">Block #847291</div>
                  <div className="text-gray-300">Hash: 0x7f3e4d2a...</div>
                  <div className="text-blue-400">Algorithm: Kyber-1024</div>
                </div>
                
                <div className="bg-black/20 p-3 rounded-lg">
                  <div className="text-green-400">Block #847290</div>
                  <div className="text-gray-300">Hash: 0x9b1c8f5e...</div>
                  <div className="text-blue-400">Algorithm: RSA-4096</div>
                </div>
                
                <div className="bg-black/20 p-3 rounded-lg">
                  <div className="text-green-400">Block #847289</div>
                  <div className="text-gray-300">Hash: 0x2d7a3e9c...</div>
                  <div className="text-blue-400">Algorithm: ECDSA-P384</div>
                </div>
              </div>
              
              <div className="mt-6 text-center">
                <div className="text-2xl font-bold text-blue-400">100%</div>
                <div className="text-sm text-gray-300">Tamper-proof Results</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}