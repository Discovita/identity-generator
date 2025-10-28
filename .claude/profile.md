# User Profile: Jake Mirra

## Working Preferences

### Development Workflow
- **Server Management**: I run servers myself - don't start servers for me unless explicitly requested
- **Testing Strategy**: I handle visual inspections and UI testing; Claude should focus on writing automated tests
- **Code Review**: I perform visual inspections of functionality

### Communication Style
- Be concise and direct
- Focus on technical accuracy over validation
- Ask clarifying questions when requirements are ambiguous

## Project Standards

### Code Quality
- Always prefer editing existing files over creating new ones
- Follow existing code patterns and conventions in the codebase
- Write tests for new functionality

### Testing Approach
- Unit tests for business logic
- Integration tests for API endpoints
- I handle manual/visual testing
- Claude writes automated tests

### Documentation
- Only create documentation files when explicitly requested
- Keep inline code comments concise and meaningful
- Update README files when adding significant features

## Technical Context

### Current Project: Face Swap Application
- FastAPI backend
- React frontend
- Python 3.11.6 environment
- Virtual environment managed by run_services.sh

### Preferred Tools & Technologies
- Python with FastAPI for backend
- React for frontend
- Git for version control

## AI Collaboration Guidelines

### Do:
- **Maintain the persistent to-do list**: Always read `.claude/todo.md` at the start of each conversation and update it as work progresses
- Write comprehensive automated tests
- Suggest improvements with clear rationale
- Explain technical decisions
- Use the TodoWrite tool for tracking multi-step tasks within a conversation
- Ask for clarification when uncertain

### Don't:
- Start servers without explicit permission
- Create unnecessary files (especially .md files)
- Over-validate or use excessive praise
- Make assumptions about ambiguous requirements

## Project-Specific Notes

### Face Swap App
- Uses Icons8 API for face swapping
- Integrates with OpenAI for image generation
- S3 for image storage
- Environment variables loaded via .env file

---

**Note**: This profile can be copied to other projects and customized. Teams can use this as a template for establishing AI collaboration standards.

**Last Updated**: 2025-10-28
