import React, { useState } from 'react'
import { workflowService } from '../service/WorkflowService'

const Questions: React.FC = () => {
  const [setting, setSetting] = useState('')
  const [outfit, setOutfit] = useState('')
  const [emotion, setEmotion] = useState('')

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    workflowService.setQuestionResponses(setting, outfit, emotion)
  }

  return (
    <div>
      <h2>Envision Your Future Self</h2>
      <p>
        Take a moment to visualize yourself having accomplished your most ambitious
        life goals. Answer these questions about that vision:
      </p>

      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="setting">What is the setting?</label>
          <input
            id="setting"
            type="text"
            value={setting}
            onChange={(e) => setSetting(e.target.value)}
            placeholder="e.g., A modern tech office overlooking the city"
            required
          />
        </div>

        <div>
          <label htmlFor="outfit">What are you wearing?</label>
          <input
            id="outfit"
            type="text"
            value={outfit}
            onChange={(e) => setOutfit(e.target.value)}
            placeholder="e.g., A sleek business suit with modern accessories"
            required
          />
        </div>

        <div>
          <label htmlFor="emotion">What is the emotion?</label>
          <input
            id="emotion"
            type="text"
            value={emotion}
            onChange={(e) => setEmotion(e.target.value)}
            placeholder="e.g., Confident and accomplished"
            required
          />
        </div>

        <button type="submit">
          Generate My Vision
        </button>
      </form>
    </div>
  )
}

export default Questions
