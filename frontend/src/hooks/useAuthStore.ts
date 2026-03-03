import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface AuthState {
  token: string | null
  user: string | null
  expiresAt: string | null
  setAuth: (token: string, user: string, expiresAt: string) => void
  logout: () => void
  isAuthenticated: () => boolean
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      token: null,
      user: null,
      expiresAt: null,
      
      setAuth: (token, user, expiresAt) => {
        set({ token, user, expiresAt })
      },
      
      logout: () => {
        set({ token: null, user: null, expiresAt: null })
      },
      
      isAuthenticated: () => {
        const { token, expiresAt } = get()
        if (!token) return false
        if (expiresAt && new Date(expiresAt) < new Date()) {
          set({ token: null, user: null, expiresAt: null })
          return false
        }
        return true
      }
    }),
    {
      name: 'tradepybot-auth'
    }
  )
)