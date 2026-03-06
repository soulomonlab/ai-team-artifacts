import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import YouTubeUpload from '../YouTubeUpload';

test('renders upload and can click generate', () => {
  render(<YouTubeUpload />);
  expect(screen.getByText(/YouTube Upload/i)).toBeInTheDocument();
  const btn = screen.getByTestId('generate-2x');
  fireEvent.click(btn);
  expect(screen.getByText(/Generated:/i)).toBeInTheDocument();
});
