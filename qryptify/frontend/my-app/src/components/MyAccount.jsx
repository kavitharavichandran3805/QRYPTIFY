import React, { useState, useEffect, useContext } from 'react';
import {
  User, Mail, Lock, Shield,
  Activity, Check, Sparkles,
  ArrowRight, Cpu, Phone, Users, Calendar,
  ArrowLeft, Eye, EyeOff,
  AlertCircle, CheckCircle2, Info, X
} from 'lucide-react';
import { api } from './api';
import { AuthContext } from '../AuthContext.jsx'
import { useNavigate } from 'react-router-dom';

function Card({ className = '', children }) {
  return (
    <div className={`bg-white/80 backdrop-blur-sm border border-gray-100 shadow-xl rounded-3xl overflow-hidden ${className}`}>
      {children}
    </div>
  );
}

function CardHeader({ className = '', children }) {
  return <div className={`p-8 pb-0 ${className}`}>{children}</div>;
}

function CardTitle({ className = '', children }) {
  return <h2 className={`font-semibold ${className}`}>{children}</h2>;
}

function CardContent({ className = '', children }) {
  return <div className={`p-8 ${className}`}>{children}</div>;
}

function Badge({ className = '', children }) {
  return (
    <span className={`inline-flex items-center rounded-full text-xs font-semibold px-3 py-1 ${className}`}>
      {children}
    </span>
  );
}

function Btn({ className = '', children, ...props }) {
  return (
    <button
      className={`inline-flex items-center justify-center font-medium focus:outline-none ${className}`}
      {...props}
    >
      {children}
    </button>
  );
}

// Custom Alert Component
function Alert({ type = 'info', message, onClose, className = '' }) {
  const getColors = () => {
    switch (type) {
      case 'success':
        return { bg: 'bg-emerald-50/90', border: 'border-emerald-200', text: 'text-emerald-800', icon: 'text-emerald-600' };
      case 'error':
        return { bg: 'bg-red-50/90', border: 'border-red-200', text: 'text-red-800', icon: 'text-red-600' };
      case 'warning':
        return { bg: 'bg-orange-50/90', border: 'border-orange-200', text: 'text-orange-800', icon: 'text-orange-600' };
      case 'danger':
        return { bg: 'bg-red-50/95', border: 'border-red-300', text: 'text-red-900', icon: 'text-red-700' };
      default:
        return { bg: 'bg-blue-50/90', border: 'border-blue-200', text: 'text-blue-800', icon: 'text-blue-600' };
    }
  };

  const colors = getColors();
  const [visible, setVisible] = useState(true);

  const handleClose = () => {
    setVisible(false);
    setTimeout(() => onClose?.(), 300);
  };

  if (!visible) return null;

  return (
    <div className={`max-w-md mx-auto backdrop-blur-sm ${colors.bg} ${colors.border} border-2 border-dashed rounded-2xl shadow-2xl p-6 animate-slide-down flex items-start gap-4 ${className}`}>
      <div className={`p-2.5 bg-white/60 rounded-xl shadow-sm ${colors.icon}`}>
        {type === 'success' && <CheckCircle2 className="w-6 h-6" />}
        {(type === 'error' || type === 'danger') && <AlertCircle className="w-6 h-6" />}
        {type === 'warning' && <AlertCircle className="w-6 h-6" />}
        {type === 'info' && <Info className="w-6 h-6" />}
      </div>
      <div className="flex-1 min-w-0">
        <p className={`font-medium ${colors.text} leading-relaxed`}>{message}</p>
      </div>
      <button
        onClick={handleClose}
        className="ml-2 p-2 hover:bg-white/60 rounded-xl transition-all duration-200 group hover:scale-110 hover:rotate-12"
      >
        <X className="w-5 h-5 text-gray-500 group-hover:text-gray-700 transition-all duration-200" />
      </button>
    </div>
  );
}

