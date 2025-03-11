# Coach Chat Logic Trace

This document traces the lifecycle of a chat request through the coaching system.

## Example Request Flow

Consider a user message: "I want to explore my creative identity"

### 1. API Entry Point (routes/coach.py)
```python
POST /user_input
{
    "user_id": "user123",
    "message": "I want to explore my creative identity",
    "context": [], # Previous messages if any
    "profile": {   # Optional user profile
        "user_id": "user123",
        "identities": [],
        "current_focus": "passions_and_talents"
    }
}
```

### 2. Service Layer (service.py)
CoachService receives the request and processes it in several steps:

a) Context Building:
```
system: [System prompt about being Leigh Ann...]
system: [Sample dialogue for reference...]
system: Current user profile:
Identities: []
Current focus: PASSIONS
user: I want to explore my creative identity
```

b) OpenAI Response:
```
"Let's explore that! I hear you wanting to step into your creative power.

For your Passions & Talents:
I am a Creative Visionary - I bring bold, beautiful ideas to life with imagination and purpose."
```

### 3. Identity Processing
IdentityProcessor parses the response:
- Detects category markers ("For your Passions & Talents" → PASSIONS)
- Finds "I am" statements
- Extracts identity name (removes "a"/"an" prefixes)
- Creates Identity objects with visualization details

### 4. Final Response
```python
{
    "message": "Let's explore that!...",
    "suggested_identities": [{
        "category": "passions_and_talents",
        "name": "Creative Visionary",
        "affirmation": "I am a Creative Visionary - I bring bold, beautiful ideas to life",
        "visualization": {
            "setting": "Professional environment",
            "appearance": "Confident and capable",
            "energy": "Focused and determined"
        }
    }],
    "visualization_prompt": {
        "setting": "Professional environment",
        "appearance": "Confident and capable",
        "energy": "Focused and determined"
    }
}
```

## Frontend Integration

The frontend can use this response to:
1. Display the coach's message
2. Update the user's profile with new identities
3. Show visualization prompts to help the user embody their new identity

Each subsequent message includes:
- Growing conversation context
- User's evolving profile
- Current identity focus

This allows the coach to maintain continuity and track the user's identity development journey.
