// blue color border for back button 
import React, { useState, useEffect, useContext } from 'react';
import {
  User, Mail, Lock, Shield,
  Activity, Check, Sparkles,
  ArrowRight, Cpu, Phone, Users, Calendar,
  ArrowLeft, Eye, EyeOff
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

export default function MyAccount() {
  const [originalProfile, setOriginalProfile] = useState(null);
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
      isActive:false,
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
        alert("Error occurred in navigating My Account section");
      }
    } catch (error) {
      console.error(error);
      alert("Unable to load profile details");
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
    alert('No changes detected');
    return;
  }

  const response = await api('update-profile', 'PATCH', payload);

  if (response?.status) {
    setOriginalProfile(profile); // sync snapshot
    alert('Profile updated successfully');
  } else {
    alert('Profile update failed');
  }
};


  const handleChangePassword = async () => {
    const { current, newPass, confirm } = passwords;
    const result=await api('reset-password','PATCH',{
      currentPassword:current,
      newPassword:newPass,
      confirmPassword:confirm
    })
    if(result.status){
      alert("Password changed successfully")
    }
    else{
      alert("Error in resetting the password")
    }
    setPasswords({ current: '', newPass: '', confirm: '' });
  };

  const handleDeleteAccount = async () => {
    if (!window.confirm('Are you sure you want to delete your account? This action cannot be undone.')) {
      return;
    }

    setLoading(true); 
    try {
      const result = await api('user-account-delete', 'DELETE', null, accessToken);

      if (result.status) {
        setAccessToken(null);
        alert('Account successfully deleted');
        navigate('/'); 
      } else {
        alert(result.message || "Error in deleting the account");
      }
    } catch (error) {
      console.error(error);
      alert('Unable to delete the account. Please try again later.');
    } finally {
      setLoading(false);
    }
  };


  const handleBack = () => {
    window.history.back();
  };

  if (loading) {
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
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-blue-50">
      {/* Top Back Button - flush left */}
      <div className="pt-6 pl-6">
        <Btn
          onClick={handleBack}
          className="inline-flex items-center gap-2 rounded-full border border-sky-300 bg-sky-50/70 hover:bg-sky-100 text-black px-4 py-2 text-sm shadow-sm"
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
            {/* Avatar */}
            <div className="relative group">
              <div className="absolute -inset-4 bg-gradient-to-r from-blue-400 to-cyan-400 rounded-full blur-2xl opacity-20 group-hover:opacity-30 transition-opacity duration-500"></div>
              <div className="relative w-32 h-32 bg-white rounded-full flex items-center justify-center shadow-2xl border border-gray-100">
                <User className="w-16 h-16 text-blue-600" />
              </div>
              <div className="absolute -bottom-1 -right-1 bg-gradient-to-r from-green-500 to-emerald-500 rounded-full w-8 h-8 flex items-center justify-center shadow-lg border-2 border-white">
                <Check className="w-4 h-4 text-white" />
              </div>
            </div>

            {/* User Info */}
            <div className="flex-1 text-center lg:text-left">
              <div className="inline-flex items-center px-4 py-2 bg-blue-50 border border-blue-200 rounded-full text-blue-700 text-sm font-medium mb-4">
                <Cpu className="w-4 h-4 mr-2" />
                Verified Account
              </div>
              <h1 className="text-4xl lg:text-5xl font-bold mb-2">
                <span className="bg-gradient-to-r from-gray-900 via-blue-900 to-cyan-700 bg-clip-text text-transparent">
                  {profile.username}
                </span>
              </h1>
              <p className="text-xl text-gray-600 flex items-center justify-center lg:justify-start gap-2 mb-2">
                <Mail className="w-5 h-5" />
                {profile.email}
              </p>

              {/* Created At & Last Login */}
              <div className="flex flex-wrap gap-3 justify-center lg:justify-start mb-6">
                <Badge className="bg-blue-50 text-blue-700">
                  <Calendar className="w-4 h-4 mr-2" />
                  Joined: {profile.createdAt}
                </Badge>
                <Badge className="bg-emerald-50 text-emerald-700">
                  <Activity className="w-4 h-4 mr-2" />
                  Last Login: {profile.lastLogin}
                </Badge>
              </div>

              <div className="flex flex-wrap gap-3 justify-center lg:justify-start">
                <Badge className="capitalize bg-gradient-to-r from-blue-600 to-cyan-500 text-white px-4 py-2 text-sm font-medium">
  <Sparkles className="w-4 h-4 mr-2" />
  {profile.role} Role
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

      {/* Main Content */}
      <section className="max-w-7xl mx-auto px-6 pb-20">
        {/* Personal Details */}
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
              />
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium text-gray-700">Last Name</label>
              <input
                value={profile.lastName}
                onChange={(e) => handleProfileChange('lastName', e.target.value)}
                className="h-12 w-full rounded-xl border border-gray-200 px-3 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 outline-none"
                placeholder="Enter your last name"
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
                className="h-12 w-full rounded-xl border border-gray-200 px-3"
                placeholder="Enter mobile number"
              />
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium text-gray-700">Username</label>
              <input
                value={profile.username}
                onChange={(e) => handleProfileChange('username', e.target.value)}
                className="h-12 w-full rounded-xl border border-gray-200 px-3"
                placeholder="Enter username"
              />
            </div>
            <Btn
              onClick={handleSaveProfile}
              className="w-full h-12 rounded-xl bg-gradient-to-r from-blue-600 to-cyan-500 text-white shadow-lg hover:from-blue-700 hover:to-cyan-600"
            >
              Save Changes
              <ArrowRight className="w-5 h-5 ml-2" />
            </Btn>
          </CardContent>
        </Card>

        {/* Password Section */}
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
              <Badge className="bg-green-500 text-white">
                Protected
              </Badge>
            </div>
            <div className="space-y-4">

  {/* Current Password */}
  <div className="relative">
    <input
      type={showPasswords.current ? 'text' : 'password'}
      name="current"
      placeholder="Current Password"
      value={passwords.current}
      onChange={handlePasswordChange}
      className="h-12 w-full rounded-xl border border-gray-200 px-3 pr-10"
    />
    <button
      type="button"
      onClick={() => togglePasswordVisibility('current')}
      className="absolute inset-y-0 right-3 flex items-center text-gray-500 hover:text-blue-600"
    >
      {showPasswords.current ? (
        <EyeOff className="w-5 h-5" />
      ) : (
        <Eye className="w-5 h-5" />
      )}
    </button>
  </div>

  {/* New Password */}
  <div className="relative">
    <input
      type={showPasswords.newPass ? 'text' : 'password'}
      name="newPass"
      placeholder="New Password"
      value={passwords.newPass}
      onChange={handlePasswordChange}
      className="h-12 w-full rounded-xl border border-gray-200 px-3 pr-10"
    />
    <button
      type="button"
      onClick={() => togglePasswordVisibility('newPass')}
      className="absolute inset-y-0 right-3 flex items-center text-gray-500 hover:text-blue-600"
    >
      {showPasswords.newPass ? (
        <EyeOff className="w-5 h-5" />
      ) : (
        <Eye className="w-5 h-5" />
      )}
    </button>
  </div>

  {/* Confirm Password */}
  <div className="relative">
    <input
      type={showPasswords.confirm ? 'text' : 'password'}
      name="confirm"
      placeholder="Confirm New Password"
      value={passwords.confirm}
      onChange={handlePasswordChange}
      className="h-12 w-full rounded-xl border border-gray-200 px-3 pr-10"
    />
    <button
      type="button"
      onClick={() => togglePasswordVisibility('confirm')}
      className="absolute inset-y-0 right-3 flex items-center text-gray-500 hover:text-blue-600"
    >
      {showPasswords.confirm ? (
        <EyeOff className="w-5 h-5" />
      ) : (
        <Eye className="w-5 h-5" />
      )}
    </button>
  </div>

</div>

            <Btn
              onClick={handleChangePassword}
              className="w-full h-12 rounded-xl border border-red-200 text-red-600 hover:bg-red-50"
            >
              Update Password
            </Btn>
          </CardContent>
        </Card>

        {/* Role Section - static with description */}
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
              <label className="text-sm font-medium text-gray-700">
                Account Role
              </label>
              <div className="capitalize h-12 w-full rounded-xl border border-gray-200 px-3 flex items-center bg-gray-50 text-gray-800">
  {profile.role}
</div>

            </div>
          </CardContent>
        </Card>

        {/* Delete Account only */}
        <div className="flex flex-col gap-4">
          <Btn
            onClick={handleDeleteAccount}
            className="w-full h-12 rounded-xl bg-red-600 text-white hover:bg-red-700 shadow-lg"
          >
            Delete Account
          </Btn>
        </div>
      </section>
    </div>
  );
}
