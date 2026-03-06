import React, { useEffect, useRef, useState } from 'react';

interface Props {
  imageUrl: string | null;
}

export default function ThumbnailEditor({ imageUrl }: Props) {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const imgRef = useRef<HTMLImageElement | null>(null);
  const [text, setText] = useState('');
  const [contrastWarning, setContrastWarning] = useState<string | null>(null);

  useEffect(() => {
    const onExport = async (e: any) => {
      const scale = e.detail?.scale ?? 1;
      const canvas = canvasRef.current;
      if (!canvas) return;
      const blob = await new Promise<Blob | null>((resolve) => {
        canvas.toBlob((b) => resolve(b), 'image/jpeg', 0.9);
      });
      window.dispatchEvent(new CustomEvent('thumbnail:exported', { detail: { blob } }));
    };
    window.addEventListener('thumbnail:export', onExport as EventListener);
    return () => window.removeEventListener('thumbnail:export', onExport as EventListener);
  }, []);

  useEffect(() => {
    const img = new Image();
    img.crossOrigin = 'anonymous';
    img.onload = () => {
      imgRef.current = img;
      draw();
    };
    img.src = imageUrl ?? '';

    async function draw() {
      const canvas = canvasRef.current;
      const img = imgRef.current;
      if (!canvas || !img) return;
      const ctx = canvas.getContext('2d');
      if (!ctx) return;

      const targetW = 1280;
      const targetH = 720;
      canvas.width = targetW;
      canvas.height = targetH;

      // Fill background to black
      ctx.fillStyle = '#000';
      ctx.fillRect(0, 0, targetW, targetH);

      // Draw image centered, cover
      const scale = Math.max(targetW / img.width, targetH / img.height);
      const sw = targetW / scale;
      const sh = targetH / scale;
      const sx = Math.max(0, (img.width - sw) / 2);
      const sy = Math.max(0, (img.height - sh) / 2);
      ctx.drawImage(img, sx, sy, sw, sh, 0, 0, targetW, targetH);

      // Overlay safe area rectangle (visual only)
      ctx.strokeStyle = 'rgba(255,255,255,0.6)';
      ctx.lineWidth = 2;
      const safeW = 1280 * 0.9; // 90% center
      const safeH = 720 * 0.9;
      const safeX = (targetW - safeW) / 2;
      const safeY = (targetH - safeH) / 2;
      ctx.strokeRect(safeX, safeY, safeW, safeH);

      // Text rendering
      ctx.font = 'bold 72px Arial';
      ctx.fillStyle = '#ffffff';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(text || 'Title', targetW / 2, targetH * 0.15);

      // Contrast check: naive brightness diff between text color and bg at text position
      const px = Math.floor(targetW / 2);
      const py = Math.floor(targetH * 0.15);
      const imageData = ctx.getImageData(px, py, 1, 1).data;
      const bgL = (0.2126 * imageData[0] + 0.7152 * imageData[1] + 0.0722 * imageData[2]) / 255;
      const textL = 1.0; // white
      const contrast = (Math.max(textL, bgL) + 0.05) / (Math.min(textL, bgL) + 0.05);
      if (contrast < 4.5) {
        setContrastWarning('Low contrast between text and background. Adjust text color or add overlay.');
      } else {
        setContrastWarning(null);
      }
    }
  }, [imageUrl, text]);

  return (
    <div>
      <div className="border rounded overflow-hidden">
        <canvas ref={canvasRef} width={1280} height={720} aria-label="Thumbnail canvas" />
      </div>

      <label className="block mt-2">
        <span className="text-sm">Thumbnail text (2–4 words recommended)</span>
        <input
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Add short text"
          className="mt-1 block w-full border rounded p-2"
          data-testid="thumbnail-text"
        />
      </label>

      {contrastWarning && <p className="text-yellow-600 text-sm mt-1" data-testid="contrast-warning">{contrastWarning}</p>}
    </div>
  );
}
