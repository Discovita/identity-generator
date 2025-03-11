import React, { useState, useRef, useEffect, useCallback } from 'react'
import { ChatMessage } from '../api/types'
import { apiClient } from '../api/client'
import { LoadingBubbles } from './LoadingBubbles'
import { ConversationExporter } from './ConversationExporter'
import MarkdownRenderer from './MarkdownRenderer'
import { initialMessage } from '../constants/initialMessage'

interface Props {
  userId: string
  initialMessages?: ChatMessage[]
}

export const ChatInterface: React.FC<Props> = ({ userId, initialMessages = [] }) => {
  const [messages, setMessages] = useState<ChatMessage[]>(initialMessages)
  const [inputMessage, setInputMessage] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  // Add initial message on mount if no messages exist
  useEffect(() => {
    if (messages.length === 0) {
      setMessages([{ role: 'assistant', content: initialMessage }])
    }
  }, [messages.length]) // Include messages.length as dependency

  const scrollToBottom = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth', block: 'end' })
  }, [])

  // Scroll when messages change
  useEffect(scrollToBottom, [messages, scrollToBottom])

  const handleSubmit = useCallback(async (e: React.FormEvent) => {
    e.preventDefault()
    if (!inputMessage.trim() || isLoading) return

    const userMessage: ChatMessage = { role: 'user', content: inputMessage.trim() }
    setMessages(prev => [...prev, userMessage])
    setInputMessage('')
    setIsLoading(true)

    try {
      const response = await apiClient.sendMessage(userId, userMessage.content, messages)
      setMessages(prev => [...prev, { role: 'assistant', content: response.message }])
    } catch (error) {
      console.error('Failed to send message:', error)
      setMessages(prev => [...prev, { role: 'system', content: 'Error sending message. Please try again.' }])
    } finally {
      setIsLoading(false)
    }
  }, [inputMessage, isLoading, messages, userId])

  return (
    <div className="chat-container">
      <div className="messages">
        {messages.map((message, index) => (
          <div key={index} className={`message ${message.role}`}>
            {message.role === 'assistant' ? (
              <MarkdownRenderer content={message.content} />
            ) : (
              message.content
            )}
          </div>
        ))}
        {isLoading && <LoadingBubbles />}
        <div ref={messagesEndRef} />
      </div>
      <div className="chat-controls">
        <form onSubmit={handleSubmit} className="input-form">
          <input
            type="text"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            placeholder="Type your message..."
            disabled={isLoading}
          />
          <button type="submit" disabled={isLoading}>
            {isLoading ? 'Sending...' : 'Send'}
          </button>
        </form>
        <ConversationExporter messages={messages} userId={userId} />
      </div>
    </div>
  )
}
