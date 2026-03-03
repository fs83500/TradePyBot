import { useAuthStore } from './useAuthStore'

const API_BASE = '/api'

interface RequestOptions {
  method?: 'GET' | 'POST' | 'PUT' | 'DELETE'
  body?: any
}

class ApiError extends Error {
  status: number
  
  constructor(message: string, status: number) {
    super(message)
    this.status = status
  }
}

export async function apiFetch<T>(endpoint: string, options: RequestOptions = {}): Promise<T> {
  const { method = 'GET', body } = options
  const token = useAuthStore.getState().token
  
  const headers: Record<string, string> = {
    'Content-Type': 'application/json'
  }
  
  if (token) {
    headers['Authorization'] = `Bearer ${token}`
  }
  
  const response = await fetch(`${API_BASE}${endpoint}`, {
    method,
    headers,
    body: body ? JSON.stringify(body) : undefined
  })
  
  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Unknown error' }))
    throw new ApiError(error.detail || 'Request failed', response.status)
  }
  
  return response.json()
}

export const api = {
  // Auth
  login: () => apiFetch<{ token: string; user: string; expires_at: string }>('/auth/login', { method: 'POST' }),
  getMe: () => apiFetch<{ username: string; role: string }>('/auth/me'),
  logout: () => apiFetch<{ message: string }>('/auth/logout', { method: 'POST' }),
  
  // Agents
  getAgents: () => apiFetch<any[]>('/agents'),
  getAgent: (name: string) => apiFetch<any>(`/agents/${name}`),
  configureAgent: (name: string, risk_slider_value: number) => 
    apiFetch<any>(`/agents/${name}/configure`, { method: 'POST', body: { risk_slider_value } }),
  getProviders: () => apiFetch<{ providers: any; available: string[] }>('/agents/providers'),
  
  // Trades
  getTrades: () => apiFetch<any[]>('/trades'),
  createTrade: (trade: any) => apiFetch<any>('/trades', { method: 'POST', body: trade }),
  
  // Portfolio
  getPortfolio: () => apiFetch<any>('/portfolio'),
  
  // Stats
  getStats: () => apiFetch<any>('/stats')
}