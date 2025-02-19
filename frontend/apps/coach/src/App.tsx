import React from 'react'
import { ChatInterface } from './components/ChatInterface'

const App: React.FC = () => {
  // Generate a random user ID for this session
  const userId = React.useMemo(() => 
    Math.random().toString(36).substring(2, 15), 
    []
  )

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
