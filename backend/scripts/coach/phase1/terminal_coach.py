"""Terminal interface for the coach service."""

import json
import sys
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Union

# Add the backend directory to the path
current_file = Path(__file__)
backend_dir = current_file.parents[2]  # Go up to backend directory
sys.path.insert(0, str(backend_dir))

from discovita.service.coach.models import (
    ChatMessage,
    CoachingState,
    CoachRequest,
    CoachResponse,
    ContextMetadataKey,
    Identity,
    UserProfile,
)
from discovita.service.coach.service import CoachService
from scripts.coach.phase1.coach_functions import coach_functions


class TerminalCoach:
    """Terminal interface for the coach service.

    This class:
    1. Provides a terminal UI for interacting with the coach
    2. Manages conversation history in memory
    3. Tracks the current coaching state
    4. Stores identities generated during the session
    """

    def __init__(self, coach_service: CoachService):
        """Initialize the terminal coach.

        Args:
            coach_service: The coach service for handling interactions
        """
        # Initialize coach service
        self.coach_service = coach_service

        # Initialize state tracking
        self.conversation_history: List[ChatMessage] = []
        self.current_state = CoachingState.INTRODUCTION
        self.identities: Dict[str, List[Identity]] = {
            "draft": [],  # List of all brainstormed identities
            "refined": [],  # List of refined identities (max 3)
        }
        self.current_focus_identity: Optional[Identity] = None
        self.metadata: Dict[str, Any] = {
            ContextMetadataKey.INTRODUCTION_COMPLETED: False,
            ContextMetadataKey.DRAFT_IDENTITIES: [],
            ContextMetadataKey.CURRENT_IDENTITY_REFINED: False,
            ContextMetadataKey.CURRENT_IDENTITY_VISUALIZED: False,
        }

        # User profile (empty initially)
        self.user_profile = UserProfile(
            user_id="terminal_user", identities=[], current_focus=None
        )

        # Set up function handlers mapping
        self.function_handlers = {
            "add_draft_identity": self._handle_add_draft_identity,
            "add_refined_identity": self._handle_add_refined_identity,
            "set_focus_identity": self._handle_set_focus_identity,
            "mark_identity_visualized": self._handle_mark_identity_visualized,
            "mark_introduction_completed": self._handle_mark_introduction_completed,
            "transition_to_next_state": self._handle_transition_to_next_state,
            "get_coaching_state": self._handle_get_coaching_state,
        }

    async def process_message(self, user_message: str) -> str:
        """Process a user message and generate a response.

        Args:
            user_message: The message from the user

        Returns:
            A response message from the coach
        """
        # Add user message to history
        self.conversation_history.append(ChatMessage(role="user", content=user_message))

        # Create request object
        request = CoachRequest(
            user_id="terminal_user",
            message=user_message,
            context=self.conversation_history.copy(),
            profile=self.user_profile,
        )

        # Get response from coach service
        response = await self.coach_service.get_response(request)

        # Process any state changes or identity updates
        self._update_state(response)

        # Add assistant message to history
        self.conversation_history.append(
            ChatMessage(role="assistant", content=response.message)
        )

        # Check if we should process function calls
        function_response = await self._process_function_calls(response.message)
        if function_response:
            # Add function response to conversation history
            self.conversation_history.append(
                ChatMessage(role="assistant", content=function_response)
            )
            # Return combined response
            return f"{response.message}\n\n[SYSTEM: Function call processed]"

        return response.message

    async def _process_function_calls(self, message: str) -> Optional[str]:
        """Process any function calls in the response message.

        Args:
            message: The response message from the coach service

        Returns:
            Optional function response message
        """
        # Prepare messages for function calling
        messages = []

        # Add appropriate system message for function calling
        system_message = (
            "You are a coaching assistant that has access to specific functions to manage "
            "the coaching session state. Monitor the conversation and call functions when "
            "appropriate to update state, track identities, and manage the coaching flow. "
            "Your goal is to ensure smooth transitions between coaching phases."
        )
        messages.append({"role": "system", "content": system_message})

        # Add conversation history
        for msg in self.conversation_history:
            messages.append({"role": msg.role, "content": msg.content})

        # Build state context for the function caller
        state_context = (
            f"Current coaching state: {self.current_state.value}\n"
            f"Draft identities: {len(self.identities['draft'])}\n"
            f"Refined identities: {len(self.identities['refined'])}\n"
            f"Current focus identity: {self.current_focus_identity.name if self.current_focus_identity else 'None'}\n"
            f"Introduction completed: {self.metadata[ContextMetadataKey.INTRODUCTION_COMPLETED]}\n"
        )
        messages.append({"role": "system", "content": state_context})

        # Call OpenAI with functions
        try:
            function_result = (
                await self.coach_service.client.call_functions_with_responses(
                    input_data=messages,
                    functions=coach_functions,
                    function_handlers={
                        name: self._wrap_function_handler(handler)
                        for name, handler in self.function_handlers.items()
                    },
                    model="gpt-4o",  # Use an appropriate model
                )
            )

            if function_result:
                return function_result
            return None
        except Exception as e:
            print(f"Error calling functions: {e}")
            return None

    def _wrap_function_handler(self, handler: Callable) -> Callable:
        """Wrap a function handler to ensure it receives the correct arguments.

        Args:
            handler: The original handler function

        Returns:
            Wrapped handler function
        """

        def wrapped_handler(args: Dict[str, Any], ctx: Any = None) -> Dict[str, Any]:
            return handler(args)

        return wrapped_handler

    def _update_state(self, response: CoachResponse) -> None:
        """Update the session state based on the coach response.

        This method:
        1. Tracks proposed and confirmed identities
        2. Updates the current state based on the coaching progress
        3. Updates the user profile with new identities

        Args:
            response: The CoachResponse object
        """
        # Handle proposed identity
        if response.proposed_identity:
            proposed = response.proposed_identity
            # Add to draft identities if not already present
            if not any(i.name == proposed.name for i in self.identities["draft"]):
                self.identities["draft"].append(proposed)
                self.metadata[ContextMetadataKey.DRAFT_IDENTITIES] = self.identities[
                    "draft"
                ]

        # Handle confirmed identity
        if response.confirmed_identity:
            confirmed = response.confirmed_identity

            # Add to user profile if not already present
            if not any(i.name == confirmed.name for i in self.user_profile.identities):
                self.user_profile.identities.append(confirmed)

            # Add to refined identities if in refinement state
            if self.current_state == CoachingState.IDENTITY_REFINEMENT:
                if not any(
                    i.name == confirmed.name for i in self.identities["refined"]
                ):
                    if len(self.identities["refined"]) < 3:
                        self.identities["refined"].append(confirmed)
                        # If we have 3 refined identities, mark as ready for visualization
                        if len(self.identities["refined"]) == 3:
                            self.metadata[
                                ContextMetadataKey.CURRENT_IDENTITY_REFINED
                            ] = True

            # Set as current focus for visualization if in visualization state
            if self.current_state == CoachingState.IDENTITY_VISUALIZATION:
                self.current_focus_identity = confirmed
                self.user_profile.current_focus = confirmed.category
                # Mark as visualized
                self.metadata[ContextMetadataKey.CURRENT_IDENTITY_VISUALIZED] = True

        # Update state based on progress
        self._check_state_transition()

    def _check_state_transition(self) -> None:
        """Check if we should transition to a new state based on current progress."""
        # Introduction → Identity Brainstorming
        if self.current_state == CoachingState.INTRODUCTION:
            # Simple heuristic: After 3 exchanges, mark introduction as complete
            if (
                len(self.conversation_history) >= 6
            ):  # 3 user messages + 3 assistant messages
                self.metadata[ContextMetadataKey.INTRODUCTION_COMPLETED] = True
                self.current_state = CoachingState.IDENTITY_BRAINSTORMING

        # Identity Brainstorming → Identity Refinement
        elif self.current_state == CoachingState.IDENTITY_BRAINSTORMING:
            # Transition when we have at least 5 draft identities
            if len(self.identities["draft"]) >= 5:
                self.current_state = CoachingState.IDENTITY_REFINEMENT

        # Identity Refinement → Identity Visualization
        elif self.current_state == CoachingState.IDENTITY_REFINEMENT:
            # Transition when we have 3 refined identities
            if len(self.identities["refined"]) == 3:
                self.current_state = CoachingState.IDENTITY_VISUALIZATION
                # Set first identity as focus
                if self.identities["refined"]:
                    self.current_focus_identity = self.identities["refined"][0]
                    self.user_profile.current_focus = self.identities["refined"][
                        0
                    ].category

    # Function call handlers

    def _handle_add_draft_identity(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Add a new identity to the draft list during brainstorming.

        Args:
            args: Function call arguments containing identity information

        Returns:
            Response with success message and updated state information
        """
        # Extract arguments
        name = args.get("name")
        category = args.get("category")
        affirmation = args.get("affirmation")

        if not all([name, category, affirmation]):
            return {
                "error": "Missing required fields. Please provide name, category, and affirmation."
            }

        # Check if identity with this name already exists
        if any(i.name == name for i in self.identities["draft"]):
            return {
                "success": False,
                "message": f"Identity '{name}' already exists in draft identities.",
            }

        # Create and add identity
        try:
            from discovita.service.coach.models import IdentityCategory

            identity = Identity(
                name=name, category=IdentityCategory(category), affirmation=affirmation
            )

            self.identities["draft"].append(identity)
            self.metadata[ContextMetadataKey.DRAFT_IDENTITIES] = self.identities[
                "draft"
            ]

            # Check for state transition
            self._check_state_transition()

            return {
                "success": True,
                "message": f"Added '{name}' to draft identities. Total draft identities: {len(self.identities['draft'])}",
                "current_state": self.current_state.value,
                "draft_identities_count": len(self.identities["draft"]),
            }
        except Exception as e:
            return {"success": False, "message": f"Error adding identity: {str(e)}"}

    def _handle_add_refined_identity(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Add a confirmed identity to the refined list during refinement.

        Args:
            args: Function call arguments containing identity information

        Returns:
            Response with success message and updated state information
        """
        # Extract arguments
        name = args.get("name")
        category = args.get("category")
        affirmation = args.get("affirmation")
        visualization = args.get("visualization", {})

        if not all([name, category, affirmation]):
            return {
                "error": "Missing required fields. Please provide name, category, and affirmation."
            }

        # Check if we already have 3 refined identities
        if len(self.identities["refined"]) >= 3:
            return {
                "success": False,
                "message": "Already have 3 refined identities. Cannot add more.",
            }

        # Check if identity with this name already exists in refined
        if any(i.name == name for i in self.identities["refined"]):
            return {
                "success": False,
                "message": f"Identity '{name}' already exists in refined identities.",
            }

        # Create and add identity
        try:
            from discovita.service.coach.models import IdentityCategory

            identity = Identity(
                name=name,
                category=IdentityCategory(category),
                affirmation=affirmation,
                visualization=visualization or None,
            )

            # Add to refined identities
            self.identities["refined"].append(identity)

            # Also add to user profile if not present
            if not any(i.name == name for i in self.user_profile.identities):
                self.user_profile.identities.append(identity)

            # If we have 3 refined identities, mark as ready for visualization
            if len(self.identities["refined"]) == 3:
                self.metadata[ContextMetadataKey.CURRENT_IDENTITY_REFINED] = True

            # Check for state transition
            self._check_state_transition()

            return {
                "success": True,
                "message": f"Added '{name}' to refined identities. Total refined identities: {len(self.identities['refined'])}",
                "current_state": self.current_state.value,
                "refined_identities_count": len(self.identities["refined"]),
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error adding refined identity: {str(e)}",
            }

    def _handle_set_focus_identity(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Set a specific identity as the current focus for visualization.

        Args:
            args: Function call arguments containing identity name

        Returns:
            Response with success message and updated state information
        """
        # Extract arguments
        identity_name = args.get("identity_name")

        if not identity_name:
            return {"error": "Missing identity_name parameter."}

        # Find the identity in refined identities
        matching_identities = [
            i for i in self.identities["refined"] if i.name == identity_name
        ]

        if not matching_identities:
            return {
                "success": False,
                "message": f"Identity '{identity_name}' not found in refined identities.",
            }

        # Set as current focus
        self.current_focus_identity = matching_identities[0]
        self.user_profile.current_focus = self.current_focus_identity.category

        # Reset visualization flag when changing focus
        self.metadata[ContextMetadataKey.CURRENT_IDENTITY_VISUALIZED] = False

        return {
            "success": True,
            "message": f"Set '{identity_name}' as current focus identity.",
            "current_focus": identity_name,
            "category": self.current_focus_identity.category.value,
        }

    def _handle_mark_identity_visualized(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Mark the current focus identity as visualized.

        Args:
            args: Empty function call arguments

        Returns:
            Response with success message and updated state information
        """
        if not self.current_focus_identity:
            return {
                "success": False,
                "message": "No current focus identity to mark as visualized.",
            }

        # Mark as visualized
        self.metadata[ContextMetadataKey.CURRENT_IDENTITY_VISUALIZED] = True

        # Check if all identities have been visualized
        visualized_identity_names = []
        for msg in self.conversation_history:
            if (
                msg.role == "assistant"
                and self.current_focus_identity
                and self.current_focus_identity.name in msg.content
            ):
                visualized_identity_names.append(self.current_focus_identity.name)

        # Automatically move to next identity if available
        self._check_move_to_next_identity()

        return {
            "success": True,
            "message": f"Marked '{self.current_focus_identity.name}' as visualized.",
            "unvisualized_count": len(
                [
                    i
                    for i in self.identities["refined"]
                    if i.name not in visualized_identity_names
                ]
            ),
            "next_focus": (
                self.current_focus_identity.name
                if self.current_focus_identity
                else None
            ),
        }

    def _handle_mark_introduction_completed(
        self, args: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Mark the introduction phase as completed to progress to identity brainstorming.

        Args:
            args: Empty function call arguments

        Returns:
            Response with success message and updated state information
        """
        # Only valid in introduction state
        if self.current_state != CoachingState.INTRODUCTION:
            return {
                "success": False,
                "message": f"Already past introduction phase. Current state: {self.current_state.value}",
            }

        # Mark introduction as completed
        self.metadata[ContextMetadataKey.INTRODUCTION_COMPLETED] = True

        # Transition to next state
        self.current_state = CoachingState.IDENTITY_BRAINSTORMING

        return {
            "success": True,
            "message": "Introduction phase completed. Transitioned to identity brainstorming.",
            "current_state": self.current_state.value,
        }

    def _handle_transition_to_next_state(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Force a transition to the next state in the coaching flow.

        Args:
            args: Function call arguments containing target state

        Returns:
            Response with success message and updated state information
        """
        # Extract arguments
        target_state = args.get("target_state")

        if not target_state:
            return {"error": "Missing target_state parameter."}

        # Validate target state
        try:
            new_state = CoachingState(target_state)

            # Check if transition is valid based on current state
            current_idx = list(CoachingState).index(self.current_state)
            target_idx = list(CoachingState).index(new_state)

            # Only allow forward transitions or staying in same state
            if target_idx < current_idx:
                return {
                    "success": False,
                    "message": f"Cannot transition backward from {self.current_state.value} to {target_state}.",
                }

            # Set new state
            self.current_state = new_state

            # Update relevant metadata for the state
            if new_state == CoachingState.IDENTITY_BRAINSTORMING:
                self.metadata[ContextMetadataKey.INTRODUCTION_COMPLETED] = True
            elif new_state == CoachingState.IDENTITY_REFINEMENT:
                # Ensure we have enough draft identities
                if len(self.identities["draft"]) < 5:
                    return {
                        "success": False,
                        "message": f"Need at least 5 draft identities for refinement. Current count: {len(self.identities['draft'])}",
                    }
            elif new_state == CoachingState.IDENTITY_VISUALIZATION:
                # Ensure we have refined identities
                if not self.identities["refined"]:
                    return {
                        "success": False,
                        "message": "Need refined identities for visualization.",
                    }

                # Set first identity as focus if not set
                if not self.current_focus_identity and self.identities["refined"]:
                    self.current_focus_identity = self.identities["refined"][0]
                    self.user_profile.current_focus = (
                        self.current_focus_identity.category
                    )

                self.metadata[ContextMetadataKey.CURRENT_IDENTITY_REFINED] = True

            return {
                "success": True,
                "message": f"Transitioned to {target_state} state.",
                "current_state": self.current_state.value,
                "previous_state": (
                    self.current_state.value
                    if target_state == self.current_state.value
                    else None
                ),
            }
        except ValueError:
            return {
                "success": False,
                "message": f"Invalid target state: {target_state}",
            }

    def _handle_get_coaching_state(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Get the current coaching state and relevant metrics.

        Args:
            args: Empty function call arguments

        Returns:
            Response with current state information
        """
        # Build state information
        state_info = {
            "current_state": self.current_state.value,
            "draft_identities_count": len(self.identities["draft"]),
            "refined_identities_count": len(self.identities["refined"]),
            "current_focus_identity": (
                self.current_focus_identity.name
                if self.current_focus_identity
                else None
            ),
            "introduction_completed": self.metadata.get(
                ContextMetadataKey.INTRODUCTION_COMPLETED, False
            ),
            "identity_refined": self.metadata.get(
                ContextMetadataKey.CURRENT_IDENTITY_REFINED, False
            ),
            "identity_visualized": self.metadata.get(
                ContextMetadataKey.CURRENT_IDENTITY_VISUALIZED, False
            ),
            "conversation_turns": len(self.conversation_history)
            // 2,  # Approximate turns
        }

        # Add state-specific information
        if self.current_state == CoachingState.IDENTITY_BRAINSTORMING:
            state_info["draft_identities"] = [i.name for i in self.identities["draft"]]
        elif self.current_state == CoachingState.IDENTITY_REFINEMENT:
            state_info["refined_identities"] = [
                i.name for i in self.identities["refined"]
            ]

        return state_info

    async def run_terminal_interface(self) -> None:
        """Run the terminal interface for the coach chatbot."""
        print("Welcome to the Coach Chatbot!")
        print("Type 'exit' to quit the conversation.\n")

        # Initial message from the coach
        init_message = "Hello! I'm Leigh Ann, your personal coach. I'm here to help you explore and develop powerful identities that align with your goals and values. How are you today?"
        print(f"Coach: {init_message}")

        while True:
            # Get user input
            user_input = input("\nYou: ")

            # Check for exit command
            if user_input.lower() in ["exit", "quit", "bye"]:
                print("\nCoach: Thank you for the conversation! Goodbye!")
                break

            # Process message and get response
            coach_response = await self.process_message(user_input)

            # Display response
            print(f"\nCoach: {coach_response}")

            # Display current state information (for debugging)
            state_info = f"\n[DEBUG] Current state: {self.current_state.value}"
            if self.current_state == CoachingState.IDENTITY_BRAINSTORMING:
                state_info += f", Draft identities: {len(self.identities['draft'])}"
            elif self.current_state == CoachingState.IDENTITY_REFINEMENT:
                state_info += f", Refined identities: {len(self.identities['refined'])}"
            elif self.current_state == CoachingState.IDENTITY_VISUALIZATION:
                current_identity = (
                    self.current_focus_identity.name
                    if self.current_focus_identity
                    else "None"
                )
                state_info += f", Current focus: {current_identity}"
                state_info += f", Visualized: {self.metadata[ContextMetadataKey.CURRENT_IDENTITY_VISUALIZED]}"
            print(state_info)

            # Special handling for identity visualization state - move to next identity
            self._check_move_to_next_identity()

    def _check_move_to_next_identity(self) -> None:
        """Check if we should move to the next identity for visualization."""
        if (
            self.current_state == CoachingState.IDENTITY_VISUALIZATION
            and self.metadata[ContextMetadataKey.CURRENT_IDENTITY_VISUALIZED]
            and len(self.identities["refined"]) > 0
        ):

            # Find which identities have been visualized
            visualized_identity_names = []
            for msg in self.conversation_history:
                if (
                    msg.role == "assistant"
                    and self.current_focus_identity
                    and self.current_focus_identity.name in msg.content
                ):
                    visualized_identity_names.append(self.current_focus_identity.name)

            # Check if there are unvisualized identities
            unvisualized_identities = [
                i
                for i in self.identities["refined"]
                if i.name not in visualized_identity_names
            ]

            if unvisualized_identities:
                # Move to the next unvisualized identity
                self.current_focus_identity = unvisualized_identities[0]
                self.user_profile.current_focus = self.current_focus_identity.category
                self.metadata[ContextMetadataKey.CURRENT_IDENTITY_VISUALIZED] = False
                print(
                    f"\n[DEBUG] Moving to next identity: {self.current_focus_identity.name}"
                )
