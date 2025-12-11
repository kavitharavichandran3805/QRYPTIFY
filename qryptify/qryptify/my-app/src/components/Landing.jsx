

import React, { useCallback } from "react";
import HeroSection from "../components/HeroSection";
import HelpSection from "../components/HelpSection";

export default function Landing() {
  const handleNavigate = useCallback((target) => {
    if (target === "faq") {
      const el = document.getElementById("faq");
      if (el) {
        const rect = el.getBoundingClientRect();
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        const offset = 120; // adjust if you want it higher/lower
        window.scrollTo({
          top: rect.top + scrollTop - offset,
          behavior: "smooth",
        });
      }
    }
  }, []);

  const handleGetStarted = useCallback(() => {
    const el = document.getElementById("login");
    if (el) {
      el.scrollIntoView({ behavior: "smooth" });
    }
  }, []);

  return (
    <>
      <HeroSection onNavigate={handleNavigate} onGetStarted={handleGetStarted} />
      <HelpSection />
    </>
  );
}
