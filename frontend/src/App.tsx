import { useState } from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import Login from './pages/Login'
import Dashboard from './pages/Dashboard'
import Integrations from './pages/Integrations'
import Stats from './pages/Stats'
import Navbar from './components/Navbar'
import { useAuthStore } from './hooks/useAuthStore'

function App() {
  const { token } = useAuthStore()
  const [sidebarOpen, setSidebarOpen] = useState(false)

  return (
    <div className="flex h-screen bg-background">
      <Navbar 
        sidebarOpen={sidebarOpen} 
        setSidebarOpen={setSidebarOpen} 
      />
      
      <div className="flex-1 overflow-auto">
        <main className="p-6">
          <Routes>
            <Route 
              path="/login" 
              element={token ? <Navigate to="/dashboard" /> : <Login />} 
            />
            <Route 
              path="/dashboard" 
              element={token ? <Dashboard /> : <Navigate to="/login" />} 
            />
            <Route 
              path="/integrations" 
              element={token ? <Integrations /> : <Navigate to="/login" />} 
            />
            <Route 
              path="/stats" 
              element={token ? <Stats /> : <Navigate to="/login" />} 
            />
            <Route 
              path="/" 
              element={<Navigate to={token ? "/dashboard" : "/login"} />} 
            />
          </Routes>
        </main>
      </div>
    </div>
  )
}

export default App
