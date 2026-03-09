export interface Feature {
  id: string;
  name: string;
  description?: string | null;
  // ISO 8601 timestamps
  created_at: string;
  updated_at?: string | null;
  // allow extra fields returned by the API
  [key: string]: any;
}

export interface FeaturesListResponse {
  total_count: number;
  page: number; // 1-based
  per_page: number;
  items: Feature[];
}

export interface ErrorResponse {
  error: {
    code: string;
    message: string;
    details?: Record<string, any>;
  };
}
