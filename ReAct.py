from dotenv import load_dotenv
import os
import openai
import re
from typing import List
from langchain_google_community import GoogleSearchAPIWrapper

load_dotenv()

openai.api_key = os.environ.get("OPENAI_API_KEY")

def chat_completion(messages: list[dict[str, str]], model: str = "gpt-4o", temperature: float = 0) -> str:
    response = openai.responses.create(
        model=model,
        input=messages,
        temperature=temperature,
    )
    return response.output_text

class Agent:
    def __init__(self, system: str = "") -> None:
        self.system = system
        self.messages: list[dict[str, str]] = []
        if self.system:
            self.messages.append({"role": "system", "content": system})

    def __call__(self, message: str = "") -> str:
        if message:
            self.messages.append({"role": "user", "content": message})
        result = self.execute()
        self.messages.append({"role": "assistant", "content": result})
        return result

    def execute(self) -> str:
        return chat_completion(messages=self.messages)

# System prompt for the agent
system_prompt = """
You run in a loop of Thought, Action, PAUSE, Observation.
At the end of the loop, you output an Answer.
Use Thought to describe your thoughts about the question you have been asked.
Use Action to run one of the actions available to you - then return PAUSE.
PAUSE ALWAYS COMES AFTER ACTION.
ALWYAS PUT A NEW LINE AFTER Thought, Action, PAUSE, Observation.
TERMINATE THE GENERATION AFTER THE PAUSE.
Observation will be the result of running those actions.

Your available actions are:

search_web:
e.g. search_web: "latest news about AI"
Searches the web and returns a summary of the top results.

Example session:

Question: What are the latest advancements in AI?
Thought: I need to search the web for the latest news about AI.
Action: search_web: "latest advancements in AI"
PAUSE
CLOSE THE CURRENT LOOP SESSION

You will be called again with this:

Observation: "Recent advancements include GPT-4, advancements in robotics, and breakthroughs in reinforcement learning."

Thought: I need more information about these advancements.
Action: search_web: "GPT-4, robotics, reinforcement learning"
PAUSE

CLOSE THE CURRENT LOOP SESSION
You will be called again with this:

Observation: "GPT-4, robotics, reinforcement learning are the latest advancements in AI."

If you have the answer, output it as the Answer.

Answer: The latest advancements in AI include GPT-4, robotics, and reinforcement learning.

Make sure to only output one Answer at the end of the loop.

ONLY USE YOUR OWN KNOWLEDGE BASE IF GOOGLE CONSTANTLY FAILS TO FIND THE ANSWER MORE THAN 2 TIMES.
Now it's your turn:
""".strip()

def search_web(query: str, num_results: int = 3) -> str:
    search = GoogleSearchAPIWrapper()
    results = search.results(query, num_results)
    return results

def loop(max_iterations: int = 10, query: str = "") -> None:
    agent = Agent(system=system_prompt)
    tools = ["search_web"]
    next_prompt = query

    for _ in range(max_iterations):
        result = agent(next_prompt)
        print(result)
        if "Answer" in result:
            break

        if "PAUSE" in result and "Action" in result:
            action_match = re.search(r"Action: ([a-z_]+): (.+)", result, re.IGNORECASE)
            if not action_match:
                next_prompt = "\nObservation: Unable to parse action."
                continue

            chosen_tool, arg = action_match.groups()
            if chosen_tool in tools:
                tool_output = eval(f"{chosen_tool}('{arg}')")
                next_prompt = f"\nObservation: {tool_output}"
            else:
                next_prompt = "\nObservation: Tool not found"
            print(next_prompt)
            continue

# Example run -----------------------------------------------------------------
if __name__ == "__main__":
    loop(query="What are the latest advancements in AI?")
