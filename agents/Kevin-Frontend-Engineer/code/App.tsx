import React from 'react'
import { Routes, Route, Link } from 'react-router-dom'
import Home from './pages/Home'
import Create from './pages/Create'
import Settings from './pages/Settings'

export default function App() {
  return (
    <div className="min-h-screen bg-gray-50 text-gray-900">
      <nav className="bg-white shadow p-4">
        <div className="container mx-auto flex gap-4">
          <Link to="/" className="font-semibold">Home</Link>
          <Link to="/create" className="font-semibold">Create</Link>
          <Link to="/settings" className="font-semibold">Settings</Link>
        </div>
      </nav>
      <main className="container mx-auto p-6">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/create" element={<Create />} />
          <Route path="/settings" element={<Settings />} />
        </Routes>
      </main>
    </div>
  )
}
