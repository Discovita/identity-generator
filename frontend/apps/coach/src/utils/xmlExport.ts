import { DOMImplementation, XMLSerializer, DOMParser } from 'xmldom'
import { ChatMessage } from '../api/types'

const sanitizeContent = (content: string): string => {
  const parser = new DOMParser()
  const doc = parser.parseFromString('<root></root>', 'text/xml')
  const textNode = doc.createTextNode(content)
  return textNode.nodeValue || ''
}

export const convertToXml = (messages: ChatMessage[], userId: string): string => {
  const doc = new DOMImplementation().createDocument(null, 'conversation', null)
  const root = doc.documentElement

  // Create metadata
  const metadata = doc.createElement('metadata')
  root.appendChild(metadata)

  const userIdElement = doc.createElement('userId')
  userIdElement.textContent = userId
  metadata.appendChild(userIdElement)

  const timestamp = doc.createElement('timestamp')
  timestamp.textContent = new Date().toISOString()
  metadata.appendChild(timestamp)

  const messageCount = doc.createElement('messageCount')
  messageCount.textContent = messages.length.toString()
  metadata.appendChild(messageCount)

  // Create messages
  const messagesElement = doc.createElement('messages')
  root.appendChild(messagesElement)

  messages.forEach(msg => {
    const messageElement = doc.createElement('message')
    
    const roleElement = doc.createElement('role')
    roleElement.textContent = msg.role
    messageElement.appendChild(roleElement)

    const contentElement = doc.createElement('content')
    const sanitizedContent = sanitizeContent(msg.content)
    contentElement.appendChild(doc.createCDATASection(sanitizedContent))
    messageElement.appendChild(contentElement)

    messagesElement.appendChild(messageElement)
  })

  return new XMLSerializer().serializeToString(doc)
}

export const downloadXml = (xmlContent: string) => {
  const blob = new Blob([xmlContent], { type: 'application/xml' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `conversation-${new Date().toISOString()}.xml`
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
}