// Glassmorphism Delete Confirmation Dialog
function ConfirmDialog({ isOpen, onConfirm, onCancel, title, message, type = 'danger' }) {
  if (!isOpen) return null;

  return (
    <>
      <div className="fixed inset-0 bg-black/40 backdrop-blur-sm z-[1000] animate-fade-overlay" />
      <div className="fixed inset-0 flex items-center justify-center p-6 z-[1001] animate-scale-in">
        <div className="w-full max-w-md bg-white/90 backdrop-blur-xl border border-white/50 shadow-3xl rounded-3xl overflow-hidden animate-glass-float">
          <div className="bg-gradient-to-r from-slate-50/80 via-white/60 to-blue-50/80 backdrop-blur-lg border-b border-slate-200/50 p-8">
            <div className="flex items-start gap-4">
              <div className="p-3 bg-gradient-to-br from-red-100/80 to-red-200/60 backdrop-blur-sm rounded-2xl border border-red-200/50 shadow-lg shrink-0">
                <AlertCircle className="w-8 h-8 text-red-600" />
              </div>
              <div className="flex-1 min-w-0 pt-1">
                <h3 className="text-2xl font-bold text-gray-900 mb-2 leading-tight">{title}</h3>
                <p className="text-gray-700 text-lg leading-relaxed">{message}</p>
              </div>
            </div>
          </div>

          <div className="px-6 py-3 bg-gradient-to-r from-orange-100/80 to-red-100/60 backdrop-blur-sm border-y border-orange-200/50">
            <p className="text-center text-sm font-semibold text-orange-800 flex items-center justify-center gap-2">
              ⚠️ <span>This action is irreversible</span>
            </p>
          </div>

          <div className="p-8 bg-gradient-to-b from-slate-50/70 via-white/50 to-blue-50/30 backdrop-blur-xl">
            <div className="flex gap-4">
              <button
                onClick={onCancel}
                className="flex-1 group relative h-14 rounded-2xl bg-gradient-to-br from-blue-50/90 via-cyan-50/80 to-blue-100/70 backdrop-blur-xl border-2 border-blue-200/60 shadow-xl hover:shadow-2xl hover:shadow-blue-200/50 hover:-translate-y-1 hover:border-blue-300/80 hover:from-blue-100/95 hover:to-cyan-100/90 transition-all duration-400 overflow-hidden font-semibold text-blue-800 text-lg"
              >
                <div className="absolute inset-0 bg-gradient-to-r from-white/60 via-transparent to-cyan-100/40 opacity-0 group-hover:opacity-100 transition-all duration-500" />
                <div className="absolute inset-0 bg-gradient-to-r from-blue-400/20 to-cyan-400/10 rounded-2xl blur opacity-0 group-hover:opacity-100 transition-all duration-600 -z-10" />
                <span className="relative z-10 flex items-center justify-center gap-2">
                  <Shield className="w-5 h-5 group-hover:scale-110 transition-transform duration-300" />
                  Cancel
                </span>
              </button>

              <button
                onClick={onConfirm}
                className="flex-1 group relative h-14 rounded-2xl bg-gradient-to-br from-red-100/95 via-red-200/80 to-red-300/70 backdrop-blur-xl border-2 border-red-300/70 shadow-xl hover:shadow-2xl hover:shadow-red-300/60 hover:-translate-y-1 hover:border-red-400/90 hover:from-red-200/95 hover:to-red-400/85 transition-all duration-400 overflow-hidden font-bold text-red-900 text-lg active:scale-[0.98]"
              >
                <div className="absolute inset-0 bg-gradient-to-r from-white/50 via-transparent to-red-100/30 opacity-0 group-hover:opacity-100 transition-all duration-500" />
                <div className="absolute inset-0 bg-gradient-to-r from-red-500/30 to-red-600/20 rounded-2xl blur opacity-0 group-hover:opacity-100 transition-all duration-600 -z-10" />
                <span className="relative z-10 flex items-center justify-center gap-2">
                  <AlertCircle className="w-5 h-5 group-hover:scale-110 transition-transform duration-300" />
                  Delete
                </span>
                <div className="absolute -inset-1 bg-gradient-to-r from-red-400/40 via-transparent to-red-500/40 -skew-x-6 opacity-0 group-hover:opacity-100 transition-all duration-700 animate-shimmer" />
              </button>
            </div>
          </div>
        </div>
      </div>

      <style jsx>{`
        @keyframes fade-overlay {
          from { opacity: 0; backdrop-filter: blur(0px); }
          to { opacity: 1; backdrop-filter: blur(8px); }
        }
        @keyframes scale-in {
          from { opacity: 0; transform: scale(0.8); }
          to { opacity: 1; transform: scale(1); }
        }
        @keyframes glass-float {
          0%, 100% { transform: translateY(0px) rotate(0deg); }
          50% { transform: translateY(-8px) rotate(0.5deg); }
        }
        @keyframes shimmer {
          0% { transform: translateX(-100%) skewX(-20deg); }
          100% { transform: translateX(100%) skewX(20deg); }
        }
        .animate-fade-overlay { animation: fade-overlay 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94); }
        .animate-scale-in { animation: scale-in 0.4s cubic-bezier(0.34, 1.56, 0.64, 1); }
        .animate-glass-float { animation: glass-float 4s ease-in-out infinite; }
        .animate-shimmer { animation: shimmer 2s linear infinite; }
      `}</style>
    </>
  );
}

