Yes, OpenAI's API provides a way to force structured responses in JSON format using their SDK. This feature is called "Structured Outputs" and it ensures that the model generates responses adhering to a specified JSON schema[7].

For Python and FastAPI, you can use the `pydantic` library to define your desired data structure. Here's how you can implement it:

1. Define your data structure using `pydantic`:

```python
from pydantic import BaseModel
from typing import List

class EntitiesModel(BaseModel):
    attributes: List[str]
    colors: List[str]
    animals: List[str]
```

2. Use the OpenAI SDK to make the API call with the structured output:

```python
from openai import OpenAI

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "Extract entities from the input text"},
        {"role": "user", "content": "The quick brown fox jumps over the lazy dog with piercing blue eyes"},
    ],
    response_format=EntitiesModel
)

parsed_response = response.choices[0].message.parsed
print(parsed_response)
```

This approach ensures that the API returns a response that matches your defined structure[7]. If the model can't generate a valid response according to the schema, it will return a refusal message instead[7].

When integrating this with FastAPI, you can create an endpoint that uses this structured output:

```python
from fastapi import FastAPI
from openai import OpenAI

app = FastAPI()
client = OpenAI()

@app.post("/extract_entities")
async def extract_entities(text: str):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Extract entities from the input text"},
            {"role": "user", "content": text},
        ],
        response_format=EntitiesModel
    )
    return response.choices[0].message.parsed
```

This method provides a clean, type-safe way to get structured responses from OpenAI's API, which can be easily integrated into your FastAPI server[5][7].
