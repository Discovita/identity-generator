import React from 'react'
import { ChatMessage } from '../api/types'
import { convertToXml, downloadXml } from '../utils/xmlExport'

interface Props {
  messages: ChatMessage[]
  userId: string
}

export const ConversationExporter: React.FC<Props> = ({ messages, userId }) => {
  const handleExport = () => {
    const xmlContent = convertToXml(messages, userId)
    downloadXml(xmlContent)
  }

  return (
    <button 
      onClick={handleExport}
      disabled={messages.length === 0}
    >
      Export Conversation
    </button>
  )
}
