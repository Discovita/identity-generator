import React, { useRef } from 'react'
import { useWorkflow } from '../context/WorkflowContext'
import LoadingSpinner from './LoadingSpinner'

const ImageUpload: React.FC = () => {
  const fileInputRef = useRef<HTMLInputElement>(null)
  const { state, uploadBaseImage } = useWorkflow()

  const handleFileChange = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (!file) return

    await uploadBaseImage(file)
  }

  const handleClick = () => {
    fileInputRef.current?.click()
  }

  return (
    <div>
      <h2>Upload Your Headshot</h2>
      <p>Please upload a clear photo of your face to begin the transformation journey.</p>
      
      <input
        type="file"
        ref={fileInputRef}
        onChange={handleFileChange}
        accept="image/*"
        style={{ display: 'none' }}
      />
      
      <button onClick={handleClick} disabled={state.isLoading}>
        {state.isLoading ? 'Uploading...' : 'Choose Photo'}
      </button>

      {state.isLoading && <LoadingSpinner />}

      {state.error && (
        <div style={{ color: 'red', marginTop: '10px' }}>
          {state.error}
        </div>
      )}
    </div>
  )
}

export default ImageUpload
