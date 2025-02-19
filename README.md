# Discovita Apps

This repository contains two applications:
- Face Swapper: A face swapping application
- Coach: An AI coaching application

## Running the Project

To run either application, simply use:

```bash
./scripts/run_project.sh
```

If no app is specified, you will be prompted to choose which app to run. Alternatively, you can specify the app directly:

```bash
./scripts/run_project.sh face-swapper
# or
./scripts/run_project.sh coach
```

The script will:
1. Check for required dependencies (Python, pip, Node.js, npm)
2. Install Python and npm dependencies
3. Build the frontend
4. Start the server

The application will be available at http://localhost:8000
