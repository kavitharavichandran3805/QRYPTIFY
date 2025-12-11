








// changes given by kavitha 

import React, { useState, useEffect } from 'react';
import {
  User, Mail, Lock, Shield,
  Activity, LogOut, Check, Sparkles,
  ArrowRight, Cpu, Phone, Cake, Users, Calendar
} from 'lucide-react';

// Simple replacements for Card/Badge using div/span
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
  const [profile, setProfile] = useState({
    name: 'Alice Johnson',
    email: 'alice@qryptify.com',
    phone: '+1 (555) 123-4567',
    dob: 'yyyy-mm-dd',
    emergencyContact: 'John Johnson (+1 (555) 987-6543)',
    role: 'Researcher',
    createdAt: '2024-01-10',
    lastLogin: '2025-12-09 18:45',
  });

  const [passwords, setPasswords] = useState({
    current: '',
    newPass: '',
    confirm: '',
  });

  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // fake loading if needed
  }, []);

  const handleProfileChange = (field, value) => {
    setProfile(prev => ({ ...prev, [field]: value }));
  };

  const handlePasswordChange = (e) => {
    setPasswords(prev => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleSaveProfile = () => {
    alert('Profile saved successfully!');
  };

  const handleChangePassword = () => {
    if (passwords.newPass !== passwords.confirm) {
      alert('New passwords do not match!');
      return;
    }
    alert('Password updated!');
    setPasswords({ current: '', newPass: '', confirm: '' });
  };

  const handleUpdateRole = () => {
    alert('Role updated successfully!');
  };

  const handleLogout = () => {
    alert('Logged out from all devices');
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
                  {profile.name}
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
                <Badge className="bg-gradient-to-r from-blue-600 to-cyan-500 text-white px-4 py-2 text-sm font-medium">
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

      {/* Main Content - Row-wise sections */}
      <section className="max-w-7xl mx-auto px-6 pb-20">
        {/* Personal Details - First Row */}
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
              <label className="text-sm font-medium text-gray-700">Full Name</label>
              <input
                value={profile.name}
                onChange={(e) => handleProfileChange('name', e.target.value)}
                className="h-12 w-full rounded-xl border border-gray-200 px-3 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 outline-none"
                placeholder="Enter your name"
              />
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium text-gray-700 flex items-center gap-2">
                <Phone className="w-4 h-4" />
                Phone Number
              </label>
              <input
                value={profile.phone}
                onChange={(e) => handleProfileChange('phone', e.target.value)}
                className="h-12 w-full rounded-xl border border-gray-200 px-3"
                placeholder="Enter phone number"
              />
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium text-gray-700 flex items-center gap-2">
                <Cake className="w-4 h-4" />
                Date of Birth
              </label>
              <input
                type="date"
                value={profile.dob}
                onChange={(e) => handleProfileChange('dob', e.target.value)}
                className="h-12 w-full rounded-xl border border-gray-200 px-3"
              />
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium text-gray-700">Emergency Contact</label>
              <input
                value={profile.emergencyContact}
                onChange={(e) => handleProfileChange('emergencyContact', e.target.value)}
                className="h-12 w-full rounded-xl border border-gray-200 px-3"
                placeholder="Enter emergency contact"
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

        {/* Password Section - Second Row */}
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
              <input
                type="password"
                name="current"
                placeholder="Current Password"
                value={passwords.current}
                onChange={handlePasswordChange}
                className="h-12 w-full rounded-xl border border-gray-200 px-3"
              />
              <input
                type="password"
                name="newPass"
                placeholder="New Password"
                value={passwords.newPass}
                onChange={handlePasswordChange}
                className="h-12 w-full rounded-xl border border-gray-200 px-3"
              />
              <input
                type="password"
                name="confirm"
                placeholder="Confirm New Password"
                value={passwords.confirm}
                onChange={handlePasswordChange}
                className="h-12 w-full rounded-xl border border-gray-200 px-3"
              />
            </div>
            <Btn
              onClick={handleChangePassword}
              className="w-full h-12 rounded-xl border border-red-200 text-red-600 hover:bg-red-50"
            >
              Update Password
            </Btn>
          </CardContent>
        </Card>

        {/* Role Section - Third Row */}
        <Card className="mb-16">
          <div className="h-1 bg-gradient-to-r from-purple-600 to-indigo-600"></div>
          <CardHeader>
            <CardTitle className="flex items-center gap-3 text-xl">
              <div className="p-3 bg-purple-50 rounded-xl">
                <Users className="w-6 h-6 text-purple-600" />
              </div>
              Role
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="space-y-2">
              <label className="text-sm font-medium text-gray-700 flex items-center gap-2">
                Account Role
              </label>
              <select
                value={profile.role}
                onChange={(e) => handleProfileChange('role', e.target.value)}
                className="h-12 w-full rounded-xl border border-gray-200 px-3 bg-white focus:border-purple-500 focus:ring-1 focus:ring-purple-500"
              >
                <option value="Researcher">Researcher</option>
                <option value="Auditor">Auditor</option>
                <option value="Admin">Admin</option>
                <option value="Developer">Developer</option>
              </select>
            </div>
            <div className="p-4 bg-gradient-to-r from-purple-50 to-indigo-50 rounded-xl border border-purple-200">
              <p className="text-sm text-gray-700 mb-2 flex items-center gap-2">
                <Check className="w-4 h-4 text-purple-600" />
                Role permissions updated instantly
              </p>
              <p className="text-xs text-gray-500">
                Your access level will be updated across all Qryptify services
              </p>
            </div>
            <Btn
              onClick={handleUpdateRole}
              className="w-full h-12 rounded-xl bg-gradient-to-r from-purple-600 to-indigo-500 text-white shadow-lg hover:from-purple-700 hover:to-indigo-600"
            >
              Update Role
              <ArrowRight className="w-5 h-5 ml-2" />
            </Btn>
          </CardContent>
        </Card>

        {/* Support & Logout Row */}
        <div className="grid lg:grid-cols-2 gap-8">
          {/* Recent Activity & Logout */}
          <Card>
            <div className="h-1 bg-gradient-to-r from-cyan-500 to-blue-600"></div>
            <CardHeader>
              <CardTitle className="flex items-center gap-3 text-xl">
                <div className="p-3 bg-cyan-50 rounded-xl">
                  <Activity className="w-6 h-6 text-cyan-600" />
                </div>
                Recent Activity
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <Btn
                onClick={handleLogout}
                className="w-full h-12 rounded-xl border border-red-200 text-red-600 hover:bg-red-50 justify-start"
              >
                <LogOut className="w-5 h-5 mr-2" />
                Log out from all devices
              </Btn>
            </CardContent>
          </Card>

          {/* Support Banner */}
          <Card>
            <div className="h-1 bg-gradient-to-r from-green-500 to-teal-500"></div>
            <CardHeader>
              <CardTitle className="flex items-center gap-3 text-xl text-center">
                <div className="p-3 bg-green-50 rounded-xl mx-auto">
                  <Shield className="w-6 h-6 text-green-600" />
                </div>
                Need Help?
              </CardTitle>
            </CardHeader>
            <CardContent className="text-center space-y-4">
              <p className="text-gray-600 max-w-md mx-auto">
                Our support team is available 24/7 to assist you with any queries.
              </p>
              <Btn className="w-full lg:w-auto rounded-xl bg-gradient-to-r from-blue-600 to-cyan-500 hover:from-blue-700 hover:to-cyan-600 text-white px-8 py-3 shadow-xl">
                <Mail className="w-5 h-5 mr-2" />
                support@qryptify.com
              </Btn>
            </CardContent>
          </Card>
        </div>
      </section>
    </div>
  );
}
