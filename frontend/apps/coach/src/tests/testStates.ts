import { ChatMessage } from '../api/types'

export interface TestState {
  name: string
  description: string
  messages: ChatMessage[]
}

export const testStates: Record<string, TestState> = {
  initialGreeting: {
    name: 'Initial Greeting',
    description: 'First interaction with Leigh Ann, no prior context',
    messages: [
      {
        role: 'assistant',
        content: "Hi, I'm Leigh Ann, CEO and professional life coach. I'm here to help you design your ideal life through conscious identity creation. What brings you here today?"
      }
    ]
  },

  identityExploration: {
    name: 'Identity Exploration Phase',
    description: 'Mid-conversation exploring identity in career context',
    messages: [
      {
        role: 'user',
        content: "I've been feeling stuck in my career and want to make a change."
      },
      {
        role: 'assistant',
        content: "I understand that feeling of being stuck. Let's explore who you want to be in your career. Instead of focusing on what you do, let's focus on who you are. What kind of professional identity resonates with you? Complete this statement: 'In my career, I am...'"
      },
      {
        role: 'user',
        content: "In my career, I am someone who helps others grow and succeed."
      },
      {
        role: 'assistant',
        content: "That's powerful. You're identifying as a mentor and enabler of success. Let's refine this identity further. When you envision yourself as someone who helps others grow and succeed, what specific qualities do you embody?"
      }
    ]
  },

  identityRefinement: {
    name: 'Identity Refinement Phase',
    description: 'Working on specific identity statements and visualization',
    messages: [
      {
        role: 'user',
        content: "I want to be more confident in my business decisions."
      },
      {
        role: 'assistant',
        content: "Let's create a powerful identity statement around this. Instead of wanting to be more confident, let's declare who you are: 'I am a decisive business leader who trusts their intuition.' How does that identity statement feel to you?"
      },
      {
        role: 'user',
        content: "That feels strong, but also a bit intimidating."
      },
      {
        role: 'assistant',
        content: "That's perfectly normal. Remember, we're not earning this identity - we're choosing it now. Let's visualize you embodying this identity. Picture yourself in your next business meeting, sitting tall, speaking with clarity, and making decisions from a place of inner knowing. Your confidence isn't something you're seeking; it's who you are."
      }
    ]
  },

  multipleIdentities: {
    name: 'Multiple Identities Integration',
    description: 'Exploring how different identities interact',
    messages: [
      {
        role: 'assistant',
        content: "We've identified several powerful identities: the decisive business leader, the nurturing parent, and the health-conscious individual. Let's explore how these identities support each other. How do you see these different aspects of yourself working together?"
      },
      {
        role: 'user',
        content: "Sometimes they feel in conflict, especially balancing business and family."
      },
      {
        role: 'assistant',
        content: "Instead of seeing these identities in conflict, let's create an integrated vision. You are a harmonious blend of all these aspects. Your decisiveness in business enhances your parenting, your nurturing nature enriches your leadership, and your health consciousness gives you the energy for both. What new identity statement could encompass this integration?"
      }
    ]
  }
}
