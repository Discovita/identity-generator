import React from 'react'
import { testStates } from '../tests/testStates'

interface TestStateSelectorProps {
  onStateSelect: (stateName: string) => void
  currentState: string
}

export const TestStateSelector: React.FC<TestStateSelectorProps> = ({
  onStateSelect,
  currentState
}) => {
  return (
    <div className="test-state-selector" style={{ margin: '20px', padding: '20px', border: '1px solid #ccc' }}>
      <h3>Test State Selector</h3>
      <select 
        value={currentState}
        onChange={(e) => onStateSelect(e.target.value)}
        style={{ padding: '8px', marginRight: '10px' }}
      >
        <option value="">Select a test state</option>
        {Object.entries(testStates).map(([key, state]) => (
          <option key={key} value={key}>
            {state.name}
          </option>
        ))}
      </select>
      {currentState && (
        <div style={{ marginTop: '10px' }}>
          <strong>Description: </strong>
          {testStates[currentState]?.description}
        </div>
      )}
    </div>
  )
}
