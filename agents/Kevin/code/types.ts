export interface Annotation {
  id: string;
  x: number; // normalized 0-1
  y: number; // normalized 0-1
  width: number; // normalized 0-1
  height: number; // normalized 0-1
  label?: string;
  createdAt: number;
}

export interface FrameMeta {
  frameIndex: number;
  timestamp?: number;
}

export interface StreamConfig {
  width?: number; // expected pixel width
  height?: number; // expected pixel height
  frameRate?: number; // expected fps
  transport?: 'webrtc' | 'websocket' | 'rtsp' | 'polling';
}
