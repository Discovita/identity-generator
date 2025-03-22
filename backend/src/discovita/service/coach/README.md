# Coach Service

The Coach Service is a sophisticated AI-powered coaching system designed to help users develop and transform their identities through structured dialogue and visualization. This service implements an identity-focused coaching approach that guides users from unconscious patterns to conscious identity creation.

## Core Components

### 1. Service Architecture

- `service.py`: Main service implementation handling coaching interactions
- `context_builder.py`: Manages conversation context and system prompts
- `prompts.py`: Contains system prompts and dialogue management
- `models/`: Data structures and type definitions

### 2. Key Features

#### Identity Management
- Proposes and confirms user identities
- Supports multiple identity categories:
  - Passions and Talents
  - Money Making/Keeping
  - Spiritual Growth
  - Personal Appearance
  - Physical Expression
  - Family Relations
  - Romantic Relations
  - Action-oriented

#### Visualization Support
- Generates visualization prompts for confirmed identities
- Includes setting, appearance, and energy descriptions
- Helps users embody their chosen identities

## Usage

### Service Initialization

```python
from discovita.service.coach.service import CoachService
from discovita.service.openai.client.client import OpenAIClient

# Initialize the service
client = OpenAIClient()
coach_service = CoachService(client)
```

### Making Requests

```python
from discovita.service.coach.models import CoachRequest, UserProfile, ChatMessage

# Create a request
request = CoachRequest(
    user_id="user123",
    message="I want to explore my professional identity",
    context=[],  # Previous chat messages if any
    profile=None  # Optional user profile
)

# Get response
response = await coach_service.get_response(request)
```

### Response Structure

The service returns a `CoachResponse` with:
- `message`: Coach's text response
- `proposed_identity`: New identity being proposed (if any)
- `confirmed_identity`: Identity being confirmed (if any)
- `visualization_prompt`: Visualization details for the identity

## Identity Creation Process

1. **Exploration Phase**
   - Discuss potential identities through dialogue
   - Focus on one identity at a time
   - Provide detailed context and explanation

2. **Proposal Phase**
   - Present a specific identity for consideration
   - Include name, category, and affirmation
   - Wait for explicit user confirmation

3. **Confirmation Phase**
   - Move proposed identity to confirmed status after user approval
   - Generate visualization prompts
   - Provide embodiment guidance

## Models

### Identity Model
```python
class Identity:
    category: IdentityCategory  # e.g., "passions_and_talents"
    name: str                  # e.g., "Creative Visionary"
    affirmation: str          # "I am" statement
    visualization: Dict        # Visual representation details
```

### Request Model
```python
class CoachRequest:
    user_id: str
    message: str
    context: List[ChatMessage]
    profile: Optional[UserProfile]
```

### Response Model
```python
class CoachResponse:
    message: str
    proposed_identity: Optional[Identity]
    confirmed_identity: Optional[Identity]
    visualization_prompt: Optional[Dict]
```

## Best Practices

1. **Identity Proposal**
   - Only propose one identity at a time
   - Always get explicit user confirmation
   - Provide clear context and reasoning

2. **Conversation Flow**
   - Start with identity exploration
   - Move to specific proposals
   - Confirm and visualize
   - Provide embodiment guidance

3. **Response Guidelines**
   - Keep responses concise but meaningful
   - Include clear next steps or questions
   - Balance guidance with user autonomy

## Error Handling

The service uses Pydantic models for validation, ensuring:
- Valid identity categories
- Required fields are present
- Proper data types
- Structured responses

## Dependencies

- OpenAI API client for LLM interactions
- Pydantic for data validation
- Python 3.7+ for async/await support

## Security Considerations

- User IDs should be properly authenticated
- Conversation context should be securely stored
- Personal information should be handled according to privacy policies 