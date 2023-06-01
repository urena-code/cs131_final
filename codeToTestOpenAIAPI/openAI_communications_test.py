#Luis Urena 
#with code adopted from https://platform.openai.com/docs/introduction





import os
import openai

# Load your API key from an environment variable or secret management service
openai.api_key = 'key_here'

response = openai.Completion.create(model="text-davinci-003", prompt="hello chatgpt can you hear meee", temperature=0, max_tokens=7)
print(response["choices"][0]["text"])
