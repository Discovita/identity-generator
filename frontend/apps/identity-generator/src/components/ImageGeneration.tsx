import React, { useEffect, useRef } from 'react'
import { useWorkflow } from '../context/WorkflowContext'
import LoadingSpinner from './LoadingSpinner'

const ImageGeneration: React.FC = () => {
  const { state, generateImage } = useWorkflow()

  const hasStartedGeneration = useRef(false)

  useEffect(() => {
    if (!hasStartedGeneration.current && !state.isLoading && !state.error) {
      hasStartedGeneration.current = true
      generateImage()
    }
  }, [generateImage, state.isLoading, state.error])

  const handleRetry = () => {
    hasStartedGeneration.current = false
    generateImage()
  }

  return (
    <div>
      <h2>Generating Your Vision</h2>
      <p>Please wait while we create your personalized vision board...</p>

      {state.isLoading && <LoadingSpinner />}

      {state.error && (
        <div style={{ marginTop: '20px' }}>
          <div style={{
            color: 'red',
            marginBottom: '15px',
            padding: '10px',
            border: '1px solid red',
            borderRadius: '4px',
            backgroundColor: '#ffebee'
          }}>
            <strong>Generation Failed</strong>
            <p style={{ margin: '5px 0' }}>
              There was an issue generating your image. Please try again.
            </p>
            <details style={{ marginTop: '10px', fontSize: '0.9em' }}>
              <summary style={{ cursor: 'pointer' }}>Technical details</summary>
              <p style={{ marginTop: '5px' }}>{state.error}</p>
            </details>
          </div>
          <button
            onClick={handleRetry}
            style={{
              padding: '10px 20px',
              fontSize: '16px',
              cursor: 'pointer',
              backgroundColor: '#007bff',
              color: 'white',
              border: 'none',
              borderRadius: '4px'
            }}
          >
            Try Again
          </button>
        </div>
      )}
    </div>
  )
}

export default ImageGeneration
