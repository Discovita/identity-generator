# OpenAI Service Demo Scripts

This directory contains demonstration scripts showing how to use the OpenAI service module.

## Structured Outputs Demo

The `demo_structured_outputs.py` script demonstrates how to use structured outputs with OpenAI to get typed responses using Pydantic models.

### Features Demonstrated

- Creating Pydantic models for structured responses
- Using `create_structured_chat_completion` to get typed responses
- Checking which models support structured outputs
- Error handling and troubleshooting

### Requirements

- Python 3.9+
- An OpenAI API key with access to GPT-4o or another compatible model
- The identity-generator backend package installed

### Running the Demo

1. Set your OpenAI API key as an environment variable:

```bash
export OPENAI_API_KEY=your-openai-api-key
```

2. Optionally, set your OpenAI organization ID:

```bash
export OPENAI_ORG_ID=your-organization-id
```

3. Run the script:

```bash
cd /path/to/identity-generator/backend
python -m discovita.service.openai_new.test.demo_structured_outputs
```

### Expected Output

The script will:
1. Check which models support structured outputs
2. Request a recipe for a vegetarian pasta dish
3. Display the structured recipe information
4. Show the raw JSON output

### Customizing

Feel free to modify the script to try different prompts or create your own Pydantic models for other types of structured data you want to extract. 