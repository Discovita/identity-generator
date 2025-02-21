import React from 'react'
import { ChatInterface } from './components/ChatInterface'
import { TestScreen } from './components/TestScreen'
import config from './config'

const App: React.FC = () => {
  const userId = React.useMemo(() => 
    Math.random().toString(36).substring(2, 15), 
    []
  )

  if (config.enableTestStates) {
    return <TestScreen />
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
