import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navigation from "./components/Navigation.jsx";
import HeroSection from "./components/HeroSection.jsx";
import AboutSection from "./components/AboutSection.jsx";
import HelpSection from "./components/HelpSection.jsx";
import LoginSection from "./components/LoginSection.jsx";
import AnalysisPage from "./components/Analysis.jsx";
import MyAccount from "./components/MyAccount.jsx";
import Explore from "./components/Explore.jsx";
import Updates from "./components/Updates.jsx";
import Ping from "./components/Ping.jsx";
import Read from "./components/Read.jsx";
import { api } from "./components/api.js";

function HomePage({ resetDashboardFlag, onResetDashboardFlag }) {
  const [activeSection, setActiveSection] = useState("home");
  const [showDashboard, setShowDashboard] = useState(false);

  // Smooth scroll to login section
  const handleGetStarted = async () => {
  try {
    const result = await api("user-details", "GET"); // check if user is logged in
    if (result.status) {
      setShowDashboard(true); // logged in → show AnalysisPage
    } else {
      const loginSection = document.getElementById("login");
      if (loginSection) {
        loginSection.scrollIntoView({ behavior: "smooth" }); // not logged in → scroll to login
      }
    }
  } catch (err) {
    const loginSection = document.getElementById("login");
    if (loginSection) {
      loginSection.scrollIntoView({ behavior: "smooth" });
    }
  }
};


  // Navigation among home page sections
  const handleNavigate = (sectionId) => {
    setActiveSection(sectionId);
    if (sectionId === "dashboard") {
      setShowDashboard(true);
      return;
    }
    setShowDashboard(false);
    const element = document.getElementById(sectionId);
    if (element) {
      element.scrollIntoView({ behavior: "smooth" });
    }
  };

  useEffect(() => {
    if (resetDashboardFlag) {
      setShowDashboard(false);
      if (onResetDashboardFlag) onResetDashboardFlag(false);
    }
  }, [resetDashboardFlag, onResetDashboardFlag]);

  useEffect(() => {
    if (showDashboard) return;
    const handleScroll = () => {
      const sections = ["home", "about", "help", "login"];
      const scrollPosition = window.scrollY + 100;
      for (const sectionId of sections) {
        const element = document.getElementById(sectionId);
        if (element) {
          const { offsetTop, offsetHeight } = element;
          if (
            scrollPosition >= offsetTop &&
            scrollPosition < offsetTop + offsetHeight
          ) {
            setActiveSection(sectionId);
            break;
          }
        }
      }
    };
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, [showDashboard]);

  return (
    <div className="min-h-screen w-full">
      {showDashboard ? (
        <AnalysisPage onForceHome={() => onResetDashboardFlag(true)} />
      ) : (
        <>
          <Navigation active={activeSection} onNavigate={handleNavigate} />
          <HeroSection onGetStarted={handleGetStarted} />
          <AboutSection />
          <HelpSection />
          <LoginSection onSuccess={() => handleNavigate("dashboard")} />
        </>
      )}
    </div>
  );
}

export default function App() {
  const [resetDashboardFlag, setResetDashboardFlag] = useState(false);

  useEffect(() => {
    const fetchCSRF = async () => {
      try {
        const result = await api("csrf-token", "GET");
        if (result.token) {
          console.log("CSRF token set");
        } else {
          console.log("Error in setting up csrf token");
        }
      } catch (err) {
        console.log("Failed to set csrf token");
      }
    };
    fetchCSRF();
  }, []);

  return (
    <Router>
      <Routes>
        <Route
          path="/"
          element={
            <HomePage
              resetDashboardFlag={resetDashboardFlag}
              onResetDashboardFlag={setResetDashboardFlag}
            />
          }
        />
        <Route
          path="/dashboard"
          element={<AnalysisPage onLogout={() => setResetDashboardFlag(true)} />}
        />
        <Route path="/account" element={<MyAccount />} />

        {/* New routes for cards */}
        <Route path="/explore" element={<Explore />} />
        <Route path="/updates" element={<Updates />} />
        <Route path="/ping" element={<Ping />} />
        <Route path="/read" element={<Read />} />

        {/* Catch-all 404 */}
        <Route
          path="*"
          element={<div className="text-2xl text-center mt-24">404 Not Found</div>}
        />
      </Routes>
    </Router>
  );
}
