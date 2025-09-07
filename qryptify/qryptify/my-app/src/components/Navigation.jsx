import React, { useState } from 'react';
import { useNavigate } from "react-router-dom";
import { Button } from '../components/ui/button';
import { Menu, X } from 'lucide-react';
import Logo from './Logo';
import {api} from './api.js';

export default function Navigation({ activeSection, onNavigate }) {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const navigate = useNavigate();

  const navItems = [
    { id: 'home', label: 'Home' },
    { id: 'about', label: 'About' },
    { id: 'help', label: 'Help' }
  ];

  const handleNavClick = (sectionId) => {
    onNavigate(sectionId);
    setIsMobileMenuOpen(false);
  };


  const handleLoginClick=async()=>{
    try {
          console.log("inside the handleLoginClick")
          const result = await api('user-details', 'GET')
          if (result.status) {
            navigate('/analysis')
          } else {
            handleNavClick('login')
          }
        } catch (error) {
          console.error('API error:', error)
          handleNavClick('login')
        }
  }

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-white/80 backdrop-blur-xl border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-6">
        <div className="flex items-center justify-between h-16">
          <Logo />
          <div className="hidden md:flex items-center space-x-8">
            {navItems.map((item) => (
              <button
                key={item.id}
                onClick={() => handleNavClick(item.id)}
                className={`text-sm font-medium transition-colors duration-200 ${
                  activeSection === item.id 
                    ? 'text-blue-600' 
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                {item.label}
              </button>
            ))}
            <Button 
              className="bg-gradient-to-r from-blue-600 to-cyan-500 hover:from-blue-700 hover:to-cyan-600 text-white px-6 shadow-lg"
              onClick={() => handleLoginClick()}
            >
              Login
            </Button>
          </div>
          <button
            className="md:hidden p-2"
            onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
          >
            {isMobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </div>
        {isMobileMenuOpen && (
          <div className="md:hidden py-4 border-t border-gray-200">
            {navItems.map((item) => (
              <button
                key={item.id}
                onClick={() => handleNavClick(item.id)}
                className={`block w-full text-left px-4 py-2 text-sm font-medium transition-colors duration-200 ${
                  activeSection === item.id 
                    ? 'text-blue-600 bg-blue-50' 
                    : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'
                }`}
              >
                {item.label}
              </button>
            ))}
            <div className="px-4 pt-2">
              <Button 
                className="w-full bg-gradient-to-r from-blue-600 to-cyan-500 hover:from-blue-700 hover:to-cyan-600 text-white shadow-lg"
                onClick={() => handleLoginClick()}
              >
                Login
              </Button>
            </div>
          </div>
        )}
      </div>
    </nav>
  );
}