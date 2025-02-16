import { apiClient } from '../api/client'
import { GenerateImageRequest } from '../api/types'

export enum WorkflowStep {
  Welcome = 'welcome',
  UploadImage = 'upload',
  Questions = 'questions',
  ImageGeneration = 'generation',
  ImageFeedback = 'feedback',
  FinalResult = 'result',
}

export interface WorkflowState {
  currentStep: WorkflowStep
  baseImageUrl?: string
  userDescription?: string
  setting?: string
  outfit?: string
  emotion?: string
  generatedImageUrl?: string
  augmentedPrompt?: string
  finalResultUrl?: string
  isLoading: boolean
  error?: string
}

export interface ImageCache {
  imageUrl: string
  augmentedPrompt: string
}

export class WorkflowService {
  private state: WorkflowState = {
    currentStep: WorkflowStep.Welcome,
    isLoading: false,
  }

  private imageHistory: ImageCache[] = []
  private selectedImageIndex: number = -1  // -1 means latest image is selected
  private subscribers: Array<() => void> = []

  subscribe(callback: () => void): void {
    this.subscribers.push(callback)
  }

  unsubscribe(callback: () => void): void {
    this.subscribers = this.subscribers.filter(sub => sub !== callback)
  }

  getState(): WorkflowState {
    return { ...this.state }
  }

  setState(newState: Partial<WorkflowState>): void {
    this.state = { ...this.state, ...newState }
    this.subscribers.forEach(callback => callback())
  }

  startWorkflow(): void {
    this.setState({ currentStep: WorkflowStep.UploadImage })
  }

  async uploadBaseImage(file: File): Promise<void> {
    this.setState({ isLoading: true, error: undefined })
    try {
      const uploadResponse = await apiClient.uploadImage(file)
      const describeResponse = await apiClient.describeImage(uploadResponse.url)
      
      this.setState({
        baseImageUrl: uploadResponse.url,
        userDescription: describeResponse.description,
        currentStep: WorkflowStep.Questions,
        isLoading: false,
      })
    } catch (error) {
      this.setState({ 
        error: error instanceof Error ? error.message : 'Failed to upload image',
        isLoading: false 
      })
    }
  }

  setQuestionResponses(setting: string, outfit: string, emotion: string): void {
    this.setState({
      setting,
      outfit,
      emotion,
      currentStep: WorkflowStep.ImageGeneration,
    })
  }

  async generateImage(userFeedback?: string): Promise<void> {
    this.setState({ isLoading: true, error: undefined })
    try {
      const request: GenerateImageRequest = {
        setting: this.state.setting!,
        outfit: this.state.outfit!,
        emotion: this.state.emotion!,
        userFeedback,
        previousAugmentedPrompt: this.state.augmentedPrompt,
        userDescription: this.state.userDescription,
      }

      const response = await apiClient.generateImage(request)
      
      this.imageHistory.push({
        imageUrl: response.imageUrl,
        augmentedPrompt: response.augmentedPrompt,
      })

      this.selectedImageIndex = -1
      this.setState({
        generatedImageUrl: response.imageUrl,
        augmentedPrompt: response.augmentedPrompt,
        currentStep: WorkflowStep.ImageFeedback,
        isLoading: false,
      })
    } catch (error) {
      this.setState({ 
        error: error instanceof Error ? error.message : 'Failed to generate image',
        isLoading: false 
      })
    }
  }

  async generateFinalResult(): Promise<void> {
    this.setState({ isLoading: true, error: undefined })
    try {
      const response = await apiClient.swapFaces({
        baseImageUrl: this.state.baseImageUrl!,
        targetImageUrl: this.state.generatedImageUrl!,
      })

      this.setState({
        finalResultUrl: response.url,
        currentStep: WorkflowStep.FinalResult,
        isLoading: false,
      })
    } catch (error) {
      this.setState({ 
        error: error instanceof Error ? error.message : 'Failed to swap faces',
        isLoading: false 
      })
    }
  }

  getImageHistory(): { images: ImageCache[], selectedIndex: number } {
    return {
      images: [...this.imageHistory],
      selectedIndex: this.selectedImageIndex
    }
  }

  selectImage(index: number): void {
    if (index >= -1 && index < this.imageHistory.length) {
      this.selectedImageIndex = index
      const imageToUse = index === -1 
        ? this.imageHistory[this.imageHistory.length - 1]
        : this.imageHistory[index]
      
      this.setState({
        generatedImageUrl: imageToUse.imageUrl,
        augmentedPrompt: imageToUse.augmentedPrompt
      })
    }
  }
}

export const workflowService = new WorkflowService()
