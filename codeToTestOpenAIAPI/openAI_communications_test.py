#Luis Urena 
#with code adopted from https://platform.openai.com/docs/introduction





import os
import openai

# Load your API key from an environment variable or secret management service
openai.api_key =  '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'

response = openai.Completion.create(model="text-davinci-003", prompt="hello chatgpt can you hear meee", temperature=0, max_tokens=7)
print(response["choices"][0]["text"])
