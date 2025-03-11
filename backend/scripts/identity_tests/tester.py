"""Core test logic for identity generation."""

from typing import Dict, Any, List
from pprint import pprint

from .api import send_message
from .identity_checker import has_engineer_identity, find_engineer_identity, extract_identities

class IdentityTester:
    """Test harness for identity generation in the coach service."""
    
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session_id = None
        self.conversation_history = []
        self.identities = []
        self.last_user_message = ""
    
    def start_session(self) -> None:
        """Initialize a new coach session."""
        print("Starting a new coach session...")
        self.session_id = f"identity-test-{id(self)}"
        self.conversation_history = []
        self.identities = []
        print(f"Session ID: {self.session_id}")
    
    def process_response(self, response: Dict[str, Any]) -> None:
        """
        Process the coach response, update conversation history, and extract identities.
        
        Args:
            response: The response from the coach API
        """
        # Extract the coach's message
        coach_message = response.get("message", "")
        print("\nCoach response:")
        print(f"{coach_message}\n")
        
        # Update conversation history
        self.conversation_history.append({"role": "assistant", "content": coach_message})
        
        # Extract identities if any
        new_identities = extract_identities(response)
        if new_identities:
            print("Identities generated:")
            for identity in new_identities:
                print(f"- {identity.get('name')}: {identity.get('affirmation')}")
                self.identities.append(identity)
        else:
            print("No identities generated in this response.")
    
    def run_test(self) -> None:
        """Run the identity generation test."""
        self.start_session()
        
        # Initial message to start the conversation
        self.last_user_message = "I want to explore my identity as an engineer."
        print(f"\nUser: {self.last_user_message}")
        
        # Send the message and process the response
        response = send_message(
            self.base_url, 
            self.session_id, 
            self.last_user_message,
            self.conversation_history
        )
        self.conversation_history.append({"role": "user", "content": self.last_user_message})
        self.process_response(response)
        
        # Continue the conversation until the engineer identity is generated or user quits
        self._interactive_conversation()
        
        # Print test results
        self._print_results()
    
    def _interactive_conversation(self) -> None:
        """Continue the conversation interactively until the identity is found or user quits."""
        while not has_engineer_identity(self.identities):
            print("\nThe 'talented engineer' identity has not been generated yet.")
            print("Enter your next message to continue the conversation, or 'q' to quit:")
            user_input = input("> ")
            
            if user_input.lower() in ['q', 'quit', 'exit']:
                print("Test ended by user.")
                break
            
            self.last_user_message = user_input
            print(f"\nUser: {self.last_user_message}")
            
            # Send the message and process the response
            response = send_message(
                self.base_url, 
                self.session_id, 
                self.last_user_message,
                self.conversation_history
            )
            self.conversation_history.append({"role": "user", "content": self.last_user_message})
            self.process_response(response)
    
    def _print_results(self) -> None:
        """Print the test results."""
        # Check if test was successful
        if has_engineer_identity(self.identities):
            print("\n✅ Test successful! The 'talented engineer' identity was generated.")
            # Print the matching identity
            engineer_identity = find_engineer_identity(self.identities)
            if engineer_identity:
                print("\nGenerated identity:")
                pprint(engineer_identity)
        else:
            print("\n❌ Test ended without generating the 'talented engineer' identity.")
        
        # Print summary
        print("\nTest summary:")
        print(f"- Messages exchanged: {len(self.conversation_history) // 2}")
        print(f"- Total identities generated: {len(self.identities)}")
        print("- All identities:")
        for identity in self.identities:
            print(f"  - {identity.get('name')}: {identity.get('affirmation')}")
