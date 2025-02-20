/* tslint:disable */
/* eslint-disable */
/**
/* This file was automatically generated from pydantic models by running pydantic2ts.
/* Do not modify it by hand - just update the pydantic models and then re-run the script
*/

/**
 * Single chat message.
 */
export interface ChatMessage {
  /**
   * Role of the message sender (user/assistant)
   */
  role: string;
  /**
   * Content of the message
   */
  content: string;
}
/**
 * Request model for coach API.
 */
export interface CoachRequest {
  /**
   * Unique identifier for the user
   */
  user_id: string;
  /**
   * User's message
   */
  message: string;
  /**
   * Previous chat context
   */
  context?: ChatMessage[];
}
/**
 * Response model for coach API.
 */
export interface CoachResponse {
  /**
   * Coach's response message
   */
  message: string;
}
