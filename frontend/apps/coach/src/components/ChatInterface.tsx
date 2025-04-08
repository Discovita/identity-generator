import React, { useState, useRef, useEffect, useCallback } from 'react';
import { CoachState, UserProfile, Message, CoachResponse } from '../types/apiTypes';
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
  initialCoachState?: CoachState;
  onStateUpdate?: (newState: CoachState, response: CoachResponse) => void;
}

export const ChatInterface: React.FC<Props> = ({
  userId,
  initialMessages = [],
  initialCoachState,
  onStateUpdate,
}) => {
  const [messages, setMessages] = useState<Message[]>(initialMessages);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Initialize coach state
  const [coachState, setCoachState] = useState<CoachState>(
    initialCoachState || {
      current_state: CoachingState.INTRODUCTION,
      user_profile: {
        name: userId,
        goals: [],
      } as UserProfile,
      identities: [],
      proposed_identity: null,
      current_identity_id: null,
      conversation_history: initialMessages,
      metadata: {},
    }
  );

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

  const resizeTextarea = useCallback(() => {
    const textarea = textareaRef.current;
    if (!textarea) return;
    textarea.style.height = 'auto';
    textarea.style.height = `${textarea.scrollHeight}px`;

    const maxHeight = 500; // Should match the CSS max-height value
    if (textarea.scrollHeight > maxHeight) {
      textarea.style.height = `${maxHeight}px`;
      textarea.classList.add('overflow');
    } else {
      textarea.classList.remove('overflow');
    }
  }, []);

  const handleInputChange = useCallback(
    (e: React.ChangeEvent<HTMLTextAreaElement>) => {
      setInputMessage(e.target.value);
      resizeTextarea();
    },
    [resizeTextarea]
  );

  useEffect(() => {
    resizeTextarea();
  }, [resizeTextarea]);

  const sendMessage = useCallback(
    async (content: string) => {
      if (!content.trim() || isLoading) return;

      const userMessage: Message = { role: 'user', content: content.trim() };
      setMessages(prev => [...prev, userMessage]);
      setInputMessage('');
      setTimeout(resizeTextarea, 0);
      setIsLoading(true);

      try {
        // Send message without adding to conversation_history (backend will add it)
        const response = await apiClient.sendMessage(content, coachState);
        setMessages(prev => [...prev, { role: 'assistant', content: response.message }]);
        setCoachState(response.coach_state);

        // Notify parent component about state update if callback provided
        if (onStateUpdate) {
          onStateUpdate(response.coach_state, response);
        }
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
    [isLoading, coachState, resizeTextarea, onStateUpdate]
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

  const handleKeyDown = useCallback(
    (e: React.KeyboardEvent) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        handleSubmit(e);
      }
    },
    [handleSubmit]
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
          <textarea
            ref={textareaRef}
            value={inputMessage}
            onChange={handleInputChange}
            onKeyDown={handleKeyDown}
            placeholder="Type your message..."
            disabled={isLoading}
            rows={1}
          />
          <button type="submit" disabled={isLoading}>
            {isLoading ? 'Sending...' : 'Send'}
          </button>
        </form>
        <ConversationExporter messages={messages} userId={userId} coachState={coachState} />
      </div>
    </div>
  );
};
