import React from 'react'
import WelcomeScreen from './components/WelcomeScreen'
import ImageUpload from './components/ImageUpload'
import Questions from './components/Questions'
import ImageFeedback from './components/ImageFeedback'
import ImageGeneration from './components/ImageGeneration'
import FinalResult from './components/FinalResult'
import { WorkflowStep } from './service/WorkflowService'
import { WorkflowProvider, useWorkflow } from './context/WorkflowContext'

const WorkflowContent: React.FC = () => {
  const { state } = useWorkflow()

  const renderCurrentStep = () => {
    switch (state.currentStep) {
      case WorkflowStep.Welcome:
        return <WelcomeScreen />
      case WorkflowStep.UploadImage:
        return <ImageUpload />
      case WorkflowStep.Questions:
        return <Questions />
      case WorkflowStep.ImageGeneration:
        return <ImageGeneration />
      case WorkflowStep.ImageFeedback:
        return <ImageFeedback />
      case WorkflowStep.FinalResult:
        return <FinalResult />
      default:
        return <WelcomeScreen />
    }
  }

  return (
    <div style={{ maxWidth: '800px', margin: '0 auto', padding: '20px' }}>
      {renderCurrentStep()}
      {state.error && (
        <div style={{ color: 'red', marginTop: '20px', textAlign: 'center' }}>
          {state.error}
        </div>
      )}
    </div>
  )
}

const App: React.FC = () => {
  return (
    <WorkflowProvider>
      <WorkflowContent />
    </WorkflowProvider>
  )
}

export default App
