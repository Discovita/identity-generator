# Step 6: Frontend Integration

## Overview

This step implements the frontend components needed to manage state and provide the coaching interface. The frontend will maintain the complete state of the coaching session and pass it with each API request.

## Implementation Details

### State Management

```typescript
// Import shared types from API
import { CoachState, CoachingState, Identity, Message } from '../api/types';

/**
 * Context for the coaching session.
 * Provides access to the current state and message sending functionality.
 */
interface CoachContext {
  /** Current state of the coaching session */
  state: CoachState;
  /** 
   * Send a message to the coach.
   * Updates state automatically with the response.
   */
  sendMessage: (message: string) => Promise<void>;
}

/**
 * Provider component for coach state and functionality.
 * Manages the complete state of the coaching session.
 */
export function CoachProvider({ children }: { children: React.ReactNode }) {
  const [state, setState] = useState<CoachState>(initialState);

  const sendMessage = async (message: string): Promise<void> => {
    const response = await fetch('/api/coach/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message, state })
    });
    
    const { message: coachMessage, state: newState, actions } = await response.json();
    
    setState(newState);
    return coachMessage;
  };

  return (
    <CoachContext.Provider value={{ state, sendMessage }}>
      {children}
    </CoachContext.Provider>
  );
}
```

### Components

1. **ChatInterface**
```typescript
/**
 * Component for displaying the chat interface and handling message input.
 * Shows conversation history and provides message input form.
 */
export function ChatInterface() {
  const { state, sendMessage } = useCoachContext();
  const [input, setInput] = useState('');

  const handleSubmit = async (e: FormEvent): Promise<void> => {
    e.preventDefault();
    if (!input.trim()) return;
    
    setInput('');
    await sendMessage(input);
  };

  return (
    <div className="chat-interface">
      <div className="messages">
        {state.conversationHistory.map((msg, i) => (
          <Message key={i} {...msg} />
        ))}
      </div>
      <form onSubmit={handleSubmit}>
        <input
          value={input}
          onChange={e => setInput(e.target.value)}
          placeholder="Type your message..."
        />
        <button type="submit">Send</button>
      </form>
    </div>
  );
}
```

2. **IdentityList**
```typescript
/**
 * Component for displaying the list of identities.
 * Shows progress (X/5) and acceptance status for each identity.
 */
export function IdentityList() {
  const { state } = useCoachContext();

  return (
    <div className="identity-list">
      <h2>Your Identities ({state.identities.length}/5)</h2>
      {state.identities.map((identity, index) => (
        <IdentityCard
          key={identity.id}
          identity={identity}
          isActive={index === state.currentIdentityIndex}
        />
      ))}
    </div>
  );
}

interface IdentityCardProps {
  identity: Identity;
  isActive: boolean;
}

/**
 * Card component for displaying a single identity.
 * Shows description and acceptance status.
 */
function IdentityCard({ identity, isActive }: IdentityCardProps) {
  return (
    <div 
      className={`identity ${isActive ? 'current' : ''} ${
        identity.isAccepted ? 'accepted' : ''
      }`}
    >
      <p>{identity.description}</p>
      {identity.isAccepted && <span>✓ Accepted</span>}
    </div>
  );
}
```

3. **ProgressIndicator**
```typescript
interface Phase {
  id: CoachingState;
  label: string;
}

const PHASES: Phase[] = [
  { id: CoachingState.INTRODUCTION, label: 'Introduction' },
  { id: CoachingState.IDENTITY_BRAINSTORMING, label: 'Brainstorming' },
  { id: CoachingState.IDENTITY_REFINEMENT, label: 'Refinement' }
];

/**
 * Component for displaying the current phase of the coaching process.
 * Shows progress through the three main phases.
 */
export function ProgressIndicator() {
  const { state } = useCoachContext();

  return (
    <div className="progress-indicator">
      {PHASES.map(phase => (
        <PhaseIndicator
          key={phase.id}
          phase={phase}
          isActive={state.currentState === phase.id}
        />
      ))}
    </div>
  );
}

interface PhaseIndicatorProps {
  phase: Phase;
  isActive: boolean;
}

/**
 * Individual phase indicator component.
 * Shows phase label and active status.
 */
function PhaseIndicator({ phase, isActive }: PhaseIndicatorProps) {
  return (
    <div className={`phase ${isActive ? 'active' : ''}`}>
      {phase.label}
    </div>
  );
}
```

### Testing Strategy

1. **Unit Tests**
   - Test individual components
   - Test state management
   - Test API integration

2. **Integration Tests**
   - Test complete user flows
   - Test state transitions
   - Test error handling

3. **E2E Tests**
   - Test complete coaching process
   - Test state persistence
   - Test UI interactions

## Implementation Steps

1. Create CoachContext and provider
2. Implement core components
3. Add API integration
4. Add error handling
5. Write tests
6. Add loading states and error UI

## Dependencies

- React for UI
- API layer from Step 5
- TypeScript for type safety

## Next Steps

1. Add error boundaries
2. Improve loading states
3. Add animations for state transitions
