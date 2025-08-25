// import React, { useState, useEffect } from 'react';
// import Navigation from './components/Navigation.jsx';
// import HeroSection from './components/HeroSection.jsx';
// import AboutSection from './components/AboutSection.jsx';
// import HelpSection from './components/HelpSection.jsx';
// import LoginSection from './components/LoginSection.jsx';

// export default function Home() {
//   const [activeSection, setActiveSection] = useState('home');

//   const handleNavigate = (sectionId) => {
//     setActiveSection(sectionId);
//     const element = document.getElementById(sectionId);
//     if (element) {
//       element.scrollIntoView({ behavior: 'smooth' });
//     }
//   };

//   useEffect(() => {
//     const handleScroll = () => {
//       const sections = ['home', 'about', 'help', 'login'];
//       const scrollPosition = window.scrollY + 100;

//       for (const sectionId of sections) {
//         const element = document.getElementById(sectionId);
//         if (element) {
//           const { offsetTop, offsetHeight } = element;
//           if (scrollPosition >= offsetTop && scrollPosition < offsetTop + offsetHeight) {
//             setActiveSection(sectionId);
//             break;
//           }
//         }
//       }
//     };

//     window.addEventListener('scroll', handleScroll);
//     return () => window.removeEventListener('scroll', handleScroll);
//   }, []);

//   return (
//     <div className="min-h-screen bg-white">
//       <Navigation activeSection={activeSection} onNavigate={handleNavigate} />
//       <HeroSection onNavigate={handleNavigate} />
//       <AboutSection />
//       <HelpSection />
//       <LoginSection />
//     </div>
//   );
// }















// import React, { useState, useEffect } from 'react';
// import Navigation from './components/Navigation.jsx';
// import HeroSection from './components/HeroSection.jsx';
// import AboutSection from './components/AboutSection.jsx';
// import HelpSection from './components/HelpSection.jsx';
// import LoginSection from './components/LoginSection.jsx';

// export default function Home() {
//   const [activeSection, setActiveSection] = useState('home');
//   const [showDashboard, setShowDashboard] = useState(false);

//   const handleNavigate = (sectionId) => {
//     setActiveSection(sectionId);
//     if (sectionId === "dashboard") {
//       setShowDashboard(true);
//       return;
//     }
//     setShowDashboard(false);
//     const element = document.getElementById(sectionId);
//     if (element) {
//       element.scrollIntoView({ behavior: 'smooth' });
//     }
//   };

//   useEffect(() => {
//     if (showDashboard) return;
//     const handleScroll = () => {
//       const sections = ['home', 'about', 'help', 'login'];
//       const scrollPosition = window.scrollY + 100;
//       for (const sectionId of sections) {
//         const element = document.getElementById(sectionId);
//         if (element) {
//           const { offsetTop, offsetHeight } = element;
//           if (scrollPosition >= offsetTop && scrollPosition < offsetTop + offsetHeight) {
//             setActiveSection(sectionId);
//             break;
//           }
//         }
//       }
//     };
//     window.addEventListener('scroll', handleScroll);
//     return () => window.removeEventListener('scroll', handleScroll);
//   }, [showDashboard]);

//   return (
//     <div className="min-h-screen bg-white">
//       {showDashboard ? (
//         // Dashboard/Hello World page
//         <div className="min-h-screen flex items-center justify-center bg-gray-100">
//           <h1 className="text-5xl font-bold text-blue-600">Hello World</h1>
//         </div>
//       ) : (
//         <>
//           <Navigation activeSection={activeSection} onNavigate={handleNavigate} />
//           <HeroSection onNavigate={handleNavigate} />
//           <AboutSection />
//           <HelpSection />
//           <LoginSection onSuccess={() => handleNavigate('dashboard')} />
//         </>
//       )}
//     </div>
//   );
// }



























import React, { useState, useEffect } from 'react';
import Navigation from './components/Navigation.jsx';
import HeroSection from './components/HeroSection.jsx';
import AboutSection from './components/AboutSection.jsx';
import HelpSection from './components/HelpSection.jsx';
import LoginSection from './components/LoginSection.jsx';
import HelloWorld from './components/Analysis.jsx';

export default function Home() {
  const [activeSection, setActiveSection] = useState('home');
  const [showDashboard, setShowDashboard] = useState(false);

  const handleNavigate = (sectionId) => {
    setActiveSection(sectionId);
    if (sectionId === "dashboard") {
      setShowDashboard(true);
      return;
    }
    setShowDashboard(false);
    const element = document.getElementById(sectionId);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  useEffect(() => {
    if (showDashboard) return;
    const handleScroll = () => {
      const sections = ['home', 'about', 'help', 'login'];
      const scrollPosition = window.scrollY + 100;
      for (const sectionId of sections) {
        const element = document.getElementById(sectionId);
        if (element) {
          const { offsetTop, offsetHeight } = element;
          if (scrollPosition >= offsetTop && scrollPosition < offsetTop + offsetHeight) {
            setActiveSection(sectionId);
            break;
          }
        }
      }
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, [showDashboard]);

  return (
    <div className="min-h-screen bg-white">
      {showDashboard ? (
        <HelloWorld />
      ) : (
        <>
          <Navigation activeSection={activeSection} onNavigate={handleNavigate} />
          <HeroSection onNavigate={handleNavigate} />
          <AboutSection />
          <HelpSection />
          {/* Pass onSuccess callback to trigger dashboard view */}
          <LoginSection onSuccess={() => handleNavigate('dashboard')} />
        </>
      )}
    </div>
  );
}






