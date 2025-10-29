# Identity Generator

A web application for generating identity images using AI.

## Prerequisites

- Python 3.9+
- Node.js 16+ and npm

## Local Development

### First Time Setup

Install all dependencies:

```bash
npm run install:all
```

### Running the App

Start both backend and frontend in development mode:

```bash
npm run dev
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000

## Production Build

Build the frontend and prepare for deployment:

```bash
npm run build
```

This builds the frontend and copies static files to `backend/public/`.

## Production Server

Start the production server:

```bash
npm start
```

## Deployment (Render)

- Build Command: `npm run install:all && npm run build`
- Start Command: `npm start`
- Environment Variables:
  - `PORT`: Server port (defaults to 8000)
  - `OPENAI_API_KEY`: Your OpenAI API key
  - `AWS_ACCESS_KEY_ID`: AWS access key for S3
  - `AWS_SECRET_ACCESS_KEY`: AWS secret key for S3
  - `S3_BUCKET`: S3 bucket name
  - `FACESWAP_API_KEY`: Icons8 Face Swap API key
