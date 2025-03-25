/**
 * TypeScript types for the coach API.
 * These types are generated from the backend Pydantic models.
 */

// Identity types
export enum IdentityCategory {
  PASSIONS = "passions_and_talents",
  MONEY_MAKER = "maker_of_money",
  MONEY_KEEPER = "keeper_of_money",
  SPIRITUAL = "spiritual",
  APPEARANCE = "personal_appearance",
  HEALTH = "physical_expression",
  FAMILY = "familial_relations",
  ROMANTIC = "romantic_relation",
  ACTION = "doer_of_things"
}

export interface Identity {
  category: IdentityCategory;
  name: string;
  affirmation: string;
  visualization?: Record<string, any>;
}

// Chat message types
export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
}

// User profile types
export interface UserProfile {
  user_id: string;
  identities: Identity[];
  current_focus?: IdentityCategory;
}

// State machine types
export enum CoachingState {
  INTRODUCTION = "INTRODUCTION",
  IDENTITY_DISCOVERY = "IDENTITY_DISCOVERY",
  IDENTITY_CONFIRMATION = "IDENTITY_CONFIRMATION",
  IDENTITY_EXPLORATION = "IDENTITY_EXPLORATION",
  IDENTITY_INTEGRATION = "IDENTITY_INTEGRATION",
  CONCLUSION = "CONCLUSION"
}

// Request types
export interface CoachStateRequest {
  user_id: string;
  message: string;
  session_id?: string;
}

// Response types
export interface CoachStateResponse {
  message: string;
  current_state: string;
  proposed_identity?: Identity;
  confirmed_identity?: Identity;
  visualization_prompt?: Record<string, any>;
  available_actions: string[];
  session_id: string;
  error?: string;
  error_code?: string;
}

export interface StateInfoResponse {
  current_state: string;
  description: string;
  available_actions: string[];
  next_possible_states: string[];
  session_id: string;
}
