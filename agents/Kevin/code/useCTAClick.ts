import { useCallback, useEffect, useRef } from 'react';

export type CTAEvent = {
  eventType: string; // e.g. 'cta_click'
  userId?: string | null;
  timestamp?: string; // ISO
  metadata?: Record<string, any>;
};

const EVENT_QUEUE_KEY = 'event_queue_v1';
const API_PATH = '/api/events';

function enqueueEvent(event: CTAEvent) {
  try {
    const raw = localStorage.getItem(EVENT_QUEUE_KEY) || '[]';
    const arr: CTAEvent[] = JSON.parse(raw);
    arr.push(event);
    localStorage.setItem(EVENT_QUEUE_KEY, JSON.stringify(arr));
  } catch (e) {
    // best-effort; swallow errors to avoid breaking UI
    console.warn('enqueueEvent failed', e);
  }
}

async function flushQueue() {
  try {
    const raw = localStorage.getItem(EVENT_QUEUE_KEY);
    if (!raw) return;
    const arr: CTAEvent[] = JSON.parse(raw);
    if (!arr.length) return;

    // try send via navigator.sendBeacon for fire-and-forget
    if (navigator && (navigator as any).sendBeacon) {
      const payload = JSON.stringify({ events: arr });
      const blob = new Blob([payload], { type: 'application/json' });
      const ok = (navigator as any).sendBeacon(API_PATH, blob);
      if (ok) {
        localStorage.removeItem(EVENT_QUEUE_KEY);
        return;
      }
      // fallthrough to fetch if sendBeacon returned false
    }

    const res = await fetch(API_PATH, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ events: arr }),
      keepalive: true,
    });

    if (res.ok) {
      localStorage.removeItem(EVENT_QUEUE_KEY);
    }
  } catch (e) {
    // leave queue intact for retry later
    console.warn('flushQueue failed', e);
  }
}

export function useCTAClick() {
  const isOnline = useRef<boolean>(typeof navigator !== 'undefined' ? navigator.onLine : true);

  useEffect(() => {
    function handleOnline() {
      isOnline.current = true;
      flushQueue();
    }
    function handleOffline() {
      isOnline.current = false;
    }
    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);
    // try flush on mount if online
    if (isOnline.current) flushQueue();
    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  const onCTAClick = useCallback(async (opts: {
    eventType?: string;
    userId?: string | null;
    metadata?: Record<string, any>;
    redirectTo?: string | null;
  }) => {
    const event: CTAEvent = {
      eventType: opts.eventType || 'cta_click',
      userId: opts.userId ?? null,
      timestamp: new Date().toISOString(),
      metadata: opts.metadata || {},
    };

    try {
      // attempt immediate POST
      const body = JSON.stringify({ events: [event] });
      // use keepalive for navigation scenarios
      const res = await fetch(API_PATH, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body,
        keepalive: true,
      });
      if (!res.ok) {
        enqueueEvent(event);
      }
    } catch (e) {
      // network or other error -> queue
      enqueueEvent(event);
    }

    // client-side behavior: navigate if requested
    if (opts.redirectTo) {
      // small timeout to give beacon/fetch a chance; keep lightweight
      setTimeout(() => {
        window.location.href = opts.redirectTo as string;
      }, 150);
    }
  }, []);

  return { onCTAClick };
}

export default useCTAClick;
