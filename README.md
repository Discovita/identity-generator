# Discovita Apps

This repository contains two applications:
- Face Swapper: A face swapping application
- Coach: An AI coaching application

## Local Development

To run either application locally, use:

```bash
./scripts/run_project.sh
```

If no app is specified, you will be prompted to choose which app to run. Alternatively, you can specify the app directly:

```bash
./scripts/run_project.sh face-swapper
# or
./scripts/run_project.sh coach
```

The application will be available at http://localhost:8000

## Deployment

For Render deployment, use:
- Build Command: `./scripts/build.sh <app-name>`
- Start Command: `./scripts/start.sh`
- Environment Variables:
  - `PORT`: Set this to your desired port (the server will automatically bind to 0.0.0.0)

The build script handles all dependency installation and frontend building, while the start script runs the server. For local development, the server runs on localhost:8000 with auto-reload enabled.
