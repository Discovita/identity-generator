import React from 'react'
import { workflowService } from '../service/WorkflowService'

const WelcomeScreen: React.FC = () => {
  const handleStart = () => {
    workflowService.startWorkflow()
  }

  return (
    <div>
      <h1>Welcome to DiscoVita Vision Board</h1>
      <p>
        Visualize your future self by creating an AI-powered vision board 
        that puts you in the picture of your dreams.
      </p>
      <p>
        Through this journey, you'll:
      </p>
      <ul>
        <li>Upload a photo of yourself</li>
        <li>Describe your dream scenario</li>
        <li>See yourself in that vision</li>
        <li>Refine the image until it's perfect</li>
      </ul>
      <p>
        Ready to see yourself in your dream future?
      </p>
      <button onClick={handleStart}>
        Start My Vision Board
      </button>
    </div>
  )
}

export default WelcomeScreen
