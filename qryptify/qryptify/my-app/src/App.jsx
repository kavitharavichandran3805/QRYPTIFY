// import React, { useState, useEffect } from 'react'
// import { BrowserRouter as Router, Routes, Route, useNavigate } from 'react-router-dom'
// import Navigation from './components/Navigation.jsx'
// import HeroSection from './components/HeroSection.jsx'
// import AboutSection from './components/AboutSection.jsx'
// import HelpSection from './components/HelpSection.jsx'
// import LoginSection from './components/LoginSection.jsx'
// import AnalysisPage from './components/Analysis.jsx'
// import MyAccount from './components/MyAccount.jsx'
// import { api } from './components/api.js'

// // -------- HomePage --------
// function HomePage({ resetDashboardFlag, onResetDashboardFlag }) {
//   const [activeSection, setActiveSection] = useState('home')
//   const [showDashboard, setShowDashboard] = useState(false)
//   const navigate = useNavigate()

//   const handleGetStarted = async () => {
//     try {
//       const result = await api('user-details', 'GET')
//       if (result.status) {
//         setShowDashboard(true)
//       } else {
//         handleNavigate('login')
//       }
//     } catch (error) {
//       handleNavigate('login')
//     }
//   }

//   const handleNavigate = (sectionId) => {
//     setActiveSection(sectionId)
//     if (sectionId === 'dashboard') {
//       setShowDashboard(true)
//       return
//     }
//     setShowDashboard(false)
//     const element = document.getElementById(sectionId)
//     if (element) {
//       element.scrollIntoView({ behavior: 'smooth' })
//     }
//   }

//   // Reset dashboard after logout
//   useEffect(() => {
//     if (resetDashboardFlag) {
//       setShowDashboard(false)
//       if (onResetDashboardFlag) onResetDashboardFlag(false)
//       navigate('/')
//     }
//   }, [resetDashboardFlag, onResetDashboardFlag, navigate])

//   // Track section while scrolling
//   useEffect(() => {
//     if (showDashboard) return
//     const handleScroll = () => {
//       const sections = ['home', 'about', 'help', 'login']
//       const scrollPosition = window.scrollY + 100
//       for (const sectionId of sections) {
//         const element = document.getElementById(sectionId)
//         if (element) {
//           const { offsetTop, offsetHeight } = element
//           if (scrollPosition >= offsetTop && scrollPosition < offsetTop + offsetHeight) {
//             setActiveSection(sectionId)
//             break
//           }
//         }
//       }
//     }
//     window.addEventListener('scroll', handleScroll)
//     return () => window.removeEventListener('scroll', handleScroll)
//   }, [showDashboard])

//   return (
//     <div className="min-h-screen bg-white">
//       {showDashboard
//         ? <AnalysisPage onForceHome={() => onResetDashboardFlag(true)} />
//         : (
//           <>
//             <Navigation activeSection={activeSection} onNavigate={handleNavigate} />
//             <HeroSection onNavigate={handleNavigate} onGetStarted={handleGetStarted} />
//             <AboutSection />
//             <HelpSection />
//             <LoginSection onSuccess={() => handleNavigate('dashboard')} />
//           </>
//         )}
//     </div>
//   )
// }

// // -------- App Routes --------
// export default function App() {
//   const [resetDashboardFlag, setResetDashboardFlag] = useState(false)

//   useEffect(() => {
//     const fetchCSRF = async () => {
//       try {
//         const result = await api('csrf-token', 'GET')
//         if (result.token) {
//           console.log('CSRF token set')
//         } else {
//           console.log('Error in setting up csrf token')
//         }
//       } catch (err) {
//         console.log('Failed to set csrf token')
//       }
//     }
//     fetchCSRF()
//   }, [])

//   return (
//     <Router>
//       <Routes>
//         <Route
//           path="/"
//           element={
//             <HomePage
//               resetDashboardFlag={resetDashboardFlag}
//               onResetDashboardFlag={setResetDashboardFlag}
//             />
//           }
//         />
//         <Route
//           path="/analysis"
//           element={<AnalysisPage onForceHome={() => setResetDashboardFlag(true)} />}
//         />
//         <Route path="/account" element={<MyAccount />} />
//       </Routes>
//     </Router>
//   )
// }
























import React, { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route, useNavigate } from 'react-router-dom'
import Navigation from './components/Navigation.jsx'
import HeroSection from './components/HeroSection.jsx'
import AboutSection from './components/AboutSection.jsx'
import HelpSection from './components/HelpSection.jsx'
import LoginSection from './components/LoginSection.jsx'
import AnalysisPage from './components/Analysis.jsx'
import MyAccount from './components/MyAccount.jsx'
import { api } from './components/api.js'

// -------- HomePage --------
function HomePage({ resetDashboardFlag, onResetDashboardFlag }) {
  const [activeSection, setActiveSection] = useState('home')
  const [showDashboard, setShowDashboard] = useState(false)
  const navigate = useNavigate()

  const handleGetStarted = async () => {
    try {
      const result = await api('user-details', 'GET')
      if (result.status) {
        setShowDashboard(true)
      } else {
        handleNavigate('login')
      }
    } catch (error) {
      handleNavigate('login')
    }
  }

  const handleNavigate = (sectionId) => {
    setActiveSection(sectionId)
    if (sectionId === 'dashboard') {
      setShowDashboard(true)
      return
    }
    setShowDashboard(false)
    const element = document.getElementById(sectionId)
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' })
    }
  }

  // Reset dashboard after logout and always go home
  useEffect(() => {
    if (resetDashboardFlag) {
      setShowDashboard(false)
      if (onResetDashboardFlag) onResetDashboardFlag(false)
      navigate('/')
    }
  }, [resetDashboardFlag, onResetDashboardFlag, navigate])

  useEffect(() => {
    if (showDashboard) return
    const handleScroll = () => {
      const sections = ['home', 'about', 'help', 'login']
      const scrollPosition = window.scrollY + 100
      for (const sectionId of sections) {
        const element = document.getElementById(sectionId)
        if (element) {
          const { offsetTop, offsetHeight } = element
          if (scrollPosition >= offsetTop && scrollPosition < offsetTop + offsetHeight) {
            setActiveSection(sectionId)
            break
          }
        }
      }
    }
    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [showDashboard])

  return (
    <div className="min-h-screen bg-white">
      {showDashboard
        ? <AnalysisPage onForceHome={() => onResetDashboardFlag(true)} />
        : (
          <>
            <Navigation activeSection={activeSection} onNavigate={handleNavigate} />
            <HeroSection onNavigate={handleNavigate} onGetStarted={handleGetStarted} />
            <AboutSection />
            <HelpSection />
            <LoginSection onSuccess={() => handleNavigate('dashboard')} />
          </>
        )}
    </div>
  )
}

// -------- App Routes --------
export default function App() {
  const [resetDashboardFlag, setResetDashboardFlag] = useState(false)

  useEffect(() => {
    const fetchCSRF = async () => {
      try {
        const result = await api('csrf-token', 'GET')
        if (result.token) {
          console.log('CSRF token set')
        } else {
          console.log('Error in setting up csrf token')
        }
      } catch (err) {
        console.log('Failed to set csrf token')
      }
    }
    fetchCSRF()
  }, [])

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
          path="/analysis"
          element={<AnalysisPage onForceHome={() => setResetDashboardFlag(true)} />}
        />
        <Route path="/account" element={<MyAccount />} />
      </Routes>
    </Router>
  )
}
