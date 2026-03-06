import { useEffect } from 'react';

export default function useImagePreview(file: File | null) {
  const url = file ? URL.createObjectURL(file) : null;
  useEffect(() => {
    return () => {
      if (url) URL.revokeObjectURL(url);
    };
  }, [url]);
  return { previewUrl: url, revoke: () => { if (url) URL.revokeObjectURL(url); } };
}
