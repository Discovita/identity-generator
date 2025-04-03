import { CoachState } from '../../../types/apiTypes';
import { ExtractedActions } from '../types';

/**
 * Extracts available actions and actions taken from the coach state metadata
 *
 * @param coachState - The current state of the coach
 * @returns Object containing available actions and actions taken
 */
export const extractActions = (coachState: CoachState): ExtractedActions => {
  const metadata = coachState.metadata || {};
  return {
    availableActions: (metadata.available_actions as string[]) || [],
    actionsTaken: (metadata.actions_taken as any[]) || [],
  };
};

/**
 * Copies JSON data to clipboard with proper formatting
 *
 * @param data - Data to copy to clipboard
 */
export const copyToClipboard = (data: any): void => {
  navigator.clipboard.writeText(JSON.stringify(data, null, 2));
};

/**
 * Extracts current state information from coach state
 *
 * @param coachState - The current state of the coach
 * @returns Object containing essential state information
 */
export const getCurrentStateInfo = (coachState: CoachState): object => {
  return {
    current_state: coachState.current_state,
    current_identity_id: coachState.current_identity_id,
  };
};
