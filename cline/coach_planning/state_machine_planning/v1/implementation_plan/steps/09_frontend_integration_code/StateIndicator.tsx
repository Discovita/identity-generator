import React from 'react';
import { CoachingState } from './apiTypes';
import { useCoach } from './CoachContext';

// Styles for the state indicator
const styles = {
  container: {
    display: 'flex',
    flexDirection: 'column' as const,
    padding: '12px',
    borderRadius: '8px',
    backgroundColor: '#f5f5f5',
    marginBottom: '16px',
  },
  header: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '8px',
  },
  title: {
    fontSize: '16px',
    fontWeight: 'bold' as const,
    margin: 0,
  },
  description: {
    fontSize: '14px',
    margin: '0 0 12px 0',
  },
  stateFlow: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '12px',
  },
  state: {
    padding: '6px 12px',
    borderRadius: '16px',
    fontSize: '12px',
    fontWeight: 'bold' as const,
  },
  activeState: {
    backgroundColor: '#4a90e2',
    color: 'white',
  },
  inactiveState: {
    backgroundColor: '#e0e0e0',
    color: '#757575',
  },
  connector: {
    height: '2px',
    flex: 1,
    backgroundColor: '#e0e0e0',
    margin: '0 4px',
  },
  actionsContainer: {
    marginTop: '8px',
  },
  actionTitle: {
    fontSize: '14px',
    fontWeight: 'bold' as const,
    margin: '0 0 4px 0',
  },
  actionsList: {
    display: 'flex',
    flexWrap: 'wrap' as const,
    gap: '4px',
  },
  action: {
    padding: '4px 8px',
    borderRadius: '4px',
    backgroundColor: '#e8f0fe',
    color: '#4a90e2',
    fontSize: '12px',
  },
};

// Map state to display name
const stateDisplayNames: Record<string, string> = {
  [CoachingState.INTRODUCTION]: 'Introduction',
  [CoachingState.IDENTITY_DISCOVERY]: 'Identity Discovery',
  [CoachingState.IDENTITY_CONFIRMATION]: 'Identity Confirmation',
  [CoachingState.IDENTITY_EXPLORATION]: 'Identity Exploration',
  [CoachingState.IDENTITY_INTEGRATION]: 'Identity Integration',
  [CoachingState.CONCLUSION]: 'Conclusion',
};

// The state flow in order
const stateFlow = [
  CoachingState.INTRODUCTION,
  CoachingState.IDENTITY_DISCOVERY,
  CoachingState.IDENTITY_CONFIRMATION,
  CoachingState.IDENTITY_EXPLORATION,
  CoachingState.IDENTITY_INTEGRATION,
  CoachingState.CONCLUSION,
];

/**
 * Component that displays the current state and available actions.
 */
const StateIndicator: React.FC = () => {
  const { currentState, stateInfo } = useCoach();
  
  if (!stateInfo) {
    return null;
  }
  
  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <h3 style={styles.title}>
          Current State: {stateDisplayNames[currentState] || currentState}
        </h3>
      </div>
      
      <p style={styles.description}>{stateInfo.description}</p>
      
      <div style={styles.stateFlow}>
        {stateFlow.map((state, index) => (
          <React.Fragment key={state}>
            <div
              style={{
                ...styles.state,
                ...(state === currentState ? styles.activeState : styles.inactiveState),
              }}
            >
              {stateDisplayNames[state]}
            </div>
            
            {index < stateFlow.length - 1 && <div style={styles.connector} />}
          </React.Fragment>
        ))}
      </div>
      
      {stateInfo.available_actions.length > 0 && (
        <div style={styles.actionsContainer}>
          <p style={styles.actionTitle}>Available Actions:</p>
          <div style={styles.actionsList}>
            {stateInfo.available_actions.map((action) => (
              <div key={action} style={styles.action}>
                {action}
              </div>
            ))}
          </div>
        </div>
      )}
      
      {stateInfo.next_possible_states.length > 0 && (
        <div style={styles.actionsContainer}>
          <p style={styles.actionTitle}>Next Possible States:</p>
          <div style={styles.actionsList}>
            {stateInfo.next_possible_states.map((state) => (
              <div key={state} style={styles.action}>
                {stateDisplayNames[state] || state}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default StateIndicator;
