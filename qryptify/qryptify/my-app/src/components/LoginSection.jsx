// import React, { useState, useContext } from 'react';
// import { Button } from '../components/ui/button';
// import { Input } from '../components/ui/input';
// import { Label } from '../components/ui/label';
// import { Shield, Mail, Lock, ArrowRight, User, CheckCircle, XCircle, Eye, EyeOff } from 'lucide-react';
// import { api } from './api';
// import { AuthContext } from '../AuthContext.jsx';

// export default function LoginSection({ onSuccess }) {
//   const [isSignUp, setIsSignUp] = useState(false);
//   const [showPopup, setShowPopup] = useState(false);
//   const [formData, setFormData] = useState({
//     firstName: '',
//     lastName: '',
//     username: '',
//     email: '',
//     password: '',
//   });

//   const [showPassword, setShowPassword] = useState(false);
//   const [apiStatus, setApiStatus] = useState(null);
//   const [rememberMe, setRememberMe] = useState(false);
//   const { setAccessToken } = useContext(AuthContext);

//   async function login() {
//     try {
//       const result = await api("login", "POST", {
//         email: formData.email,
//         password: formData.password,
//         rememberMe: rememberMe
//       });
//       if (result.status) {
//         setAccessToken(result.access);
//         setApiStatus(true);
//         setShowPopup(true);
//         setTimeout(() => {
//           setShowPopup(false);
//           if (onSuccess) onSuccess();
//         }, 2500);
//       } else {
//         setApiStatus(false);
//         setShowPopup(true);
//         setTimeout(() => setShowPopup(false), 2500);
//       }
//     } catch (error) {
//       setApiStatus(false);
//       setShowPopup(true);
//       setTimeout(() => setShowPopup(false), 2500);
//     }
//   }

//   async function signup() {
//     try {
//       const result = await api("signup", "POST", {
//         first_name: formData.firstName,
//         last_name: formData.lastName,
//         username: formData.username,
//         email: formData.email,
//         password: formData.password,
//         rememberMe: rememberMe,
//       });
//       if (result.status) {
//         setAccessToken(result.access);
//         setApiStatus(true);
//         setShowPopup(true);
//         setTimeout(() => {
//           setShowPopup(false);
//           if (onSuccess) onSuccess();
//         }, 2500);
//       } else {
//         setApiStatus(false);
//         setShowPopup(true);
//         setTimeout(() => setShowPopup(false), 2500);
//       }
//     } catch (error) {
//       setApiStatus(false);
//       setShowPopup(true);
//       setTimeout(() => setShowPopup(false), 2500);
//     }
//   }

//   const handleChange = (e) => {
//     setFormData({ ...formData, [e.target.id]: e.target.value });
//   };

//   const handleSubmit = async (e) => {
//     e.preventDefault();
//     if (isSignUp) {
//       await signup();
//     } else {
//       await login();
//     }
//   };

