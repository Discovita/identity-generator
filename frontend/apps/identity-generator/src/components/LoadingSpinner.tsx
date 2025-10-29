import React from 'react'

const LoadingSpinner: React.FC = () => {
  return (
    <div className="spinner" style={{ margin: '20px auto' }}>
      <style>
        {`
          .spinner {
            width: 70px;
            text-align: center;
          }

          .spinner > div {
            width: 18px;
            height: 18px;
            background-color: #333;
            border-radius: 100%;
            display: inline-block;
            animation: bounce 1.4s infinite ease-in-out both;
            margin: 0 3px;
          }

          .spinner .bounce1 {
            animation-delay: -0.32s;
          }

          .spinner .bounce2 {
            animation-delay: -0.16s;
          }

          @keyframes bounce {
            0%, 80%, 100% { 
              transform: scale(0);
            } 
            40% { 
              transform: scale(1.0);
            }
          }
        `}
      </style>
      <div className="bounce1"></div>
      <div className="bounce2"></div>
      <div className="bounce3"></div>
    </div>
  )
}

export default LoadingSpinner
