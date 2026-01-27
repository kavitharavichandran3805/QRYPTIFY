import React, { useState, useContext, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import {
  Shield,
  Mail,
  Lock,
  ArrowRight,
  User,
  CheckCircle,
  XCircle,
  Eye,
  EyeOff,
  UserCircle,
  Hash,
  ChevronDown,
} from 'lucide-react';
import { api } from './api';
import { AuthContext } from '../AuthContext.jsx';

export default function LoginSection({ onSuccess }) {
  const [isSignUp, setIsSignUp] = useState(false);
  const [isForgotPassword, setIsForgotPassword] = useState(false);
  const [showPopup, setShowPopup] = useState(false);

  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    username: '',
    email: '',
    password: '',
    confirmPassword: '',
    role: 'guest', 
    limit: '',
  });

  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [apiStatus, setApiStatus] = useState(null);
  const [rememberMe, setRememberMe] = useState(false);
  const [roleFocused, setRoleFocused] = useState(false);

  const { setAccessToken } = useContext(AuthContext);
  const navigate = useNavigate();
  const roleRef = useRef(null);

  async function login() {
    try {
      const result = await api('login', 'POST', {
        email: formData.email,
        password: formData.password,
        rememberMe,
      });
      if (result.status) {
        setAccessToken(result.access);
        setApiStatus(true);
        setShowPopup(true);
        setTimeout(() => {
          setShowPopup(false);
          if (onSuccess) onSuccess();
          navigate('/');
        }, 2500);
      } else {
        setApiStatus(false);
        setShowPopup(true);
        setTimeout(() => setShowPopup(false), 2500);
      }
    } catch {
      setApiStatus(false);
      setShowPopup(true);
      setTimeout(() => setShowPopup(false), 2500);
    }
  }

  async function signup() {
    try {
      const getUser=await api('user-details','GET');
      if(getUser.status && (getUser.user.role=='admin' || getUser.user.role=='Admin')){
        console.log("Admin creating a account");
        const result = await api('signup', 'POST', {
          first_name: formData.firstName,
          last_name: formData.lastName,
          username: formData.username,
          email: formData.email,
          password: formData.password,
          role: formData.role,
          limit: formData.limit,
          rememberMe,
        });

        if (result.status) {
          setApiStatus(true);
          setShowPopup(true);
          setTimeout(() => {
            setShowPopup(false);
          }, 2500);
        } else {
          setApiStatus(false);
          setShowPopup(true);
          setTimeout(() => setShowPopup(false), 2500);
        }
      }
      else{
        alert("You are not allowed to create an user")
      }
    } catch {
      setApiStatus(false);
      setShowPopup(true);
      setTimeout(() => setShowPopup(false), 2500);
    }
  }

  async function resetPassword() {
    try {
      const result = await api('forgot-password', 'PATCH', {
        email: formData.email,
        newPassword: formData.password,
        confirmPassword: formData.confirmPassword,
      });

      if (result.status) {
        setApiStatus(true);
        setShowPopup(true);
        setTimeout(() => {
          setShowPopup(false);
          setIsForgotPassword(false);
        }, 2500);
      } else {
        setApiStatus(false);
        setShowPopup(true);
        setTimeout(() => setShowPopup(false), 2500);
      }
    } catch {
      setApiStatus(false);
      setShowPopup(true);
      setTimeout(() => setShowPopup(false), 2500);
    }
  }

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.id]: e.target.value });
  };

  const handleRoleClick = () => {
    setRoleFocused(true);
    roleRef.current?.focus();
  };

  const handleRoleFocus = () => {
    setRoleFocused(true);
  };

  const handleRoleBlur = () => {
    setTimeout(() => setRoleFocused(false), 150);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (isForgotPassword) {
      await resetPassword();
    } else if (isSignUp) {
      await signup();
    } else {
      await login();
    }
  };

  return (
    <section
      id="login"
      className="min-h-screen bg-gradient-to-br from-gray-900 via-blue-900 to-cyan-900 flex items-center relative"
    >
      <div className="max-w-7xl mx-auto px-6 py-20 w-full">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          {/* Left Side Info */}
          <div className="text-white space-y-8">
            <div className="space-y-6">
              <h1 className="text-5xl font-bold leading-tight">
                <span className="bg-gradient-to-r from-white to-cyan-300 bg-clip-text text-transparent">
                  Secure Access
                </span>
                <br />
                <span>to Qryptify</span>
              </h1>
              <p className="text-xl text-blue-200 leading-relaxed max-w-lg">
                Join thousands of researchers and security professionals who trust
                Qryptify for their cryptographic analysis needs.
              </p>
            </div>
            <div className="space-y-4">
              <div className="flex items-center gap-3">
                <Shield className="w-5 h-5 text-cyan-400" />
                <span className="text-blue-200">Enterprise-grade security</span>
              </div>
              <div className="flex items-center gap-3">
                <Shield className="w-5 h-5 text-cyan-400" />
                <span className="text-blue-200">Blockchain-verified results</span>
              </div>
              <div className="flex items-center gap-3">
                <Shield className="w-5 h-5 text-cyan-400" />
                <span className="text-blue-200">24/7 expert support</span>
              </div>
            </div>
          </div>

          {/* Right Side Box */}
          <div className="relative">
            <div className="absolute inset-0 bg-gradient-to-r from-cyan-400 to-blue-500 rounded-3xl blur-xl opacity-20"></div>
            <div className="relative bg-white p-8 rounded-3xl shadow-2xl">
              <div className="text-center mb-8">
                <h2 className="text-2xl font-bold text-gray-900 mb-2">
                  {isForgotPassword
                    ? 'Reset Your Password'
                    : isSignUp
                    ? 'Create an Account'
                    : 'Welcome Back'}
                </h2>
                <p className="text-gray-600">
                  {isForgotPassword
                    ? 'Enter your email and set a new password'
                    : isSignUp
                    ? 'Sign up for your Qryptify account'
                    : 'Sign in to your Qryptify account'}
                </p>
              </div>

              {/* Form */}
              <form onSubmit={handleSubmit} className="space-y-6">
                {isSignUp && !isForgotPassword && (
                  <>
                    <div className="grid grid-cols-2 gap-4">
                      <div className="space-y-2">
                        <Label htmlFor="firstName" className="text-gray-700">
                          First Name
                        </Label>
                        <Input
                          id="firstName"
                          type="text"
                          value={formData.firstName}
                          onChange={handleChange}
                          placeholder="First Name"
                          className="h-12 border-gray-300 focus:border-black focus:ring-black"
                          required
                        />
                      </div>
                      <div className="space-y-2">
                        <Label htmlFor="lastName" className="text-gray-700">
                          Last Name
                        </Label>
                        <Input
                          id="lastName"
                          type="text"
                          value={formData.lastName}
                          onChange={handleChange}
                          placeholder="Last Name"
                          className="h-12 border-gray-300 focus:border-black focus:ring-black"
                          required
                        />
                      </div>
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="username" className="text-gray-700">
                        Username
                      </Label>
                      <div className="relative">
                        <User className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                        <Input
                          id="username"
                          type="text"
                          value={formData.username}
                          onChange={handleChange}
                          placeholder="Choose a username"
                          className="pl-10 h-12 border-gray-300 focus:border-black focus:ring-black"
                          required
                        />
                      </div>
                    </div>

                    {/* Role Dropdown - DROPDOWN ITEMS PADDED RIGHT */}
                    <div className="space-y-2">
                      <Label htmlFor="role" className="text-gray-700">
                        Role
                      </Label>
                      <div className="relative">
                        <UserCircle className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400 z-10" />
                        <div 
                          ref={roleRef}
                          className={`pl-10 pr-10 h-12 flex items-center bg-white cursor-pointer transition-all duration-200 border rounded-lg hover:border-gray-400 ${
                            roleFocused 
                              ? 'border-black ring-2 ring-black ring-opacity-30 shadow-md' 
                              : 'border-gray-300'
                          }`}
                          onClick={handleRoleClick}
                          onFocus={handleRoleFocus}
                          onBlur={handleRoleBlur}
                          tabIndex={0}
                          role="button"
                        >
                          <span className={`flex-1 text-sm font-medium transition-colors ${
                            roleFocused ? 'text-gray-900' : 'text-gray-500'
                          }`}>
                            {formData.role.charAt(0).toUpperCase() + formData.role.slice(1)}
                          </span>
                          <ChevronDown className={`w-4 h-4 transition-transform duration-200 ${
                            roleFocused ? 'rotate-180 text-black' : 'text-gray-400'
                          }`} />
                        </div>
                        <select
                          id="role"
                          value={formData.role}
                          onChange={handleChange}
                          onFocus={handleRoleFocus}
                          onBlur={handleRoleBlur}
                          className="absolute inset-0 w-full h-full pl-12 pr-12 opacity-0 cursor-pointer z-20 rounded-lg"
                          style={{ 
                            appearance: 'none',
                            paddingLeft: '2.5rem',
                            paddingRight: '2.5rem'
                          }}
                          required
                        >
                          <option value="guest" style={{ paddingLeft: '2.5rem' }}>Guest</option>
                          <option value="researcher" style={{ paddingLeft: '2.5rem' }}>Researcher</option>
                          <option value="auditor" style={{ paddingLeft: '2.5rem' }}>Auditor</option>
                          <option value="admin" style={{ paddingLeft: '2.5rem' }}>Admin</option>
                        </select>
                      </div>
                    </div>

                    {/* Limit Field - Only for Guest */}
                    {formData.role === 'guest' && (
                      <div className="space-y-2">
                        <Label htmlFor="limit" className="text-gray-700">
                          Limit
                        </Label>
                        <div className="relative">
                          <Hash className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                          <Input
                            id="limit"
                            type="number"
                            min="1"
                            value={formData.limit}
                            onChange={handleChange}
                            placeholder="Enter limit number"
                            className="pl-10 h-12 border-gray-300 focus:border-black focus:ring-black"
                            required
                          />
                        </div>
                      </div>
                    )}
                  </>
                )}

                {/* Email */}
                <div className="space-y-2">
                  <Label htmlFor="email" className="text-gray-700">
                    Email Address
                  </Label>
                  <div className="relative">
                    <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                    <Input
                      id="email"
                      type="email"
                      value={formData.email}
                      onChange={handleChange}
                      placeholder="Enter your email"
                      className="pl-10 h-12 border-gray-300 focus:border-black focus:ring-black"
                      required
                    />
                  </div>
                </div>

                {/* Password */}
                {!isForgotPassword && (
                  <div className="space-y-2">
                    <Label htmlFor="password" className="text-gray-700">
                      Password
                    </Label>
                    <div className="relative">
                      <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                      <Input
                        id="password"
                        type={showPassword ? 'text' : 'password'}
                        value={formData.password}
                        onChange={handleChange}
                        placeholder="Enter your password"
                        className="pl-10 pr-10 h-12 border-gray-300 focus:border-black focus:ring-black"
                        required
                      />
                      <button
                        type="button"
                        onClick={() => setShowPassword(!showPassword)}
                        className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
                      >
                        {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                      </button>
                    </div>
                  </div>
                )}

                {/* Forgot Password */}
                {isForgotPassword && (
                  <>
                    <div className="space-y-2">
                      <Label htmlFor="password" className="text-gray-700">
                        New Password
                      </Label>
                      <div className="relative">
                        <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                        <Input
                          id="password"
                          type={showPassword ? 'text' : 'password'}
                          value={formData.password}
                          onChange={handleChange}
                          placeholder="Enter new password"
                          className="pl-10 pr-10 h-12 border-gray-300 focus:border-black focus:ring-black"
                          required
                        />
                        <button
                          type="button"
                          onClick={() => setShowPassword(!showPassword)}
                          className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
                        >
                          {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                        </button>
                      </div>
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="confirmPassword" className="text-gray-700">
                        Confirm Password
                      </Label>
                      <div className="relative">
                        <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                        <Input
                          id="confirmPassword"
                          type={showConfirmPassword ? 'text' : 'password'}
                          value={formData.confirmPassword}
                          onChange={handleChange}
                          placeholder="Confirm your new password"
                          className="pl-10 pr-10 h-12 border-gray-300 focus:border-black focus:ring-black"
                          required
                        />
                        <button
                          type="button"
                          onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                          className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
                        >
                          {showConfirmPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                        </button>
                      </div>
                    </div>
                  </>
                )}

                {/* Remember Me + Forgot Password */}
                {!isForgotPassword && !isSignUp && (
                  <div className="flex items-center justify-between">
                    <label className="flex items-center">
                      <input
                        type="checkbox"
                        checked={rememberMe}
                        onChange={(e) => setRememberMe(e.target.checked)}
                        className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                      />
                      <span className="ml-2 text-sm text-gray-600">Remember me</span>
                    </label>

                    <button
                      type="button"
                      onClick={() => setIsForgotPassword(true)}
                      className="text-sm text-blue-600 hover:text-blue-700"
                    >
                      Forgot password?
                    </button>
                  </div>
                )}

                <Button
                  type="submit"
                  className="w-full h-12 bg-gradient-to-r from-blue-600 to-cyan-500 hover:from-blue-700 hover:to-cyan-600 text-white font-semibold shadow-lg"
                >
                  {isForgotPassword
                    ? 'Reset Password'
                    : isSignUp
                    ? 'Create User'
                    : 'Sign In'}
                  <ArrowRight className="w-5 h-5 ml-2" />
                </Button>
              </form>

              {/* Toggle between login/signup */}
              {!isForgotPassword && (
                <div className="mt-8 pt-6 border-t border-gray-200 text-center">
                  <p className="text-gray-600">
                    {isSignUp ? (
                      <>
                        Already have an account?{' '}
                        <button
                          onClick={() => setIsSignUp(false)}
                          className="text-blue-600 hover:text-blue-700 font-medium"
                        >
                          Sign in
                        </button>
                      </>
                    ) : (
                      <>
                        Admin access required | {' '}
                        <button
                          onClick={() => setIsSignUp(true)}
                          className="text-blue-600 hover:text-blue-700 font-medium"
                        >
                          Create a new user account
                        </button>
                      </>
                    )}
                  </p>
                </div>
              )}

              {/* Back to login from forgot password */}
              {isForgotPassword && (
                <div className="mt-6 text-center">
                  <button
                    onClick={() => setIsForgotPassword(false)}
                    className="text-sm text-blue-600 hover:text-blue-700 font-medium"
                  >
                    ← Back to login
                  </button>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Popup Overlay */}
        {showPopup && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 transition-opacity">
            <div className="bg-white rounded-2xl shadow-2xl p-8 text-center animate-fadeIn max-w-sm w-full">
              {apiStatus ? (
                <>
                  <div className="flex items-center justify-center mb-4">
                    <div className="bg-green-100 p-3 rounded-full">
                      <CheckCircle className="w-12 h-12 text-green-500 animate-bounce" />
                    </div>
                  </div>
                  <h3 className="text-xl font-semibold text-gray-900">
                    {isSignUp
                      ? 'User created successfully!'
                      : isForgotPassword
                      ? 'Password reset successful!'
                      : 'Logged in successfully!'}
                  </h3>
                </>
              ) : (
                <>
                  <div className="flex items-center justify-center mb-4">
                    <div className="bg-red-100 p-3 rounded-full">
                      <XCircle className="w-12 h-12 text-red-600 animate-shake" />
                    </div>
                  </div>
                  <h3 className="text-xl font-semibold text-red-700">
                    {isSignUp
                      ? 'Unable to create user!'
                      : isForgotPassword
                      ? 'Password reset failed!'
                      : 'Login failed!'}
                  </h3>
                  <p className="text-sm text-gray-500 mt-2">
                    Please try again.
                  </p>
                </>
              )}
            </div>
          </div>
        )}
      </div>
    </section>
  );
}