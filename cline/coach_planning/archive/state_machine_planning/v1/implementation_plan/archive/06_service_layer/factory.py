from ..openai.client.client import OpenAIClient
from .service import CoachService
from .state.machine import CoachStateMachine
from .prompt.manager import PromptManager
from .context.manager import ContextManager
from .action.executor import ActionExecutor
from .persistence.database import DatabaseService

def create_coach_service(
    client: OpenAIClient,
    db_service: DatabaseService
) -> CoachService:
    """Create a coach service with all required components."""
    # Create component instances
    state_machine = CoachStateMachine(db_service)
    prompt_manager = PromptManager()
    context_manager = ContextManager(db_service)
    action_executor = ActionExecutor(context_manager, state_machine, db_service)
    
    # Create and return service
    return CoachService(
        client=client,
        state_machine=state_machine,
        prompt_manager=prompt_manager,
        context_manager=context_manager,
        action_executor=action_executor
    )
