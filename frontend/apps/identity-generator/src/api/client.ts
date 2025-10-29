import { 
  FaceSwapResponse, 
  GenerateImageRequest, 
  ImageGenerationResponse, 
  UploadResponse,
  DescribeImageRequest,
  DescribeImageResponse
} from './types'

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000/api/v1'

export class ApiClient {
  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    })

    if (!response.ok) {
      throw new Error(`API request failed: ${response.statusText}`)
    }

    return response.json()
  }

  async uploadImage(file: File): Promise<UploadResponse> {
    const formData = new FormData()
    formData.append('file', file)

    const response = await fetch(`${API_BASE_URL}/upload`, {
      method: 'POST',
      body: formData,
    })

    if (!response.ok) {
      throw new Error(`Upload failed: ${response.statusText}`)
    }

    return response.json()
  }

  async generateImage(request: GenerateImageRequest): Promise<ImageGenerationResponse> {
    return this.request<ImageGenerationResponse>('/generate', {
      method: 'POST',
      body: JSON.stringify(request),
    })
  }

  async describeImage(imageUrl: string): Promise<DescribeImageResponse> {
    const request: DescribeImageRequest = { image_url: imageUrl }
    return this.request<DescribeImageResponse>('/describe', {
      method: 'POST',
      body: JSON.stringify(request),
    })
  }

  async swapFaces(request: { baseImageUrl: string, targetImageUrl: string }): Promise<FaceSwapResponse> {
    return this.request<FaceSwapResponse>('/swap', {
      method: 'POST',
      body: JSON.stringify({
        source_url: request.baseImageUrl,
        target_url: request.targetImageUrl,
      }),
    })
  }
}

export const apiClient = new ApiClient()
