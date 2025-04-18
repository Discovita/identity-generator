import React from 'react'

export const LoadingBubbles: React.FC = () => {
  return (
    <div className="message assistant loading-bubbles">
      <div className="bubble"></div>
      <div className="bubble"></div>
      <div className="bubble"></div>
      <style>
        {`
          .loading-bubbles {
            display: flex;
            gap: 4px;
            padding: 12px !important;
            min-width: 60px;
          }
          
          .bubble {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background-color: #666;
            animation: bounce 1s infinite;
          }
          
          .bubble:nth-child(2) {
            animation-delay: 0.2s;
          }
          
          .bubble:nth-child(3) {
            animation-delay: 0.4s;
          }
          
          @keyframes bounce {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-5px); }
          }
        `}
      </style>
    </div>
  )
}
