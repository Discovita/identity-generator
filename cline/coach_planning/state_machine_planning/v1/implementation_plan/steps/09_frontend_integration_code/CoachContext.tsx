import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { 
  CoachStateResponse, 
  ChatMessage, 
  Identity, 
  CoachingState,
  StateInfoResponse
} from './apiTypes';
import { coachApi } from './api';

// Define the context state type
interface CoachContextState {
  // Session state
  userId: string;
  sessionId: string | null;
  currentState: string;
  stateInfo: StateInfoResponse | null;
  
  // Conversation state
  messages: ChatMessage[];
  isLoading: boolean;
  error: string | null;
  
  // Identity state
  proposedIdentity: Identity | null;
  confirmedIdentity: Identity | null;
  identities: Identity[];
  
  // Actions
  sendMessage: (message: string) => Promise<void>;
  createSession: () => Promise<void>;
  resetSession: () => Promise<void>;
  getStateInfo: () => Promise<void>;
}

// Create the context with a default value
const CoachContext = createContext<CoachContextState | undefined>(undefined);

// Props for the provider component
interface CoachProviderProps {
  userId: string;
  children: ReactNode;
}

// Provider component
export const CoachProvider: React.FC<CoachProviderProps> = ({ userId, children }) => {
  // Session state
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [currentState, setCurrentState] = useState<string>(CoachingState.INTRODUCTION);
  const [stateInfo, setStateInfo] = useState<StateInfoResponse | null>(null);
  
  // Conversation state
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  
  // Identity state
  const [proposedIdentity, setProposedIdentity] = useState<Identity | null>(null);
  const [confirmedIdentity, setConfirmedIdentity] = useState<Identity | null>(null);
  const [identities, setIdentities] = useState<Identity[]>([]);
  
  // Initialize session on component mount
  useEffect(() => {
    createSession();
  }, [userId]);
  
  // Send a message to the coach
  const sendMessage = async (message: string) => {
    if (!sessionId) {
      await createSession();
    }
    
    setIsLoading(true);
    setError(null);
    
    try {
      // Add user message to the conversation
      const userMessage: ChatMessage = { role: 'user', content: message };
      setMessages(prev => [...prev, userMessage]);
      
      // Send the message to the API
      const response = await coachApi.sendMessage({
        user_id: userId,
        message,
        session_id: sessionId || undefined
      });
      
      // Update session state
      setSessionId(response.session_id);
      setCurrentState(response.current_state);
      
      // Update identity state
      if (response.proposed_identity) {
        setProposedIdentity(response.proposed_identity);
      }
      
      if (response.confirmed_identity) {
        setConfirmedIdentity(response.confirmed_identity);
        setIdentities(prev => [...prev, response.confirmed_identity!]);
      }
      
      // Add assistant message to the conversation
      const assistantMessage: ChatMessage = { role: 'assistant', content: response.message };
      setMessages(prev => [...prev, assistantMessage]);
      
      // Get updated state info
      await getStateInfo();
    } catch (err) {
      setError('Failed to send message. Please try again.');
      console.error('Error sending message:', err);
    } finally {
      setIsLoading(false);
    }
  };
  
  // Create a new coaching session
  const createSession = async () => {
    setIsLoading(true);
    setError(null);
    
    try {
      const response = await coachApi.createSession(userId);
      
      // Reset state
      setMessages([]);
      setProposedIdentity(null);
      setConfirmedIdentity(null);
      
      // Update session state
      setStateInfo(response);
      setCurrentState(response.current_state);
      
      // Get the session ID from the API
      const stateResponse = await coachApi.getStateInfo(userId);
      setSessionId(stateResponse.session_id);
    } catch (err) {
      setError('Failed to create session. Please try again.');
      console.error('Error creating session:', err);
    } finally {
      setIsLoading(false);
    }
  };
  
  // Reset the current session
  const resetSession = async () => {
    if (!sessionId) return;
    
    setIsLoading(true);
    setError(null);
    
    try {
      const response = await coachApi.resetSession(sessionId);
      
      // Reset state
      setMessages([]);
      setProposedIdentity(null);
      setConfirmedIdentity(null);
      
      // Update session state
      setStateInfo(response);
      setCurrentState(response.current_state);
    } catch (err) {
      setError('Failed to reset session. Please try again.');
      console.error('Error resetting session:', err);
    } finally {
      setIsLoading(false);
    }
  };
  
  // Get information about the current state
  const getStateInfo = async () => {
    if (!sessionId) return;
    
    try {
      const response = await coachApi.getStateInfo(userId, sessionId);
      setStateInfo(response);
    } catch (err) {
      console.error('Error getting state info:', err);
    }
  };
  
  // Create the context value
  const contextValue: CoachContextState = {
    userId,
    sessionId,
    currentState,
    stateInfo,
    messages,
    isLoading,
    error,
    proposedIdentity,
    confirmedIdentity,
    identities,
    sendMessage,
    createSession,
    resetSession,
    getStateInfo
  };
  
  return (
    <CoachContext.Provider value={contextValue}>
      {children}
    </CoachContext.Provider>
  );
};

// Custom hook to use the coach context
export const useCoach = () => {
  const context = useContext(CoachContext);
  
  if (context === undefined) {
    throw new Error('useCoach must be used within a CoachProvider');
  }
  
  return context;
};