//   return (
//     <section id="login" className="min-h-screen bg-gradient-to-br from-gray-900 via-blue-900 to-cyan-900 flex items-center relative">
//       <div className="max-w-7xl mx-auto px-6 py-20 w-full">
//         <div className="grid lg:grid-cols-2 gap-12 items-center">
//           {/* Left Side Info */}
//           <div className="text-white space-y-8">
//             <div className="space-y-6">
//               <h1 className="text-5xl font-bold leading-tight">
//                 <span className="bg-gradient-to-r from-white to-cyan-300 bg-clip-text text-transparent">
//                   Secure Access
//                 </span>
//                 <br />
//                 <span>to Qryptify</span>
//               </h1>
//               <p className="text-xl text-blue-200 leading-relaxed max-w-lg">
//                 Join thousands of researchers and security professionals who trust Qryptify for their cryptographic analysis needs.
//               </p>
//             </div>
//             <div className="space-y-4">
//               <div className="flex items-center gap-3">
//                 <Shield className="w-5 h-5 text-cyan-400" />
//                 <span className="text-blue-200">Enterprise-grade security</span>
//               </div>
//               <div className="flex items-center gap-3">
//                 <Shield className="w-5 h-5 text-cyan-400" />
//                 <span className="text-blue-200">Blockchain-verified results</span>
//               </div>
//               <div className="flex items-center gap-3">
//                 <Shield className="w-5 h-5 text-cyan-400" />
//                 <span className="text-blue-200">24/7 expert support</span>
//               </div>
//             </div>
//           </div>
//           {/* Right Side Box */}
//           <div className="relative">
//             <div className="absolute inset-0 bg-gradient-to-r from-cyan-400 to-blue-500 rounded-3xl blur-xl opacity-20"></div>
//             <div className="relative bg-white p-8 rounded-3xl shadow-2xl">
//               <div className="text-center mb-8">
//                 <h2 className="text-2xl font-bold text-gray-900 mb-2">
//                   {isSignUp ? 'Create an Account' : 'Welcome Back'}
//                 </h2>
//                 <p className="text-gray-600">
//                   {isSignUp ? 'Sign up for your Qryptify account' : 'Sign in to your Qryptify account'}
//                 </p>
//               </div>
//               {/* Form */}
//               <form onSubmit={handleSubmit} className="space-y-6">
//                 {isSignUp && (
//                   <>
//                     <div className="grid grid-cols-2 gap-4">
//                       <div className="space-y-2">
//                         <Label htmlFor="firstName" className="text-gray-700">First Name</Label>
//                         <Input
//                           id="firstName"
//                           type="text"
//                           value={formData.firstName}
//                           onChange={handleChange}
//                           className="h-12 border-gray-300 focus:border-blue-500 focus:ring-blue-500"
//                           placeholder="First Name"
//                           required
//                         />
//                       </div>
//                       <div className="space-y-2">
//                         <Label htmlFor="lastName" className="text-gray-700">Last Name</Label>
//                         <Input
//                           id="lastName"
//                           type="text"
//                           value={formData.lastName}
//                           onChange={handleChange}
//                           className="h-12 border-gray-300 focus:border-blue-500 focus:ring-blue-500"
//                           placeholder="Last Name"
//                           required
//                         />
//                       </div>
//                     </div>
//                     <div className="space-y-2">
//                       <Label htmlFor="username" className="text-gray-700">Username</Label>
//                       <div className="relative">
//                         <User className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
//                         <Input
//                           id="username"
//                           type="text"
//                           value={formData.username}
//                           onChange={handleChange}
//                           className="pl-10 h-12 border-gray-300 focus:border-blue-500 focus:ring-blue-500"
//                           placeholder="Choose a username"
//                           required
//                         />
//                       </div>
//                     </div>
//                   </>
//                 )}
//                 <div className="space-y-2">
//                   <Label htmlFor="email" className="text-gray-700">Email Address</Label>
//                   <div className="relative">
//                     <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
//                     <Input
//                       id="email"
//                       type="email"
//                       value={formData.email}
//                       onChange={handleChange}
//                       className="pl-10 h-12 border-gray-300 focus:border-blue-500 focus:ring-blue-500"
//                       placeholder="Enter your email"
//                       required
//                     />
//                   </div>
//                 </div>
//                 {/* Password Field with Eye Toggle */}
//                 <div className="space-y-2">
//                   <Label htmlFor="password" className="text-gray-700">Password</Label>
//                   <div className="relative">
//                     <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
//                     <Input
//                       id="password"
//                       type={showPassword ? "text" : "password"}
//                       value={formData.password}
//                       onChange={handleChange}
//                       className="pl-10 pr-10 h-12 border-gray-300 focus:border-blue-500 focus:ring-blue-500"
//                       placeholder="Enter your password"
//                       required
//                     />
//                     <button
//                       type="button"
//                       onClick={() => setShowPassword(!showPassword)}
//                       className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-500 hover:text-gray-700"
//                     >
//                       {showPassword ? <Eye className="w-5 h-5" /> : <EyeOff className="w-5 h-5" />}
//                     </button>
//                   </div>
//                 </div>
//                 <div className="flex items-center justify-between">
//                   <label className="flex items-center">
//                     <input
//                       type="checkbox"
//                       checked={rememberMe}
//                       onChange={(e) => setRememberMe(e.target.checked)}
//                       className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
//                     />
//                     <span className="ml-2 text-sm text-gray-600">Remember me</span>
//                   </label>
//                   <button type="button" className="text-sm text-blue-600 hover:text-blue-700">
//                     Forgot password?
//                   </button>
//                 </div>
//                 <Button
//                   type="submit"
//                   className="w-full h-12 bg-gradient-to-r from-blue-600 to-cyan-500 hover:from-blue-700 hover:to-cyan-600 text-white font-semibold shadow-lg"
//                 >
//                   {isSignUp ? 'Sign Up' : 'Sign In'}
//                   <ArrowRight className="w-5 h-5 ml-2" />
//                 </Button>
//               </form>
//               <div className="mt-8 pt-6 border-t border-gray-200 text-center">
//                 <p className="text-gray-600">
//                   {isSignUp ? (
//                     <>
//                       Already have an account?{' '}
//                       <button
//                         onClick={() => setIsSignUp(false)}
//                         className="text-blue-600 hover:text-blue-700 font-medium"
//                       >
//                         Sign in
//                       </button>
//                     </>
//                   ) : (
//                     <>
//                       Don't have an account?{' '}
//                       <button
//                         onClick={() => setIsSignUp(true)}
//                         className="text-blue-600 hover:text-blue-700 font-medium"
//                       >
//                         Sign up for free
//                       </button>
//                     </>
//                   )}
//                 </p>
//               </div>
//             </div>
//           </div>
//         </div>
//       </div>
//       {/* Popup Overlay */}
//       {showPopup && (
//         <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 transition-opacity">
//           <div className="bg-white rounded-2xl shadow-2xl p-8 text-center animate-fadeIn max-w-sm w-full">
//             {apiStatus ? (
//               <>
//                 <div className="flex items-center justify-center mb-4">
//                   <div className="bg-green-100 p-3 rounded-full">
//                     <CheckCircle className="w-12 h-12 text-green-500 animate-bounce" />
//                   </div>
//                 </div>
//                 <h3 className="text-xl font-semibold text-gray-900">
//                   {isSignUp ? 'Signed up successfully!' : 'Logged in successfully!'}
//                 </h3>
//               </>
//             ) : (
//               <>
//                 <div className="flex items-center justify-center mb-4">
//                   <div className="bg-red-100 p-3 rounded-full">
//                     <XCircle className="w-12 h-12 text-red-600 animate-shake" />
//                   </div>
//                 </div>
//                 <h3 className="text-xl font-semibold text-red-700">
//                   {isSignUp ? 'Signup failed!' : 'Login failed!'}
//                 </h3>
//                 <p className="text-sm text-gray-500 mt-2">
//                   Incorrect email or password. Please try again.
//                 </p>
//               </>
//             )}
//           </div>
//         </div>
//       )}
//     </section>
//   );
// }


