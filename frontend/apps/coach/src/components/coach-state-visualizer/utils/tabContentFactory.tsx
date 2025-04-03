import React from 'react';
import { CoachResponse, CoachState } from '../../../types/apiTypes';
import { TabName, ExpandedSectionsConfig, ExtractedActions } from '../types';
import { renderJsonSection, renderFinalPrompt, renderEmptyState } from './renderUtils';
import { getCurrentStateInfo } from './dataUtils';

/**
 * Factory function to render the appropriate content for each tab
 *
 * @param tabName - The currently active tab name
 * @param coachState - The current coach state
 * @param lastResponse - The last API response
 * @param expandedSections - Configuration for which sections are expanded
 * @param toggleSection - Function to toggle section expansion
 * @param extractedActions - Actions extracted from the coach state
 * @returns JSX element with the tab content
 */
export const renderTabContent = (
  tabName: TabName,
  coachState: CoachState,
  lastResponse: CoachResponse | undefined,
  expandedSections: ExpandedSectionsConfig,
  toggleSection: (section: string) => void,
  extractedActions: ExtractedActions
): JSX.Element => {
  const { availableActions, actionsTaken } = extractedActions;

  switch (tabName) {
    case TabName.STATE:
      return (
        <>
          {renderJsonSection(
            'Current State',
            getCurrentStateInfo(coachState),
            'state',
            expandedSections['state'],
            toggleSection
          )}

          {renderJsonSection(
            'User Profile',
            coachState.user_profile,
            'userProfile',
            expandedSections['userProfile'],
            toggleSection
          )}

          {renderJsonSection(
            'Metadata',
            coachState.metadata,
            'metadata',
            expandedSections['metadata'],
            toggleSection
          )}
        </>
      );

    case TabName.PROMPT:
      return (
        <>
          {renderFinalPrompt(lastResponse, expandedSections['prompt'], toggleSection)}

          {!lastResponse?.final_prompt &&
            renderEmptyState(
              'No prompt information available yet.',
              'Send a message to see the prompt used to generate a response.'
            )}
        </>
      );

    case TabName.ACTIONS:
      return (
        <>
          {renderJsonSection(
            'Actions Taken',
            actionsTaken,
            'actionsTaken',
            expandedSections['actionsTaken'],
            toggleSection
          )}

          {renderJsonSection(
            'Available Actions',
            availableActions,
            'availableActions',
            expandedSections['availableActions'],
            toggleSection
          )}

          {(!actionsTaken || actionsTaken.length === 0) &&
            (!availableActions || availableActions.length === 0) &&
            renderEmptyState(
              'No action information available yet.',
              'Actions will appear here when the coach performs them or lists available ones.'
            )}
        </>
      );

    case TabName.IDENTITIES:
      return (
        <>
          {renderJsonSection(
            'Confirmed Identities',
            coachState.identities,
            'identities',
            expandedSections['identities'],
            toggleSection
          )}

          {renderJsonSection(
            'Proposed Identity',
            coachState.proposed_identity,
            'proposedIdentity',
            expandedSections['proposedIdentity'],
            toggleSection
          )}

          {(!coachState.identities || coachState.identities.length === 0) &&
            !coachState.proposed_identity &&
            renderEmptyState('No identities created yet.')}
        </>
      );

    case TabName.CONVERSATION:
      return (
        <>
          {renderJsonSection(
            'Conversation History',
            coachState.conversation_history,
            'history',
            expandedSections['history'],
            toggleSection
          )}

          {(!coachState.conversation_history || coachState.conversation_history.length === 0) &&
            renderEmptyState('No conversation history available.')}
        </>
      );

    default:
      return <div>Select a tab to view details</div>;
  }
};
