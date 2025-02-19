export interface ChatMessage {
  role: string
  content: string
}

export interface CoachRequest {
  user_id: string
  message: string
  context: ChatMessage[]
}

export interface CoachResponse {
  message: string
}
