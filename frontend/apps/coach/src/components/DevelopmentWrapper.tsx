import React from 'react'
import { ChatInterface } from './ChatInterface'
import { ChatMessage } from '../api/types'

interface DevelopmentWrapperProps {
  userId: string
  initialMessages?: ChatMessage[]
}

export const DevelopmentWrapper: React.FC<DevelopmentWrapperProps> = ({
  userId,
  initialMessages = []
}) => {
  return <ChatInterface userId={userId} initialMessages={initialMessages} />
}
