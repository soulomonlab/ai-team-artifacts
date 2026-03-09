import React from 'react'
import { Routes, Route, Link } from 'react-router-dom'
import Home from './frontend/screens/Home'
import Create from './frontend/screens/Create'
import Settings from './frontend/screens/Settings'

export default function App() {
  return (
    <div className="min-h-screen bg-gray-50 text-gray-900">
      <header className="bg-white shadow-sm">
        <div className="max-w-4xl mx-auto px-4 py-3 flex items-center justify-between">
          <h1 className="text-lg font-medium">Cherry</h1>
          <nav className="space-x-4">
            <Link to="/" className="text-sm text-blue-600">Home</Link>
            <Link to="/create" className="text-sm text-blue-600">Create</Link>
            <Link to="/settings" className="text-sm text-blue-600">Settings</Link>
          </nav>
        </div>
      </header>
      <main className="max-w-4xl mx-auto px-4 py-6">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/create" element={<Create />} />
          <Route path="/settings" element={<Settings />} />
        </Routes>
      </main>
    </div>
  )
}
