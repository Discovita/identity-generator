import React, { useState, useCallback } from 'react';
import { testStates } from '../tests/testStates';
import { ChatInterface } from './ChatInterface';
import { CoachStateVisualizer } from './coach-state-visualizer';
import { CoachResponse, CoachState } from '../types/apiTypes';
import '../styles/coach-state-visualizer.css';

export const TestScreen: React.FC = () => {
  const [selectedState, setSelectedState] = useState('');
  const [hasStarted, setHasStarted] = useState(false);
  // Track current coach state and last response
  const [currentCoachState, setCurrentCoachState] = useState<CoachState | null>(null);
  const [lastResponse, setLastResponse] = useState<CoachResponse | null>(null);

  const userId = React.useMemo(() => Math.random().toString(36).substring(2, 15), []);

  // Callback to receive updated state from ChatInterface
  const handleStateUpdate = useCallback((newState: CoachState, response: CoachResponse) => {
    setCurrentCoachState(newState);
    setLastResponse(response);
  }, []);

  if (hasStarted) {
    const initialState = testStates[selectedState].coach_state;

    return (
      <div className="test-mode">
        <div className="test-header">
          <h2>Test Mode: {testStates[selectedState].name}</h2>
          <button onClick={() => setHasStarted(false)} style={{ padding: '8px 16px' }}>
            Back to Test Selection
          </button>
        </div>

        <div className="test-mode-container">
          <div className="test-mode-chat">
            <ChatInterface
              userId={userId}
              initialCoachState={initialState}
              initialMessages={initialState.conversation_history || []}
              onStateUpdate={handleStateUpdate}
            />
          </div>

          <div className="test-mode-visualizer">
            <CoachStateVisualizer
              coachState={currentCoachState || initialState}
              lastResponse={lastResponse || undefined}
            />
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="test-screen" style={{ padding: '40px' }}>
      <h1>Test State Selection</h1>
      <p>Select a test state to simulate different chat scenarios</p>

      <div className="state-selector" style={{ marginTop: '20px' }}>
        <select
          value={selectedState}
          onChange={e => setSelectedState(e.target.value)}
          style={{ padding: '8px', marginRight: '10px', minWidth: '200px' }}
        >
          <option value="">Select a test state</option>
          {Object.entries(testStates).map(([key, state]) => (
            <option key={key} value={key}>
              {state.name}
            </option>
          ))}
        </select>

        <button
          onClick={() => setHasStarted(true)}
          disabled={!selectedState}
          style={{
            padding: '8px 16px',
            opacity: selectedState ? 1 : 0.5,
          }}
        >
          Start Test
        </button>
      </div>

      {selectedState && (
        <div style={{ marginTop: '20px' }}>
          <h3>Selected State Details:</h3>
          <p>
            <strong>Name:</strong> {testStates[selectedState].name}
          </p>
          <p>
            <strong>Description:</strong> {testStates[selectedState].description}
          </p>
          <p>
            <strong>Current State:</strong> {testStates[selectedState].coach_state.current_state}
          </p>
          <p>
            <strong>Identities:</strong>{' '}
            {testStates[selectedState].coach_state.identities?.length || 0}
          </p>
          <p>
            <strong>Conversation History:</strong>{' '}
            {testStates[selectedState].coach_state.conversation_history?.length || 0} messages
          </p>
        </div>
      )}
    </div>
  );
};
