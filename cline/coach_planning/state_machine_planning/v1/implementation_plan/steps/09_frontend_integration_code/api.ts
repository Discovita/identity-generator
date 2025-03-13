import axios from 'axios';
import { 
  CoachStateRequest, 
  CoachStateResponse, 
  StateInfoResponse 
} from './apiTypes';

// Create axios instance with base URL from environment
const api = axios.create({
  baseURL: process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Coach API client for interacting with the coach service.
 */
export const coachApi = {
  /**
   * Send a message to the coach and get a response.
   * 
   * @param request The request containing the user message and session info
   * @returns The coach's response
   */
  async sendMessage(request: CoachStateRequest): Promise<CoachStateResponse> {
    const response = await api.post<CoachStateResponse>('/api/coach/chat', request);
    return response.data;
  },

  /**
   * Get information about the current state.
   * 
   * @param userId The user ID
   * @param sessionId Optional session ID
   * @returns Information about the current state
   */
  async getStateInfo(userId: string, sessionId?: string): Promise<StateInfoResponse> {
    const url = sessionId 
      ? `/api/coach/state/${userId}?session_id=${sessionId}`
      : `/api/coach/state/${userId}`;
    
    const response = await api.get<StateInfoResponse>(url);
    return response.data;
  },

  /**
   * Create a new coaching session.
   * 
   * @param userId The user ID
   * @returns Information about the initial state
   */
  async createSession(userId: string): Promise<StateInfoResponse> {
    const response = await api.post<StateInfoResponse>(`/api/coach/session/new/${userId}`);
    return response.data;
  },

  /**
   * Reset a coaching session to the initial state.
   * 
   * @param sessionId The session ID
   * @returns Information about the reset state
   */
  async resetSession(sessionId: string): Promise<StateInfoResponse> {
    const response = await api.post<StateInfoResponse>(`/api/coach/session/reset/${sessionId}`);
    return response.data;
  }
};
