# Identity Generator

A project containing two applications:
- **Coach**: A coaching interface for managing user identities
- **Face Swapper**: A face swapping application for generating identity images

## Running the Project

To run either application, use:

```bash
./scripts/run_project.sh [app-name]
```

Where `[app-name]` is either `coach` or `face-swapper`. If no app name is provided, you will be prompted to choose one.

The script will:
1. Set up all required dependencies (Python and Node.js)
2. Build the selected frontend application
3. Start the server

The application will be available at `http://localhost:8000`.
