import React, { useState, useRef, useEffect, useCallback } from 'react';
import { CoachState, UserProfile, Message } from '../types/apiTypes';
import { CoachingState } from '../types/enums';
import { apiClient } from '../api/client';
import { LoadingBubbles } from './LoadingBubbles';
import { ConversationExporter } from './ConversationExporter';
import MarkdownRenderer from './MarkdownRenderer';
import { initialMessage } from '../constants/initialMessage';
import { IdentityChoice } from './IdentityChoice';

interface Props {
  userId: string;
  initialMessages?: Message[];
}

export const ChatInterface: React.FC<Props> = ({ userId, initialMessages = [] }) => {
  const [messages, setMessages] = useState<Message[]>(initialMessages);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Initialize coach state
  const [coachState, setCoachState] = useState<CoachState>({
    current_state: CoachingState.INTRODUCTION,
    user_profile: {
      name: userId,
      goals: [],
    } as UserProfile,
    identities: [],
    proposed_identity: null,
    current_identity_index: null,
    conversation_history: initialMessages,
    metadata: {},
  });

  // Add initial message on mount if no messages exist
  useEffect(() => {
    if (messages.length === 0) {
      setMessages([{ role: 'assistant', content: initialMessage }]);
    }
  }, [messages.length]); // Include messages.length as dependency

  const scrollToBottom = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth', block: 'end' });
  }, []);

  // Scroll when messages change
  useEffect(scrollToBottom, [messages, scrollToBottom]);

  const sendMessage = useCallback(
    async (content: string) => {
      if (!content.trim() || isLoading) return;

      const userMessage: Message = { role: 'user', content: content.trim() };
      setMessages(prev => [...prev, userMessage]);
      setInputMessage('');
      setIsLoading(true);

      try {
        // Update coach state with new message
        const updatedState = {
          ...coachState,
          conversation_history: [...(coachState.conversation_history ?? []), userMessage],
        };

        const response = await apiClient.sendMessage(content, updatedState);
        setMessages(prev => [...prev, { role: 'assistant', content: response.message }]);
        setCoachState(response.coach_state);
      } catch (error) {
        console.error('Failed to send message:', error);
        setMessages(prev => [
          ...prev,
          { role: 'system', content: 'Error sending message. Please try again.' },
        ]);
      } finally {
        setIsLoading(false);
      }
    },
    [isLoading, coachState]
  );

  const handleSubmit = useCallback(
    (e: React.FormEvent) => {
      e.preventDefault();
      if (inputMessage.trim()) {
        sendMessage(inputMessage);
      }
    },
    [inputMessage, sendMessage]
  );

  const handleIdentityChoice = useCallback(
    (response: string) => {
      sendMessage(response);
    },
    [sendMessage]
  );

  return (
    <div className="chat-container">
      <div className="messages">
        {messages.map((message, index) => (
          <div key={index} className={`message ${message.role}`}>
            {message.role === 'assistant' ? (
              <>
                <MarkdownRenderer content={message.content} />
                {index === messages.length - 1 && coachState.proposed_identity && !isLoading && (
                  <IdentityChoice
                    identity={coachState.proposed_identity}
                    onChoiceSelected={handleIdentityChoice}
                    disabled={isLoading}
                  />
                )}
              </>
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
            onChange={e => setInputMessage(e.target.value)}
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
  );
};
