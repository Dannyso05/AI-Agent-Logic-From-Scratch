import re
from openai import AsyncOpenAI, OpenAI
import dotenv
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

client = AsyncOpenAI(
    api_key=OPENAI_API_KEY,  
)
sync_client = OpenAI(
    api_key=OPENAI_API_KEY,
)

def llm_call(prompt: str,  model: str = "gpt-4o-mini") -> str:
    messages = []
    messages.append({"role": "user", "content": prompt})
    chat_completion = sync_client.responses.create(
        model=model,
        input=messages,
    )
    return chat_completion.output_text


async def llm_call_async(prompt: str,  model: str = "gpt-4o-mini") -> str:
    messages = []
    messages.append({"role": "user", "content": prompt})
    chat_completion = await client.responses.create(
        model=model,
        input=messages,
    )
    print(model,"cimpleted")
    
    return chat_completion.output_text


if __name__ == "__main__":
    test = llm_call("hi")
    print(test)
