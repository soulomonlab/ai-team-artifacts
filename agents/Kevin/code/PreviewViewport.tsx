import React from 'react';

interface Props {
  imageUrl: string | null;
  showBannerSafeArea?: boolean;
}

export default function PreviewViewport({ imageUrl, showBannerSafeArea = true }: Props) {
  return (
    <div className="space-y-4">
      <div>
        <h4 className="font-medium">Desktop preview</h4>
        <div className="border rounded mt-2" style={{ width: 480, height: 270 }}>
          <img src={imageUrl ?? ''} alt="Desktop preview" style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
        </div>
      </div>

      <div>
        <h4 className="font-medium">Mobile preview</h4>
        <div className="border rounded mt-2" style={{ width: 360, height: 202 }}>
          <img src={imageUrl ?? ''} alt="Mobile preview" style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
        </div>
      </div>

      {showBannerSafeArea && (
        <div>
          <h4 className="font-medium">Banner safe area overlay</h4>
          <div className="border rounded mt-2" style={{ width: 480, height: 135, position: 'relative' }}>
            <img src={imageUrl ?? ''} alt="Banner preview" style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
            <div style={{ position: 'absolute', left: '50%', top: '50%', transform: 'translate(-50%, -50%)', width: 1546 * (480 / 2560), height: 423 * (135 / 1440), border: '2px dashed rgba(255,255,255,0.8)' }} />
          </div>
        </div>
      )}
    </div>
  );
}
