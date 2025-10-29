import React, { useState } from 'react'
import { workflowService } from '../service/WorkflowService'
import LoadingSpinner from './LoadingSpinner'

const ImageFeedback: React.FC = () => {
  const [feedback, setFeedback] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [isSwapping, setIsSwapping] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const state = workflowService.getState()
  const { images: imageHistory, selectedIndex } = workflowService.getImageHistory()

  const handleSubmitFeedback = async () => {
    if (feedback.trim()) {
      setIsLoading(true)
      setError(null)
      try {
        await workflowService.generateImage(feedback)
        setFeedback('')
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to generate new version')
      } finally {
        setIsLoading(false)
      }
    }
  }

  const handleFinalize = async () => {
    setIsSwapping(true)
    setError(null)
    try {
      await workflowService.generateFinalResult()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to finalize image')
    } finally {
      setIsSwapping(false)
    }
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

        {error && (
          <div style={{
            color: 'red',
            marginBottom: '15px',
            padding: '10px',
            border: '1px solid red',
            borderRadius: '4px',
            backgroundColor: '#ffebee'
          }}>
            <strong>Error</strong>
            <p style={{ margin: '5px 0' }}>
              {error}
            </p>
            <p style={{ margin: '5px 0', fontSize: '0.9em' }}>
              Please try again or adjust your request.
            </p>
          </div>
        )}

        <textarea
          value={feedback}
          onChange={(e) => setFeedback(e.target.value)}
          placeholder="Describe any changes you'd like to make to the image..."
          rows={4}
        />

        <div>
          <button onClick={handleSubmitFeedback} disabled={isLoading || isSwapping}>
            {isLoading ? <LoadingSpinner /> : 'Generate New Version'}
          </button>
          <button onClick={handleFinalize} disabled={isSwapping || isLoading}>
            {isSwapping ? <LoadingSpinner /> : 'Finalize Image'}
          </button>
        </div>
      </div>
    </div>
  )
}

export default ImageFeedback
