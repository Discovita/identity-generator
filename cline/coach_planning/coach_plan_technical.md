# Technical Plan: Leigh Ann Coaching Implementation

## Current Architecture

The coaching system consists of:

1. **API Layer** (`/api/routes/coach.py`)
   - Single POST endpoint `/user_input`
   - Handles user messages and context
   - Uses FastAPI dependency injection

2. **Service Layer** (`/service/coach/service.py`)
   - `CoachService` class manages coaching interactions
   - Uses OpenAI GPT-4 for responses
   - Basic system prompt without personality

3. **Data Models** (`/service/coach/models.py`)
   - `ChatMessage`: Individual message with role and content
   - `CoachRequest`: User ID, message, and conversation context
   - `CoachResponse`: Coach's response message

4. **Frontend** (`frontend/apps/coach`)
   - React application
   - Maintains conversation state client-side
   - No persistent storage

## Required Changes

### 1. System Prompt Enhancement
Replace basic coaching prompt with Leigh Ann's personality:

```python
SYSTEM_PROMPT = """You are Leigh Ann, the CEO and professional life coach. Your approach combines:

1. Identity-Focused Coaching
   - Help clients design their ideal life through conscious identity creation
   - Guide them to embody new identities immediately rather than "earning" them
   - Use powerful "I am" statements and identity refinement

2. Communication Style
   - Direct and empowering
   - Focus on bringing subconscious patterns into conscious awareness
   - Transform survival mode into active creation
   - Use metaphors and visualizations effectively

3. Structured Process
   - Start with identity exploration across key life areas
   - Guide identity refinement through specific examples
   - Help clients embody new identities through visualization
   - Maintain focus on transformation and alignment

4. Key Principles
   - Life happens by design, not accident
   - Identity drives behavior
   - Transformation requires conscious choice
   - Support through technology tools

Reference the sample dialogue for specific examples of interaction style and methodology.
"""
```

### 2. Enhanced Request/Response Models

```python
class IdentityCategory(str, Enum):
    PASSIONS = "passions_and_talents"
    MONEY_MAKER = "maker_of_money"
    MONEY_KEEPER = "keeper_of_money"
    SPIRITUAL = "spiritual"
    APPEARANCE = "personal_appearance"
    HEALTH = "physical_expression"
    FAMILY = "familial_relations"
    ROMANTIC = "romantic_relation"
    ACTION = "doer_of_things"

class Identity(BaseModel):
    category: IdentityCategory
    name: str
    affirmation: str
    visualization: Optional[dict] = None

class UserProfile(BaseModel):
    user_id: str
    identities: List[Identity] = Field(default_factory=list)
    current_focus: Optional[IdentityCategory] = None

class CoachRequest(BaseModel):
    user_id: str
    message: str
    context: List[ChatMessage]
    profile: Optional[UserProfile] = None

class CoachResponse(BaseModel):
    message: str
    suggested_identities: Optional[List[Identity]] = None
    visualization_prompt: Optional[dict] = None
```

### 3. Service Layer Enhancements

```python
class CoachService:
    def __init__(self, client: OpenAIClient):
        self.client = client
        self._load_sample_dialogue()
    
    def _load_sample_dialogue(self):
        """Load sample dialogue for reference in prompts."""
        # Load and process sample dialogue
        
    async def get_response(
        self,
        message: str,
        context: List[ChatMessage],
        profile: Optional[UserProfile] = None
    ) -> CoachResponse:
        """Enhanced response generation with identity tracking."""
        # Build context with profile
        # Generate response
        # Extract suggested identities
        # Generate visualization if needed
```

## Implementation Steps

1. **Model Updates** (1-2 hours)
   - Create new model classes
   - Add validation and documentation
   - Update existing code to use new models

2. **Service Layer** (2-3 hours)
   - Implement enhanced CoachService
   - Add identity tracking
   - Add visualization support
   - Add sample dialogue integration

3. **API Updates** (1 hour)
   - Update route to handle new request/response models
   - Add error handling for new fields
   - Update API documentation

4. **Testing** (2-3 hours)
   - Unit tests for new models
   - Integration tests for service layer
   - API endpoint tests
   - Sample dialogue validation

## Testing Strategy

1. **Unit Tests**
   ```python
   def test_identity_creation():
       """Test identity model creation and validation."""
       
   def test_profile_management():
       """Test user profile updates and validation."""
       
   def test_coach_response_generation():
       """Test response generation with identity tracking."""
   ```

2. **Integration Tests**
   ```python
   async def test_full_coaching_session():
       """Test complete coaching interaction flow."""
       
   async def test_identity_refinement():
       """Test identity refinement process."""
   ```

3. **Validation Tests**
   ```python
   def test_sample_dialogue_alignment():
       """Verify responses align with sample dialogue style."""
   ```

## Next Steps

1. Implement model changes
2. Update service layer
3. Enhance API
4. Add tests
5. Validate against sample dialogue
6. Plan frontend updates for new features

## Future Considerations

1. Database persistence for user profiles
2. Analytics on identity progression
3. Enhanced visualization capabilities
4. Multi-session coaching journeys
