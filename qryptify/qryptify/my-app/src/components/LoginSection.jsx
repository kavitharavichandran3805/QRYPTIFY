/*
import React, { useState } from 'react';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { Shield, Mail, Lock, ArrowRight } from 'lucide-react';

export default function LoginSection() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    // Login functionality would be implemented here
    console.log('Login attempt:', { email, password });
  };

  return (
    <section id="login" className="min-h-screen bg-gradient-to-br from-gray-900 via-blue-900 to-cyan-900 flex items-center">
      <div className="max-w-7xl mx-auto px-6 py-20 w-full">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
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

          <div className="relative">
            <div className="absolute inset-0 bg-gradient-to-r from-cyan-400 to-blue-500 rounded-3xl blur-xl opacity-20"></div>
            <div className="relative bg-white p-8 rounded-3xl shadow-2xl">
              <div className="text-center mb-8">
                <h2 className="text-2xl font-bold text-gray-900 mb-2">Welcome Back</h2>
                <p className="text-gray-600">Sign in to your Qryptify account</p>
              </div>

              <form onSubmit={handleSubmit} className="space-y-6">
                <div className="space-y-2">
                  <Label htmlFor="email" className="text-gray-700">Email Address</Label>
                  <div className="relative">
                    <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                    <Input
                      id="email"
                      type="email"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      className="pl-10 h-12 border-gray-300 focus:border-blue-500 focus:ring-blue-500"
                      placeholder="Enter your email"
                      required
                    />
                  </div>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="password" className="text-gray-700">Password</Label>
                  <div className="relative">
                    <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                    <Input
                      id="password"
                      type="password"
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      className="pl-10 h-12 border-gray-300 focus:border-blue-500 focus:ring-blue-500"
                      placeholder="Enter your password"
                      required
                    />
                  </div>
                </div>

                <div className="flex items-center justify-between">
                  <label className="flex items-center">
                    <input type="checkbox" className="rounded border-gray-300 text-blue-600 focus:ring-blue-500" />
                    <span className="ml-2 text-sm text-gray-600">Remember me</span>
                  </label>
                  <button type="button" className="text-sm text-blue-600 hover:text-blue-700">
                    Forgot password?
                  </button>
                </div>

                <Button 
                  type="submit"
                  className="w-full h-12 bg-gradient-to-r from-blue-600 to-cyan-500 hover:from-blue-700 hover:to-cyan-600 text-white font-semibold shadow-lg"
                >
                  Sign In
                  <ArrowRight className="w-5 h-5 ml-2" />
                </Button>
              </form>

              <div className="mt-8 pt-6 border-t border-gray-200 text-center">
                <p className="text-gray-600">
                  Don't have an account?{' '}
                  <button className="text-blue-600 hover:text-blue-700 font-medium">
                    Sign up for free
                  </button>
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
  */





















import React, { useState } from 'react';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { Shield, Mail, Lock, ArrowRight, User } from 'lucide-react';

export default function LoginSection() {
  const [isSignUp, setIsSignUp] = useState(false);
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    username: '',
    email: '',
    password: '',
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.id]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (isSignUp) {
      console.log('Sign Up attempt:', formData);
    } else {
      console.log('Login attempt:', {
        email: formData.email,
        password: formData.password,
      });
    }
  };

  return (
    <section id="login" className="min-h-screen bg-gradient-to-br from-gray-900 via-blue-900 to-cyan-900 flex items-center">
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
                  {isSignUp ? 'Create an Account' : 'Welcome Back'}
                </h2>
                <p className="text-gray-600">
                  {isSignUp ? 'Sign up for your Qryptify account' : 'Sign in to your Qryptify account'}
                </p>
              </div>

              {/* Form */}
              <form onSubmit={handleSubmit} className="space-y-6">
                {isSignUp && (
                  <>
                    {/* First Name & Last Name in Same Row */}
                    <div className="grid grid-cols-2 gap-4">
                      <div className="space-y-2">
                        <Label htmlFor="firstName" className="text-gray-700">First Name</Label>
                        <Input
                          id="firstName"
                          type="text"
                          value={formData.firstName}
                          onChange={handleChange}
                          className="h-12 border-gray-300 focus:border-blue-500 focus:ring-blue-500"
                          placeholder="First Name"
                          required
                        />
                      </div>
                      <div className="space-y-2">
                        <Label htmlFor="lastName" className="text-gray-700">Last Name</Label>
                        <Input
                          id="lastName"
                          type="text"
                          value={formData.lastName}
                          onChange={handleChange}
                          className="h-12 border-gray-300 focus:border-blue-500 focus:ring-blue-500"
                          placeholder="Last Name"
                          required
                        />
                      </div>
                    </div>

                    {/* Username */}
                    <div className="space-y-2">
                      <Label htmlFor="username" className="text-gray-700">Username</Label>
                      <div className="relative">
                        <User className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                        <Input
                          id="username"
                          type="text"
                          value={formData.username}
                          onChange={handleChange}
                          className="pl-10 h-12 border-gray-300 focus:border-blue-500 focus:ring-blue-500"
                          placeholder="Choose a username"
                          required
                        />
                      </div>
                    </div>
                  </>
                )}

                {/* Email */}
                <div className="space-y-2">
                  <Label htmlFor="email" className="text-gray-700">Email Address</Label>
                  <div className="relative">
                    <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                    <Input
                      id="email"
                      type="email"
                      value={formData.email}
                      onChange={handleChange}
                      className="pl-10 h-12 border-gray-300 focus:border-blue-500 focus:ring-blue-500"
                      placeholder="Enter your email"
                      required
                    />
                  </div>
                </div>

                {/* Password */}
                <div className="space-y-2">
                  <Label htmlFor="password" className="text-gray-700">Password</Label>
                  <div className="relative">
                    <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                    <Input
                      id="password"
                      type="password"
                      value={formData.password}
                      onChange={handleChange}
                      className="pl-10 h-12 border-gray-300 focus:border-blue-500 focus:ring-blue-500"
                      placeholder="Enter your password"
                      required
                    />
                  </div>
                </div>

                {/* Remember Me & Forgot Password */}
                <div className="flex items-center justify-between">
                  <label className="flex items-center">
                    <input type="checkbox" className="rounded border-gray-300 text-blue-600 focus:ring-blue-500" />
                    <span className="ml-2 text-sm text-gray-600">Remember me</span>
                  </label>
                  <button type="button" className="text-sm text-blue-600 hover:text-blue-700">
                    Forgot password?
                  </button>
                </div>

                {/* Submit Button */}
                <Button 
                  type="submit"
                  className="w-full h-12 bg-gradient-to-r from-blue-600 to-cyan-500 hover:from-blue-700 hover:to-cyan-600 text-white font-semibold shadow-lg"
                >
                  {isSignUp ? 'Sign Up' : 'Sign In'}
                  <ArrowRight className="w-5 h-5 ml-2" />
                </Button>
              </form>

              {/* Switch Between Login & Signup */}
              <div className="mt-8 pt-6 border-t border-gray-200 text-center">
                <p className="text-gray-600">
                  {isSignUp ? (
                    <>
                      Already have an account?{' '}
                      <button onClick={() => setIsSignUp(false)} className="text-blue-600 hover:text-blue-700 font-medium">
                        Sign in
                      </button>
                    </>
                  ) : (
                    <>
                      Don't have an account?{' '}
                      <button onClick={() => setIsSignUp(true)} className="text-blue-600 hover:text-blue-700 font-medium">
                        Sign up for free
                      </button>
                    </>
                  )}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
