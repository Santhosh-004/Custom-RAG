import requests
import os
from enum import Enum
from enums import PromptType
import prompts

class OllamaClient:
    def __init__(self, host=None):
        self.host = host or os.getenv('OLLAMA_HOST', 'http://localhost:11434')

    def generate(self, prompt: str, stream=False, thinkingModel=False, model='qwen3:4b') -> str:
        url = f"{self.host}/api/generate"
        if thinkingModel:
            full_prompt = prompt
        else:
            full_prompt = "think /no_think " + prompt
        payload = {"model": model, "prompt": full_prompt, "stream": stream, }
        res = requests.post(url, json=payload)
        res.raise_for_status()
        response = res.json().get('response')

        return (response.split('</think>')[1]).lstrip()
    
    def infoOrQuestion(self, prompt: str) -> PromptType:
        response = self.generate(prompts.infoQuestionMessage(prompt))
        print(f"Response info/question: {response}")
        if response == 'question':
            return PromptType.QUESTION
        elif response == 'information':
            return PromptType.INFO
        return PromptType.CHATTER
