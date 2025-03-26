/* tslint:disable */
/* eslint-disable */
/**
/* This file was automatically generated from pydantic models by running pydantic2ts.
/* Do not modify it by hand - just update the pydantic models and then re-run the script
*/

/**
 * Type of action to perform
 */
export type ActionType =
  | "create_identity"
  | "update_identity"
  | "accept_identity"
  | "complete_introduction"
  | "transition_state";
/**
 * Current state of the coaching session
 */
export type CoachingState = "introduction" | "identity_brainstorming" | "identity_refinement";

/**
 * An action to be performed on the coaching state.
 */
export interface Action {
  type: ActionType;
  /**
   * Parameters for the action
   */
  params?: {
    [k: string]: unknown;
  };
}
/**
 * Request model for coach API.
 */
export interface CoachRequest {
  /**
   * User's message
   */
  message: string;
  coach_state: CoachState;
}
/**
 * Current state of the coaching session
 */
export interface CoachState {
  current_state: CoachingState;
  user_profile: UserProfile;
  /**
   * List of confirmed identities
   */
  identities?: Identity[];
  /**
   * Currently proposed identity, cleared unless explicitly proposed by LLM
   */
  proposed_identity?: Identity | null;
  /**
   * Index of current identity being refined
   */
  current_identity_index?: number | null;
  /**
   * History of conversation
   */
  conversation_history?: Message[];
  /**
   * Additional metadata
   */
  metadata?: {
    [k: string]: unknown;
  };
}
/**
 * User's profile information
 */
export interface UserProfile {
  /**
   * User's name
   */
  name: string;
  /**
   * User's goals
   */
  goals?: string[];
}
/**
 * Represents a single identity with its acceptance status.
 */
export interface Identity {
  /**
   * Unique identifier for the identity
   */
  id: string;
  /**
   * Description of the identity
   */
  description: string;
  /**
   * Whether the identity has been accepted by the user
   */
  is_accepted?: boolean;
}
/**
 * A single message in the conversation history.
 */
export interface Message {
  /**
   * Role of the message sender (user or coach)
   */
  role: string;
  /**
   * Content of the message
   */
  content: string;
}
/**
 * Response model for coach API.
 */
export interface CoachResponse {
  /**
   * Coach's response message
   */
  message: string;
  coach_state: CoachState1;
  /**
   * Prompt for identity visualization
   */
  visualization_prompt?: {
    [k: string]: unknown;
  } | null;
}
/**
 * Updated state of the coaching session
 */
export interface CoachState1 {
  current_state: CoachingState;
  user_profile: UserProfile;
  /**
   * List of confirmed identities
   */
  identities?: Identity[];
  /**
   * Currently proposed identity, cleared unless explicitly proposed by LLM
   */
  proposed_identity?: Identity | null;
  /**
   * Index of current identity being refined
   */
  current_identity_index?: number | null;
  /**
   * History of conversation
   */
  conversation_history?: Message[];
  /**
   * Additional metadata
   */
  metadata?: {
    [k: string]: unknown;
  };
}
/**
 * Complete state of a coaching session.
 * This object is passed with each request/response to maintain stateless operation.
 */
export interface CoachState2 {
  current_state: CoachingState;
  user_profile: UserProfile;
  /**
   * List of confirmed identities
   */
  identities?: Identity[];
  /**
   * Currently proposed identity, cleared unless explicitly proposed by LLM
   */
  proposed_identity?: Identity | null;
  /**
   * Index of current identity being refined
   */
  current_identity_index?: number | null;
  /**
   * History of conversation
   */
  conversation_history?: Message[];
  /**
   * Additional metadata
   */
  metadata?: {
    [k: string]: unknown;
  };
}
/**
 * Structured response from the coach.
 */
export interface CoachStructuredResponse {
  /**
   * Main response message to show the user
   */
  message: string;
  coach_state: CoachState3;
}
/**
 * Updated state of the coaching session
 */
export interface CoachState3 {
  current_state: CoachingState;
  user_profile: UserProfile;
  /**
   * List of confirmed identities
   */
  identities?: Identity[];
  /**
   * Currently proposed identity, cleared unless explicitly proposed by LLM
   */
  proposed_identity?: Identity | null;
  /**
   * Index of current identity being refined
   */
  current_identity_index?: number | null;
  /**
   * History of conversation
   */
  conversation_history?: Message[];
  /**
   * Additional metadata
   */
  metadata?: {
    [k: string]: unknown;
  };
}
/**
 * Result of processing a user message.
 * Contains the coach's response, updated state, and any actions taken.
 */
export interface ProcessMessageResult {
  /**
   * Coach's response message
   */
  message: string;
  state: CoachState4;
  /**
   * Actions performed
   */
  actions?: Action[];
}
/**
 * Updated coaching state
 */
export interface CoachState4 {
  current_state: CoachingState;
  user_profile: UserProfile;
  /**
   * List of confirmed identities
   */
  identities?: Identity[];
  /**
   * Currently proposed identity, cleared unless explicitly proposed by LLM
   */
  proposed_identity?: Identity | null;
  /**
   * Index of current identity being refined
   */
  current_identity_index?: number | null;
  /**
   * History of conversation
   */
  conversation_history?: Message[];
  /**
   * Additional metadata
   */
  metadata?: {
    [k: string]: unknown;
  };
}
/**
 * User information and goals.
 */
export interface UserProfile1 {
  /**
   * User's name
   */
  name: string;
  /**
   * User's goals
   */
  goals?: string[];
}
/**
 * Base model for LLM responses that can generate their own schema documentation.
 */
export interface LLMResponseModel {}
