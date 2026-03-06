export interface WorklistItem {
  id: string;
  title: string;
  status: 'open' | 'in_progress' | 'closed' | 'on_hold';
  assignee?: string;
  createdAt: string; // ISO date
  priority?: 'low' | 'medium' | 'high';
  metadata?: Record<string, any>;
}

export interface WorklistResponse {
  items: WorklistItem[];
  total_count: number;
  page: number;
  page_size: number;
}

// NOTE: These types are provisional — please confirm API shape with backend (Marcus).