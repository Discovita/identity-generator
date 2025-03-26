import { CoachRequest, CoachResponse } from './types';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000/api/v1';

export class ApiClient {
  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    });

    if (!response.ok) {
      throw new Error(`API request failed: ${response.statusText}`);
    }

    return response.json();
  }

  async sendMessage(
    message: string,
    coach_state: CoachRequest['coach_state']
  ): Promise<CoachResponse> {
    return this.request<CoachResponse>('/coach/user_input', {
      method: 'POST',
      body: JSON.stringify({
        message,
        coach_state,
      }),
    });
  }
}

export const apiClient = new ApiClient();
