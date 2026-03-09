import { useCallback, useEffect, useRef, useState } from 'react';

export type WSMessage = { type: string; data: any; id?: string };

export default function useWebSocket() {
  const wsRef = useRef<WebSocket | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const [messages, setMessages] = useState<WSMessage[]>([]);
  const [subscriptions, setSubscriptions] = useState<string[]>([]);
  const reconnectRef = useRef<{ attempts: number; timer?: number | null }>({ attempts: 0, timer: null });

  const connect = useCallback((url: string, token?: string) => {
    if (wsRef.current) return;
    const headers = token ? { Authorization: token } : undefined;
    // Note: browser WebSocket doesn't support custom headers; append token as query param
    const finalUrl = token ? `${url}?auth=${encodeURIComponent(token)}` : url;
    const ws = new WebSocket(finalUrl);
    wsRef.current = ws;

    ws.onopen = () => {
      reconnectRef.current.attempts = 0;
      setIsConnected(true);
    };

    ws.onmessage = (ev) => {
      try {
        const parsed = JSON.parse(ev.data);
        setMessages((s) => [...s, parsed]);
      } catch (e) {
        setMessages((s) => [...s, { type: 'raw', data: ev.data }]);
      }
    };

    ws.onclose = () => {
      wsRef.current = null;
      setIsConnected(false);
    };

    ws.onerror = () => {
      // rely on onclose + reconnect if desired
    };
  }, []);

  const disconnect = useCallback(() => {
    if (!wsRef.current) return;
    wsRef.current.close();
    wsRef.current = null;
    setIsConnected(false);
  }, []);

  const send = useCallback((msg: any) => {
    if (!wsRef.current || wsRef.current.readyState !== WebSocket.OPEN) return false;
    wsRef.current.send(JSON.stringify(msg));
    return true;
  }, []);

  const subscribe = useCallback((topic: string) => {
    if (!subscriptions.includes(topic)) {
      setSubscriptions((s) => [...s, topic]);
      send({ type: 'subscribe', topic });
    }
  }, [subscriptions, send]);

  const unsubscribe = useCallback((topic: string) => {
    setSubscriptions((s) => s.filter((t) => t !== topic));
    send({ type: 'unsubscribe', topic });
  }, [send]);

  const clearMessages = useCallback(() => setMessages([]), []);

  useEffect(() => {
    return () => {
      if (wsRef.current) {
        wsRef.current.close();
        wsRef.current = null;
      }
    };
  }, []);

  return { connect, disconnect, isConnected, messages, send, subscribe, unsubscribe, clearMessages, subscriptions } as const;
}
