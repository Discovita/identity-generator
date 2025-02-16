import React from 'react'
import { useWorkflow } from '../context/WorkflowContext'
import LoadingSpinner from './LoadingSpinner'

const FinalResult: React.FC = () => {
  const { state } = useWorkflow()

  return (
    <div>
      <h2>Your Vision Board Complete!</h2>
      {state.isLoading && <LoadingSpinner />}
      <p>Here's your personalized vision of your future self:</p>
      
      {!state.isLoading && state.finalResultUrl && (
        <div>
          <img 
            src={state.finalResultUrl} 
            alt="Your future self" 
            style={{ maxWidth: '100%', height: 'auto' }}
          />
        </div>
      )}

      {!state.isLoading && state.baseImageUrl && state.generatedImageUrl && (
        <div>
          <h3>Original Photos</h3>
          <div style={{ display: 'flex', gap: '20px' }}>
            <div>
              <h4>Your Photo</h4>
              <img 
                src={state.baseImageUrl} 
                alt="You, before the transformation" 
                style={{ width: '200px', height: '200px', objectFit: 'cover' }}
              />
            </div>
            <div>
              <h4>Generated Scene</h4>
              <img 
                src={state.generatedImageUrl} 
                alt="Your aspirational setting" 
                style={{ width: '200px', height: '200px', objectFit: 'cover' }}
              />
            </div>
          </div>
        </div>
      )}

      {!state.isLoading && (
        <div>
          <p>
            Remember: This vision board represents your potential future self. 
            Keep it as inspiration for your journey ahead!
          </p>
        </div>
      )}

      {state.error && (
        <div style={{ color: 'red', marginTop: '10px' }}>
          {state.error}
        </div>
      )}
    </div>
  )
}

export default FinalResult
