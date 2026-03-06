import React, { useRef, useState, useEffect } from 'react';
import type { Annotation } from '../types';

interface Props {
  width: number;
  height: number;
  annotations: Annotation[];
  onCreate: (a: Annotation) => void;
  onUpdate: (a: Annotation) => void;
  onSelect?: (id?: string) => void;
}

const AnnotationCanvas: React.FC<Props> = ({ width, height, annotations, onCreate, onUpdate, onSelect }) => {
  const svgRef = useRef<SVGSVGElement | null>(null);
  const [dragging, setDragging] = useState<null | { startX:number; startY:number }>(null);
  const [newRect, setNewRect] = useState<null | { x:number; y:number; w:number; h:number }>(null);

  useEffect(()=>{
    const handleUp = (e: MouseEvent) => {
      if(!dragging) return;
      const { startX, startY } = dragging;
      const rect = svgRef.current!.getBoundingClientRect();
      const endX = e.clientX - rect.left;
      const endY = e.clientY - rect.top;
      const x = Math.min(startX, endX);
      const y = Math.min(startY, endY);
      const w = Math.abs(endX - startX);
      const h = Math.abs(endY - startY);
      const annotation: Annotation = {
        id: Math.random().toString(36).slice(2,9),
        x: x/width,
        y: y/height,
        width: w/width,
        height: h/height,
        createdAt: Date.now(),
      };
      onCreate(annotation);
      setDragging(null);
      setNewRect(null);
    };
    window.addEventListener('mouseup', handleUp);
    return ()=> window.removeEventListener('mouseup', handleUp);
  }, [dragging, width, height, onCreate]);

  const handleDown = (e: React.MouseEvent) => {
    const rect = svgRef.current!.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    setDragging({ startX: x, startY: y });
    setNewRect({ x, y, w:0, h:0 });
  };

  const handleMove = (e: React.MouseEvent) => {
    if(!dragging) return;
    const rect = svgRef.current!.getBoundingClientRect();
    const mx = e.clientX - rect.left;
    const my = e.clientY - rect.top;
    const x = Math.min(dragging.startX, mx);
    const y = Math.min(dragging.startY, my);
    const w = Math.abs(mx - dragging.startX);
    const h = Math.abs(my - dragging.startY);
    setNewRect({ x, y, w, h });
  };

  return (
    <svg
      ref={svgRef}
      width={width}
      height={height}
      onMouseDown={handleDown}
      onMouseMove={handleMove}
      style={{ border: '1px solid rgba(0,0,0,0.2)', touchAction: 'none', userSelect: 'none' }}
    >
      {annotations.map(a => (
        <rect
          key={a.id}
          x={a.x * width}
          y={a.y * height}
          width={a.width * width}
          height={a.height * height}
          fill="transparent"
          stroke="lime"
          strokeWidth={2}
        />
      ))}
      {newRect && (
        <rect
          x={newRect.x}
          y={newRect.y}
          width={newRect.w}
          height={newRect.h}
          fill="rgba(0,255,0,0.15)"
          stroke="lime"
          strokeWidth={1}
        />
      )}
    </svg>
  );
};

export default AnnotationCanvas;
