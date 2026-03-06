import React, { useEffect, useRef } from 'react';

interface Props {
  src: string;
  width: number;
  height: number;
  transport: 'webrtc' | 'websocket' | 'rtsp' | 'polling';
  onReady?: () => void;
}

const VideoPlayer: React.FC<Props> = ({ src, width, height, transport, onReady }) => {
  const videoRef = useRef<HTMLVideoElement | null>(null);
  useEffect(()=>{
    const v = videoRef.current;
    if(!v) return;
    if(transport === 'webrtc'){
      // placeholder: assume src is an SDP or signaling URL
      // In real implementation, signaling + RTCPeerConnection required.
      // For MVP, support direct video src via <video> when possible.
      v.src = src;
      v.play().catch(()=>{});
    } else {
      v.src = src;
      v.play().catch(()=>{});
    }
    onReady && onReady();
  }, [src, transport, onReady]);

  return (
    <video ref={videoRef} width={width} height={height} controls />
  );
}

export default VideoPlayer;
