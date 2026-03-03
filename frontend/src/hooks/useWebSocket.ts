import { useEffect, useRef, useState } from 'react'

interface UseWebSocketOptions {
  onMessage?: (data: any) => void
  onOpen?: () => void
  onClose?: () => void
  onError?: (error: Event) => void
}

export function useWebSocket(endpoint: string, options: UseWebSocketOptions = {}) {
  const [connected, setConnected] = useState(false)
  const [lastMessage, setLastMessage] = useState<any>(null)
  const wsRef = useRef<WebSocket | null>(null)
  const reconnectTimeout = useRef<NodeJS.Timeout | null>(null)

  const connect = () => {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
    const wsUrl = `${protocol}//${window.location.host}${endpoint}`
    
    const ws = new WebSocket(wsUrl)
    
    ws.onopen = () => {
      setConnected(true)
      options.onOpen?.()
    }
    
    ws.onclose = () => {
      setConnected(false)
      options.onClose?.()
      // Reconnect after 3 seconds
      reconnectTimeout.current = setTimeout(connect, 3000)
    }
    
    ws.onerror = (error) => {
      options.onError?.(error)
    }
    
    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)
        setLastMessage(data)
        options.onMessage?.(data)
      } catch (e) {
        // Non-JSON message
        setLastMessage(event.data)
        options.onMessage?.(event.data)
      }
    }
    
    wsRef.current = ws
  }

  const disconnect = () => {
    if (reconnectTimeout.current) {
      clearTimeout(reconnectTimeout.current)
    }
    wsRef.current?.close()
  }

  const send = (data: any) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify(data))
    }
  }

  useEffect(() => {
    connect()
    return () => disconnect()
  }, [endpoint])

  return {
    connected,
    lastMessage,
    send,
    disconnect,
    reconnect: connect
  }
}

// Market data WebSocket hook
export function useMarketData() {
  const [prices, setPrices] = useState<Record<string, number>>({})
  
  const { connected } = useWebSocket('/ws/market', {
    onMessage: (data) => {
      if (data.type === 'price' && data.symbol && data.price) {
        setPrices(prev => ({
          ...prev,
          [data.symbol]: data.price
        }))
      }
    }
  })
  
  return { prices, connected }
}

// AI Feedback WebSocket hook
export function useAIFeedback() {
  const [feedback, setFeedback] = useState<any[]>([])
  
  const { connected } = useWebSocket('/ws/feedback', {
    onMessage: (data) => {
      if (data.type === 'feedback') {
        setFeedback(prev => [data, ...prev].slice(0, 50))
      }
    }
  })
  
  return { feedback, connected }
}