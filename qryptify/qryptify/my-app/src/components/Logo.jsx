import React from "react";

export default function Logo({ className = "" }) {
  return (
    <>
      <style>{`
        @keyframes crypto-float {
          0%, 100% { transform: translateY(0px) rotateX(10deg); }
          50% { transform: translateY(-4px) rotateX(-10deg); }
        }
        @keyframes crypto-rotate {
          from { transform: rotateZ(0deg); }
          to { transform: rotateZ(360deg); }
        }
        @keyframes crypto-pulse {
          0%, 100% {
            opacity: 1;
            transform: translate(-50%, -50%) translateZ(12px) scale(1);
            box-shadow: 0 0 12px rgba(59, 130, 246, 0.8);
          }
          50% {
            opacity: 0.7;
            transform: translate(-50%, -50%) translateZ(12px) scale(1.2);
            box-shadow: 0 0 20px rgba(59, 130, 246, 1);
          }
        }
        @keyframes crypto-orbit {
          from {
            transform: rotate(0deg) translateX(20px) rotate(0deg);
            opacity: 1;
          }
          to {
            transform: rotate(360deg) translateX(20px) rotate(-360deg);
            opacity: 0.3;
          }
        }
        @keyframes crypto-glow-pulse {
          0%, 100% {
            opacity: 0.3;
            transform: scale(1);
          }
          50% {
            opacity: 0.6;
            transform: scale(1.1);
          }
        }
        .crypto-logo-container {
          perspective: 1000px;
          position: relative;
        }
        .crypto-hexagon {
          width: 32px; 
          height: 32px;
          position: relative;
          transform-style: preserve-3d;
          animation: crypto-float 6s ease-in-out infinite;
        }
        .hex-layer {
          position: absolute;
          width: 100%;
          height: 100%;
          clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);
          animation: crypto-rotate 12s linear infinite;
          border-radius: 0.5rem;
        }
        .hex-layer-1 {
          background: linear-gradient(45deg, #3b82f6, #06b6d4);
          transform: translateZ(8px);
          animation-delay: 0s;
        }
        .hex-layer-2 {
          background: linear-gradient(45deg, #8b5cf6, #06b6d4);
          transform: translateZ(4px) scale(0.85);
          animation-delay: -2s;
          opacity: 0.8;
        }
        .hex-layer-3 {
          background: linear-gradient(45deg, #ec4899, #f59e0b);
          transform: translateZ(0px) scale(0.7);
          animation-delay: -4s;
          opacity: 0.6;
        }
        .crypto-core {
          position: absolute;
          top: 50%;
          left: 50%;
          width: 8px;
          height: 8px;
          background: linear-gradient(45deg, #ffffff, #f0f9ff);
          border-radius: 9999px;
          transform: translate(-50%, -50%) translateZ(12px);
          box-shadow: 0 0 12px rgba(59, 130, 246, 0.8);
          animation: crypto-pulse 3s ease-in-out infinite;
        }
        .crypto-particles {
          position: absolute;
          inset: -8px;
          pointer-events: none;
        }
        .particle {
          position: absolute;
          width: 2px;
          height: 2px;
          background: #06b6d4;
          border-radius: 9999px;
          animation: crypto-orbit 8s linear infinite;
        }
        .particle:nth-child(1) {
          animation-delay: 0s;
          top: 0;
          left: 50%;
        }
        .particle:nth-child(2) {
          animation-delay: -2s;
          top: 25%;
          right: 0;
        }
        .particle:nth-child(3) {
          animation-delay: -4s;
          bottom: 0;
          left: 50%;
        }
        .particle:nth-child(4) {
          animation-delay: -6s;
          top: 25%;
          left: 0;
        }
        .crypto-glow {
          position: absolute;
          inset: -6px;
          background: radial-gradient(circle, rgba(59, 130, 246, 0.2) 0%, transparent 70%);
          border-radius: 9999px;
          animation: crypto-glow-pulse 4s ease-in-out infinite;
        }
      `}</style>

      <div className={`flex items-center gap-3 mt-1 ${className}`}>
        <div className="crypto-logo-container w-8 h-8 relative">
          <div className="crypto-glow"></div>

          <div className="crypto-hexagon">
            <div className="hex-layer hex-layer-1 rounded-md"></div>
            <div className="hex-layer hex-layer-2 rounded-md"></div>
            <div className="hex-layer hex-layer-3 rounded-md"></div>
            <div className="crypto-core"></div>
          </div>

          <div className="crypto-particles">
            <div className="particle"></div>
            <div className="particle"></div>
            <div className="particle"></div>
            <div className="particle"></div>
          </div>
        </div>

        <span className="text-xl font-bold bg-gradient-to-r from-blue-600 via-purple-600 to-cyan-500 bg-clip-text text-transparent">
          Qryptify
        </span>
      </div>
    </>
  );
}