import React, { useState } from 'react'
import { ChatInterface } from './components/ChatInterface'
import { DevelopmentWrapper } from './components/DevelopmentWrapper'
import { TestStateSelector } from './components/TestStateSelector'
import { testStates } from './tests/testStates'

const App: React.FC = () => {
  // Generate a random user ID for this session
  const userId = React.useMemo(() => 
    Math.random().toString(36).substring(2, 15), 
    []
  )

  // Debug environment variable
  console.log('REACT_APP_ENABLE_TEST_STATES:', {
    rawValue: process.env.REACT_APP_ENABLE_TEST_STATES,
    type: typeof process.env.REACT_APP_ENABLE_TEST_STATES,
    comparison: process.env.REACT_APP_ENABLE_TEST_STATES === 'true'
  })
  
  const enableTestStates = process.env.REACT_APP_ENABLE_TEST_STATES === 'true'
  const [currentTestState, setCurrentTestState] = useState<string>('')

  if (enableTestStates) {
    return (
      <div className="app">
        <header>
          <h1>Life Coach Chat (Development Mode)</h1>
        </header>
        <TestStateSelector
          onStateSelect={setCurrentTestState}
          currentState={currentTestState}
        />
        <main>
          <DevelopmentWrapper
            userId={userId}
            initialMessages={currentTestState ? testStates[currentTestState].messages : []}
          />
        </main>
      </div>
    )
  }

  return (
    <div className="app">
      <header>
        <h1>Life Coach Chat</h1>
      </header>
      <main>
        <ChatInterface userId={userId} />
      </main>
    </div>
  )
}

export default App
