from typing import Dict, Any, Optional
import aiohttp
import json

class LLMService:
    def __init__(self, api_key: str, model: str = "gpt-4"):
        self.api_key = api_key
        self.model = model
        self.api_url = "https://api.openai.com/v1/chat/completions"
    
    async def get_response_async(self, prompt: str) -> str:
        """Get a response from the LLM asynchronously."""
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        data = {
            "model": self.model,
            "messages": [{"role": "system", "content": prompt}],
            "temperature": 0.7
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(self.api_url, headers=headers, json=data) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"LLM API error: {error_text}")
                
                result = await response.json()
                return result["choices"][0]["message"]["content"]
    
    def get_response(self, prompt: str) -> str:
        """Synchronous version of get_response_async for non-async contexts."""
        import requests
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        data = {
            "model": self.model,
            "messages": [{"role": "system", "content": prompt}],
            "temperature": 0.7
        }
        
        response = requests.post(self.api_url, headers=headers, json=data)
        
        if response.status_code != 200:
            raise Exception(f"LLM API error: {response.text}")
            
        result = response.json()
        return result["choices"][0]["message"]["content"]