import React, { useState, useContext } from 'react';
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
  });

  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [apiStatus, setApiStatus] = useState(null);
  const [rememberMe, setRememberMe] = useState(false);
  const { setAccessToken } = useContext(AuthContext);
  const navigate = useNavigate();

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
      const result = await api('signup', 'POST', {
        first_name: formData.firstName,
        last_name: formData.lastName,
        username: formData.username,
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

  async function resetPassword() {
    try {
      const result = await api('reset-password', 'PATCH', {
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
                          required
                          className="pl-10"
                        />
                      </div>
                    </div>
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
                      required
                      className="pl-10"
                    />
                  </div>
                </div>

                {/* Password fields */}
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
                        required
                        className="pl-10 pr-10"
                      />
                      <button
                        type="button"
                        onClick={() => setShowPassword(!showPassword)}
                        className="absolute right-3 top-1/2 transform -translate-y-1/2"
                      >
                        {showPassword ? <Eye /> : <EyeOff />}
                      </button>
                    </div>
                  </div>
                )}

                {isForgotPassword && (
                  <>
                    {/* New Password */}
                    <div className="space-y-2">
                      <Label htmlFor="password" className="text-gray-700">
                        New Password
                      </Label>
                      <Input
                        id="password"
                        type={showPassword ? 'text' : 'password'}
                        value={formData.password}
                        onChange={handleChange}
                        placeholder="Enter new password"
                        required
                      />
                    </div>
                    {/* Confirm Password */}
                    <div className="space-y-2">
                      <Label htmlFor="confirmPassword" className="text-gray-700">
                        Confirm Password
                      </Label>
                      <Input
                        id="confirmPassword"
                        type={showConfirmPassword ? 'text' : 'password'}
                        value={formData.confirmPassword}
                        onChange={handleChange}
                        placeholder="Confirm your new password"
                        required
                      />
                    </div>
                  </>
                )}

                {/* Remember Me + Forgot Password */}
                {!isForgotPassword && (
                  <div className="flex items-center justify-between">
                    <label className="flex items-center">
                      <input
                        type="checkbox"
                        checked={rememberMe}
                        onChange={(e) => setRememberMe(e.target.checked)}
                        className="rounded border-gray-300"
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
                  className="w-full h-12 bg-gradient-to-r from-blue-600 to-cyan-500 text-white font-semibold shadow-lg"
                >
                  {isForgotPassword
                    ? 'Reset Password'
                    : isSignUp
                    ? 'Sign Up'
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
                        Don't have an account?{' '}
                        <button
                          onClick={() => setIsSignUp(true)}
                          className="text-blue-600 hover:text-blue-700 font-medium"
                        >
                          Sign up for free
                        </button>
                      </>
                    )}
                  </p>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
