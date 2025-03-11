# Identity Extraction Implementation Trace

## Current Implementation

The core of our identity extraction is implemented through structured LLM responses:

1. **Models** (`models.py`)
   - `Identity`: Structured representation of a user's identity
     ```python
     class Identity(BaseModel):
         category: IdentityCategory
         name: str
         affirmation: str
         visualization: Optional[Dict]
     ```
   - `CoachResponse`: Contains extracted identities from LLM
     ```python
     class CoachResponse(BaseModel):
         message: str
         suggested_identities: Optional[List[Identity]]
         visualization_prompt: Optional[Dict]
     ```

2. **Structured Response** (`structured_response.py`)
   - Defines expected LLM output structure
   - Ensures type safety through Pydantic model
   ```python
   class CoachStructuredResponse(BaseModel):
       message: str
       identities: Optional[List[Identity]]
   ```

3. **Service Implementation** (`service.py`)
   - Uses OpenAI client's structured completion
   - Extracts identities directly from LLM response
   ```python
   structured_response = await self.client.get_structured_completion(
       messages=[...],
       response_model=CoachStructuredResponse
   )
   ```

## Work Needed

0. **Sanity Check**
   - Write a script in ./backend/scripts that tests our newly
     implemented API function for chat with identity extraction.
     The test should introduce a scenario where the coach obviously
     should produce an identity for the user and ensure it does.
     This will be an integration test script - it will run the
     code with a live OpenAI API key.

1. **LLM Prompt Enhancement**
   - Define clear markers for identity categories
   - Ensure consistent "I am" statement formatting
   - Ensure the LLM does not overwhelm the user with trying to 
     define many identities at once. It should encourage the user
     to focus on one at a time.

2. **Response Validation**
   - Add validation to ensure extracted identities match expected format
   - Handle cases where LLM response doesn't contain identities
   - Verify category assignments are valid

3. **Identity Context**
   - Track previously extracted identities
   - Allow refinement of existing identities
   - Handle identity evolution over conversation

The key focus should be on ensuring reliable identity extraction through proper LLM prompting and structured responses, removing the need for post-processing parsing.
