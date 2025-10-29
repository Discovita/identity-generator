import React, { useState } from 'react'
import { workflowService } from '../service/WorkflowService'
import LoadingSpinner from './LoadingSpinner'

const ImageFeedback: React.FC = () => {
  const [feedback, setFeedback] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [isSwapping, setIsSwapping] = useState(false)
  const state = workflowService.getState()
  const { images: imageHistory, selectedIndex } = workflowService.getImageHistory()

  const handleSubmitFeedback = async () => {
    if (feedback.trim()) {
      setIsLoading(true)
      await workflowService.generateImage(feedback)
      setFeedback('')
      setIsLoading(false)
    }
  }

  const handleFinalize = async () => {
    setIsSwapping(true)
    await workflowService.generateFinalResult()
    setIsSwapping(false)
  }

  return (
    <div>
      <h2>Your Vision</h2>
      
      <div style={{
        border: '3px solid #007bff',
        padding: '2px',
        display: 'inline-block'
      }}>
        <img 
          src={state.generatedImageUrl} 
          alt="Generated vision" 
          style={{ maxWidth: '100%', height: 'auto', display: 'block' }}
        />
      </div>

      <div>
        <h3>Previous Versions</h3>
        <div style={{ display: 'flex', gap: '10px', overflowX: 'auto' }}>
          {imageHistory.map((image, index) => (
            <div
              key={index}
              onClick={() => workflowService.selectImage(index)}
              style={{
                position: 'relative',
                cursor: 'pointer',
                border: selectedIndex === index ? '3px solid #007bff' : 'none',
                padding: '2px'
              }}
            >
              <img
                src={image.imageUrl}
                alt={`Version ${index + 1}`}
                style={{ width: '100px', height: '100px', objectFit: 'cover' }}
              />
            </div>
          ))}
        </div>
      </div>

      <div>
        <h3>How would you like to adjust this image?</h3>
        <textarea
          value={feedback}
          onChange={(e) => setFeedback(e.target.value)}
          placeholder="Describe any changes you'd like to make to the image..."
          rows={4}
        />
        
        <div>
          <button onClick={handleSubmitFeedback} disabled={isLoading}>
            {isLoading ? <LoadingSpinner /> : 'Generate New Version'}
          </button>
          <button onClick={handleFinalize} disabled={isSwapping}>
            {isSwapping ? <LoadingSpinner /> : 'Finalize Image'}
          </button>
        </div>
      </div>
    </div>
  )
}

export default ImageFeedback
