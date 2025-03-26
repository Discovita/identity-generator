import React from 'react';
import { Identity } from '../types/apiTypes';

export interface IdentityChoiceProps {
  identity: Identity;

  /**
   * Callback function when a button is clicked
   * @param response The predefined response text to send
   */
  onChoiceSelected: (response: string) => void;
  disabled: boolean;
}

/**
 * Component for displaying identity choice buttons
 *
 * These buttons appear when a proposed identity is available
 * and allow users to quickly respond with canned messages
 * instead of typing their own responses.
 *
 * There are three main actions:
 * 1. Accept - Confirm the identity as is
 * 2. Refine - Accept but with some adjustments
 * 3. Reject - Ask for a different identity
 */
export const IdentityChoice: React.FC<IdentityChoiceProps> = ({
  identity,
  onChoiceSelected,
  disabled,
}) => {
  return (
    <div className="identity-choice-buttons">
      <button
        onClick={() => onChoiceSelected(`Yes, I like the "${identity.description}" identity.`)}
        disabled={disabled}
        className="identity-button accept-button"
        aria-label="Accept this identity"
      >
        I love it!
      </button>
      <button
        onClick={() => onChoiceSelected(`I like this identity but can we adjust it slightly?`)}
        disabled={disabled}
        className="identity-button refine-button"
        aria-label="Refine this identity"
      >
        Refine it
      </button>
      <button
        onClick={() =>
          onChoiceSelected(`This isn't really what I'm looking for. What are some other options?`)
        }
        disabled={disabled}
        className="identity-button reject-button"
        aria-label="Try another identity"
      >
        Not for me
      </button>
    </div>
  );
};
