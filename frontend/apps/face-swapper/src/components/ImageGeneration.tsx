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

  return (
    <div>
      <h2>Generating Your Vision</h2>
      <p>Please wait while we create your personalized vision board...</p>
      
      {state.isLoading && <LoadingSpinner />}

      {state.error && (
        <div style={{ color: 'red', marginTop: '10px' }}>
          {state.error}
        </div>
      )}
    </div>
  )
}

export default ImageGeneration
