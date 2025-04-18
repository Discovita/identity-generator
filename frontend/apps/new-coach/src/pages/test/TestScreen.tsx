import React, { useState, useCallback } from 'react';
import { testStates } from '@/tests/testStates';
import { ChatInterface } from '@/pages/test/ChatInterface';
import { CoachStateVisualizer } from '@/pages/test/coach-state-visualizer';
import { CoachResponse, CoachState } from '@/types/apiTypes';
// Import shadcn/ui components
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import {
  Select,
  SelectTrigger,
  SelectContent,
  SelectItem,
  SelectValue,
} from '@/components/ui/select';
import { Label } from '@/components/ui/label';

/**
 * TestScreen Component
 * -------------------
 * 1. Allows the user to select a test state and start a test chat session.
 * 2. Uses shadcn/ui components for all UI elements (Card, Button, Select, Label).
 * 3. Uses Tailwind CSS for all layout, spacing, and color styling.
 * 4. Preserves all business logic and state management from the original implementation.
 * 5. Provides step-by-step comments for clarity and maintainability.
 */
function TestScreen() {
  // State for the selected test state key
  const [selectedState, setSelectedState] = useState('');
  // State for whether the test has started
  const [hasStarted, setHasStarted] = useState(false);
  // Track current coach state and last response
  const [currentCoachState, setCurrentCoachState] = useState<CoachState | null>(null);
  const [lastResponse, setLastResponse] = useState<CoachResponse | null>(null);

  // Generate a random userId for the session
  const userId = React.useMemo(() => Math.random().toString(36).substring(2, 15), []);

  // Callback to receive updated state from ChatInterface
  const handleStateUpdate = useCallback((newState: CoachState, response: CoachResponse) => {
    setCurrentCoachState(newState);
    setLastResponse(response);
  }, []);

  // If the test has started, show the chat and visualizer
  if (hasStarted) {
    const initialState = testStates[selectedState].coach_state;
    return (
      <div className="flex flex-col min-h-screen bg-background-light">
        {/* Header with test name and back button */}
        <div className="sticky top-0 z-20 w-full bg-gold-50 border-b-2 border-gold-200 shadow-gold-md flex items-center justify-between px-6 py-4">
          <h2 className="text-lg font-semibold text-gold-700">
            Test Mode: {testStates[selectedState].name}
          </h2>
          <Button variant="default" size="sm" onClick={() => setHasStarted(false)}>
            Back to Test Selection
          </Button>
        </div>
        {/* Main content: chat and visualizer side by side */}
        <div className="flex flex-col md:flex-row gap-6 p-6 max-w-6xl mx-auto w-full">
          <Card className="flex-1 min-w-0 max-w-2xl bg-white">
            <CardHeader>
              <CardTitle className="text-xl">Chat</CardTitle>
            </CardHeader>
            <CardContent className="p-0">
              <ChatInterface
                userId={userId}
                initialCoachState={initialState}
                initialMessages={initialState.conversation_history || []}
                onStateUpdate={handleStateUpdate}
              />
            </CardContent>
          </Card>
          <Card className="flex-1 min-w-0 max-w-xl bg-white">
            <CardHeader>
              <CardTitle className="text-xl">Coach State Visualizer</CardTitle>
            </CardHeader>
            <CardContent className="p-0">
              <CoachStateVisualizer
                coachState={currentCoachState || initialState}
                lastResponse={lastResponse || undefined}
              />
            </CardContent>
          </Card>
        </div>
      </div>
    );
  }

  // Test state selection screen
  return (
    <div className="flex items-center justify-center min-h-screen bg-background-light w-full h-full">
      <div>
        <Card className="w-full p-8">
          <CardHeader>
            <CardTitle className="text-2xl mb-2">Test State Selection</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-gold-900 mb-6">
              Select a test state to simulate different chat scenarios
            </p>
            {/* State selector form */}
            <form className="flex flex-col gap-4">
              <div className="flex flex-col md:flex-row md:items-center gap-4">
                <Label htmlFor="test-state-select" className="min-w-[120px]">
                  Test State
                </Label>
                <Select value={selectedState} onValueChange={setSelectedState}>
                  <SelectTrigger
                    id="test-state-select"
                    className="min-w-[200px]"
                    aria-label="Select a test state"
                  >
                    <SelectValue placeholder="Select a test state" />
                  </SelectTrigger>
                  <SelectContent>
                    {Object.entries(testStates).map(([key, state]) => (
                      <SelectItem key={key} value={key}>
                        {state.name}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
                <Button
                  type="button"
                  onClick={() => setHasStarted(true)}
                  disabled={!selectedState}
                  className="ml-0 md:ml-2"
                >
                  Start Test
                </Button>
              </div>
            </form>
            {/* Selected state details */}
            {selectedState && (
              <div className="mt-8 bg-gold-50 border border-gold-200 rounded-lg p-4">
                <h3 className="text-lg font-semibold text-gold-700 mb-2">
                  Selected State Details:
                </h3>
                <div className="space-y-1 text-gold-900">
                  <p>
                    <span className="font-semibold">Name:</span> {testStates[selectedState].name}
                  </p>
                  <p>
                    <span className="font-semibold">Description:</span>{' '}
                    {testStates[selectedState].description}
                  </p>
                  <p>
                    <span className="font-semibold">Current State:</span>{' '}
                    {testStates[selectedState].coach_state.current_state}
                  </p>
                  <p>
                    <span className="font-semibold">Identities:</span>{' '}
                    {testStates[selectedState].coach_state.identities?.length || 0}
                  </p>
                  <p>
                    <span className="font-semibold">Conversation History:</span>{' '}
                    {testStates[selectedState].coach_state.conversation_history?.length || 0}{' '}
                    messages
                  </p>
                </div>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

export default TestScreen;