export default function MyAccount() {
  const [originalProfile, setOriginalProfile] = useState(null);
  const [alerts, setAlerts] = useState([]);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
  const navigate = useNavigate();
  const { accessToken, setAccessToken } = useContext(AuthContext);
  const [profile, setProfile] = useState({
    firstName: "",
    lastName: "",
    email: "",
    mobile: "",
    username: "",
    role: "",
    createdAt: "",
    lastLogin: "",
    isActive: false,
  });

  const [passwords, setPasswords] = useState({
    current: '',
    newPass: '',
    confirm: '',
  });

  const [showPasswords, setShowPasswords] = useState({
    current: false,
    newPass: false,
    confirm: false,
  });

  const [loading, setLoading] = useState(false);
  const [passwordLoading, setPasswordLoading] = useState(false); // Added for password update loading

  // Alert management functions
  const addAlert = (message, type = 'info') => {
    const id = Date.now();
    setAlerts(prev => [...prev, { id, message, type }]);
    setTimeout(() => removeAlert(id), 6000);
  };

  const removeAlert = (id) => {
    setAlerts(prev => prev.filter(alert => alert.id !== id));
  };

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        setLoading(true);
        const data = await api('user-details', 'GET');

        if (data.status) {
          const mappedProfile = {
            firstName: data.user.first_name || "",
            lastName: data.user.last_name || "",
            email: data.user.email || "",
            mobile: data.user.phone || "",
            username: data.user.username || "",
            role: data.user.role || "",
            createdAt: data.user.date_joined || "",
            lastLogin: data.user.last_login || "",
            isActive: Boolean(data.user.is_active),
          };
          setProfile(mappedProfile);
          setOriginalProfile(mappedProfile);
        } else {
          addAlert("Error occurred in navigating My Account section", 'error');
        }
      } catch (error) {
        console.error('Profile fetch error:', error);
        addAlert("Unable to load profile details", 'error');
      } finally {
        setLoading(false);
      }
    };

    fetchProfile();
  }, []);

  const handleProfileChange = (field, value) => {
    setProfile(prev => ({ ...prev, [field]: value }));
  };

  const handlePasswordChange = (e) => {
    setPasswords(prev => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const togglePasswordVisibility = (field) => {
    setShowPasswords(prev => ({ ...prev, [field]: !prev[field] }));
  };

  const validatePasswordFields = () => {
  const { current, newPass, confirm } = passwords;
  
  if (!current.trim()) {
    addAlert('Please enter your current password', 'warning');
    return false;
  }
  
  if (!newPass.trim()) {
    addAlert('Please enter a new password', 'warning');
    return false;
  }
  
  if (!confirm.trim()) {
    addAlert('Please confirm your new password', 'warning');
    return false;
  }
  
  // ✅ NEW: Check if new password is same as current
  if (newPass === current) {
    addAlert('New password cannot be the same as current password', 'error');
    return false;
  }
  
  if (newPass !== confirm) {
    addAlert('New password and confirm password do not match', 'error');
    return false;
  }
  
  if (newPass.length < 6) {
    addAlert('New password must be at least 6 characters long', 'error');
    return false;
  }
  
  return true;
};


  const handleSaveProfile = async () => {
    if (!originalProfile) return;

    const payload = {};

    if (profile.firstName !== originalProfile.firstName) {
      payload.first_name = profile.firstName;
    }

    if (profile.lastName !== originalProfile.lastName) {
      payload.last_name = profile.lastName;
    }

    if (profile.mobile !== originalProfile.mobile) {
      payload.phone = profile.mobile;
    }

    if (profile.username !== originalProfile.username) {
      payload.username = profile.username;
    }

    if (Object.keys(payload).length === 0) {
      addAlert('No changes detected', 'warning');
      return;
    }

    try {
      setLoading(true);
      const response = await api('update-profile', 'PATCH', payload);

      if (response?.status) {
        setOriginalProfile(profile);
        addAlert('Profile updated successfully', 'success');
      } else {
        addAlert(response?.message || 'Profile update failed', 'error');
      }
    } catch (error) {
      console.error('Profile update error:', error);
      addAlert(error?.response?.data?.message || 'Profile update failed', 'error');
    } finally {
      setLoading(false);
    }
  };

  // ✅ FIXED Password Change Function
  const handleChangePassword = async () => {
    // Validate fields first
    if (!validatePasswordFields()) return;

    const { current, newPass } = passwords;
    
    setPasswordLoading(true);

    try {
      console.log('Sending password reset request with payload:', {
        currentPassword: current,
        newPassword: newPass,
        confirmPassword: passwords.confirm
      });

      const result = await api('reset-password', 'PATCH', {
        currentPassword: current,
        newPassword: newPass,
        confirmPassword: passwords.confirm
      });

      console.log('API Response:', result);

      // ✅ More robust status checking
      if (result?.status === true || result?.status === 'success' || result?.success === true) {
        addAlert("Password changed successfully! ", 'success');
        setPasswords({ current: '', newPass: '', confirm: '' });
        setShowPasswords({ current: false, newPass: false, confirm: false });
      } else {
        // Handle different error response formats
        const errorMessage = result?.message || 
                           result?.error || 
                           result?.data?.message || 
                           "Password reset failed. Please check your current password and try again.";
        addAlert(errorMessage, 'error');
      }
    } catch (error) {
      console.error('Password change error:', error);
      
      // Handle different error response structures
      const errorMessage = error?.response?.data?.message || 
                          error?.response?.data?.error || 
                          error?.message || 
                          "Error in resetting the password. Please try again.";
      
      addAlert(errorMessage, 'error');
    } finally {
      setPasswordLoading(false);
    }
  };

  const handleDeleteAccount = async () => {
    setShowDeleteConfirm(true);
  };

  const handleConfirmDelete = async () => {
    setShowDeleteConfirm(false);
    setLoading(true);
    
    try {
      const result = await api('user-account-delete', 'DELETE', null, accessToken);

      if (result?.status === true || result?.status === 'success') {
        setAccessToken(null);
        addAlert('Account successfully deleted! Redirecting...', 'success');
        setTimeout(() => navigate('/'), 2000);
      } else {
        addAlert(result?.message || "Error in deleting the account", 'error');
      }
    } catch (error) {
      console.error(error);
      addAlert('Unable to delete the account. Please try again later.', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleCancelDelete = () => {
    setShowDeleteConfirm(false);
    addAlert('Account deletion cancelled', 'info');
  };

  const handleBack = () => {
    window.history.back();
  };

  if (loading && !showDeleteConfirm) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-blue-50 flex items-center justify-center">
        <div className="animate-pulse flex flex-col items-center gap-4">
          <div className="w-16 h-16 bg-blue-200 rounded-full"></div>
          <div className="h-4 w-32 bg-blue-200 rounded"></div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-blue-50 relative">
      {/* Confirmation Dialog */}
      <ConfirmDialog
        isOpen={showDeleteConfirm}
        onConfirm={handleConfirmDelete}
        onCancel={handleCancelDelete}
        title="Delete Account"
        message="This action cannot be undone. All your data, analysis history, and account information will be permanently removed from our systems."
        type="danger"
      />

      {/* Alerts Container */}
      <div className="fixed top-20 right-6 z-50 space-y-3 max-w-sm">
        {alerts.map((alert) => (
          <Alert
            key={alert.id}
            type={alert.type}
            message={alert.message}
            onClose={() => removeAlert(alert.id)}
          />
        ))}
      </div>

      {/* Top Back Button */}
      <div className="pt-6 pl-6">
        <Btn
          onClick={handleBack}
          className="inline-flex items-center gap-2 rounded-full border border-sky-300 bg-sky-50/70 hover:bg-sky-100 text-black px-4 py-2 text-sm shadow-sm hover:border-sky-400 transition-all duration-200"
          disabled={loading}
        >
          <ArrowLeft className="w-4 h-4" />
          Back
        </Btn>
      </div>

      {/* Hero Header */}
      <section className="relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-r from-blue-600/5 to-cyan-600/5"></div>
        <div className="max-w-7xl mx-auto px-6 py-16">
          <div className="flex flex-col lg:flex-row items-center gap-10">
            <div className="relative group">
              <div className="absolute -inset-4 bg-gradient-to-r from-blue-400 to-cyan-400 rounded-full blur-2xl opacity-20 group-hover:opacity-30 transition-opacity duration-500"></div>
              <div className="relative w-32 h-32 bg-white rounded-full flex items-center justify-center shadow-2xl border border-gray-100">
                <User className="w-16 h-16 text-blue-600" />
              </div>
              <div className="absolute -bottom-1 -right-1 bg-gradient-to-r from-green-500 to-emerald-500 rounded-full w-8 h-8 flex items-center justify-center shadow-lg border-2 border-white">
                <Check className="w-4 h-4 text-white" />
              </div>
            </div>

            <div className="flex-1 text-center lg:text-left">
              <div className="inline-flex items-center px-4 py-2 bg-blue-50 border border-blue-200 rounded-full text-blue-700 text-sm font-medium mb-4">
                <Cpu className="w-4 h-4 mr-2" />
                Verified Account
              </div>
              <h1 className="text-4xl lg:text-5xl font-bold mb-2">
                <span className="bg-gradient-to-r from-gray-900 via-blue-900 to-cyan-700 bg-clip-text text-transparent">
                  {profile.username || 'User'}
                </span>
              </h1>
              <p className="text-xl text-gray-600 flex items-center justify-center lg:justify-start gap-2 mb-2">
                <Mail className="w-5 h-5" />
                {profile.email}
              </p>

              <div className="flex flex-wrap gap-3 justify-center lg:justify-start mb-6">
                <Badge className="bg-blue-50 text-blue-700">
                  <Calendar className="w-4 h-4 mr-2" />
                  Joined: {profile.createdAt || 'N/A'}
                </Badge>
                <Badge className="bg-emerald-50 text-emerald-700">
                  <Activity className="w-4 h-4 mr-2" />
                  Last Login: {profile.lastLogin || 'N/A'}
                </Badge>
              </div>

              <div className="flex flex-wrap gap-3 justify-center lg:justify-start">
                <Badge className="capitalize bg-gradient-to-r from-blue-600 to-cyan-500 text-white px-4 py-2 text-sm font-medium">
                  <Sparkles className="w-4 h-4 mr-2" />
                  {profile.role || 'User'} Role
                </Badge>
                <Badge className="bg-gradient-to-r from-green-500 to-emerald-500 text-white px-4 py-2 text-sm font-medium">
                  <Check className="w-4 h-4 mr-2" />
                  Active
                </Badge>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="max-w-7xl mx-auto px-6 pb-20">
        <Card className="mb-8">
          <div className="h-1 bg-gradient-to-r from-blue-600 to-cyan-500"></div>
          <CardHeader>
            <CardTitle className="flex items-center gap-3 text-xl">
              <div className="p-3 bg-blue-50 rounded-xl">
                <User className="w-6 h-6 text-blue-600" />
              </div>
              Personal Details
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="space-y-2">
              <label className="text-sm font-medium text-gray-700">First Name</label>
              <input
                value={profile.firstName}
                onChange={(e) => handleProfileChange('firstName', e.target.value)}
                className="h-12 w-full rounded-xl border border-gray-200 px-3 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 outline-none"
                placeholder="Enter your first name"
                disabled={loading}
              />
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium text-gray-700">Last Name</label>
              <input
                value={profile.lastName}
                onChange={(e) => handleProfileChange('lastName', e.target.value)}
                className="h-12 w-full rounded-xl border border-gray-200 px-3 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 outline-none"
                placeholder="Enter your last name"
                disabled={loading}
              />
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium text-gray-700 flex items-center gap-2">
                <Phone className="w-4 h-4" />
                Mobile Number
              </label>
              <input
                value={profile.mobile}
                onChange={(e) => handleProfileChange('mobile', e.target.value)}
                className="h-12 w-full rounded-xl border border-gray-200 px-3 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 outline-none"
                placeholder="Enter mobile number"
                disabled={loading}
              />
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium text-gray-700">Username</label>
              <input
                value={profile.username}
                onChange={(e) => handleProfileChange('username', e.target.value)}
                className="h-12 w-full rounded-xl border border-gray-200 px-3 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 outline-none"
                placeholder="Enter username"
                disabled={loading}
              />
            </div>
            <Btn
              onClick={handleSaveProfile}
              className="w-full h-12 rounded-xl bg-gradient-to-r from-blue-600 to-cyan-500 text-white shadow-lg hover:from-blue-700 hover:to-cyan-600 transition-all duration-200"
              disabled={loading}
            >
              {loading ? (
                <>
                  <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin mr-2" />
                  Saving...
                </>
              ) : (
                <>
                  Save Changes
                  <ArrowRight className="w-5 h-5 ml-2" />
                </>
              )}
            </Btn>
          </CardContent>
        </Card>

        <Card className="mb-8">
          <div className="h-1 bg-gradient-to-r from-red-500 to-pink-500"></div>
          <CardHeader>
            <CardTitle className="flex items-center gap-3 text-xl">
              <div className="p-3 bg-red-50 rounded-xl">
                <Lock className="w-6 h-6 text-red-600" />
              </div>
              Password
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="flex items-center justify-between p-4 bg-green-50 border border-green-200 rounded-xl mb-6">
              <div className="flex items-center gap-3">
                <Shield className="w-5 h-5 text-green-600" />
                <span className="font-medium text-gray-800">Account Security</span>
              </div>
              <Badge className="bg-green-500 text-white">Protected</Badge>
            </div>
            
            <div className="space-y-4">
              <div className="relative">
                <input
                  type={showPasswords.current ? 'text' : 'password'}
                  name="current"
                  placeholder="Current Password *"
                  value={passwords.current}
                  onChange={handlePasswordChange}
                  className="h-12 w-full rounded-xl border border-gray-200 px-3 pr-10 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 outline-none disabled:bg-gray-50"
                  disabled={passwordLoading}
                />
                <button
                  type="button"
                  onClick={() => togglePasswordVisibility('current')}
                  className="absolute inset-y-0 right-3 flex items-center text-gray-500 hover:text-blue-600 disabled:opacity-50"
                  disabled={passwordLoading}
                >
                  {showPasswords.current ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                </button>
              </div>

              <div className="relative">
                <input
                  type={showPasswords.newPass ? 'text' : 'password'}
                  name="newPass"
                  placeholder="New Password *"
                  value={passwords.newPass}
                  onChange={handlePasswordChange}
                  className="h-12 w-full rounded-xl border border-gray-200 px-3 pr-10 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 outline-none disabled:bg-gray-50"
                  disabled={passwordLoading}
                />
                <button
                  type="button"
                  onClick={() => togglePasswordVisibility('newPass')}
                  className="absolute inset-y-0 right-3 flex items-center text-gray-500 hover:text-blue-600 disabled:opacity-50"
                  disabled={passwordLoading}
                >
                  {showPasswords.newPass ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                </button>
              </div>

              <div className="relative">
                <input
                  type={showPasswords.confirm ? 'text' : 'password'}
                  name="confirm"
                  placeholder="Confirm New Password *"
                  value={passwords.confirm}
                  onChange={handlePasswordChange}
                  className="h-12 w-full rounded-xl border border-gray-200 px-3 pr-10 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 outline-none disabled:bg-gray-50"
                  disabled={passwordLoading}
                />
                <button
                  type="button"
                  onClick={() => togglePasswordVisibility('confirm')}
                  className="absolute inset-y-0 right-3 flex items-center text-gray-500 hover:text-blue-600 disabled:opacity-50"
                  disabled={passwordLoading}
                >
                  {showPasswords.confirm ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                </button>
              </div>
            </div>

            <Btn
              onClick={handleChangePassword}
              className="w-full h-12 rounded-xl bg-gradient-to-r from-blue-600 to-cyan-500 text-white shadow-lg hover:from-blue-700 hover:to-cyan-600 transition-all duration-200"
              disabled={passwordLoading || loading}
            >
              {passwordLoading ? (
                <>
                  <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin mr-2" />
                  Updating...
                  
                </>
              ) : (
                <>
                Update Password
                <ArrowRight className="w-5 h-5 ml-2" />
                </>

              )}
            </Btn>
          </CardContent>
        </Card>

        <Card className="mb-8">
          <div className="h-1 bg-gradient-to-r from-purple-600 to-indigo-600"></div>
          <CardHeader>
            <CardTitle className="flex items-center gap-3 text-xl">
              <div className="p-3 bg-purple-50 rounded-xl">
                <Users className="w-6 h-6 text-purple-600" />
              </div>
              Role
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <label className="text-sm font-medium text-gray-700">Account Role</label>
              <div className="capitalize h-12 w-full rounded-xl border border-gray-200 px-3 flex items-center bg-gray-50 text-gray-800">
                {profile.role || 'User'}
              </div>
            </div>
          </CardContent>
        </Card>

        {!loading && (
          <div className="flex flex-col gap-4">
            <Btn
              onClick={handleDeleteAccount}
              className="w-full h-14 rounded-2xl bg-gradient-to-r from-red-600 to-red-700 text-white font-semibold shadow-xl hover:from-red-700 hover:to-red-800 hover:shadow-2xl hover:-translate-y-1 transition-all duration-300 flex items-center justify-center gap-3 text-lg"
              disabled={loading || passwordLoading}
            >
              <AlertCircle className="w-6 h-6" />
              Delete Account
            </Btn>
            <p className="text-center text-sm text-gray-500 px-4">
              ⚠️ This action is permanent and cannot be undone
            </p>
          </div>
        )}
      </section>

      <style jsx>{`
        @keyframes slide-down {
          from { opacity: 0; transform: translateX(100%) scale(0.95); }
          to { opacity: 1; transform: translateX(0) scale(1); }
        }
        .animate-slide-down { animation: slide-down 0.3s cubic-bezier(0.4, 0, 0.2, 1); }
      `}</style>
    </div>
  );
}