from dotenv import load_dotenv
import os
import openai
import re
from typing import List
from langchain_google_community import GoogleSearchAPIWrapper
import requests

load_dotenv()

openai.api_key = os.environ.get("OPENAI_API_KEY")

def chat_completion(messages: list[dict[str, str]], model: str = "gpt-4o-mini", temperature: float = 0) -> str:
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

calculate:
e.g. calculate: "2 + 2 * 3"
Performs mathematical calculations and returns the result.

stock_lookup:
e.g. stock_lookup: "AAPL"
Looks up the current stock price and company information for a given ticker symbol.

Example session:

Question: What is the current price of Apple stock and how much would it cost to buy 100 shares?
Thought: I need to first look up the current price of Apple stock.
Action: stock_lookup: "AAPL"
PAUSE
CLOSE THE CURRENT LOOP SESSION

You will be called again with this:

Observation: "Apple Inc. (AAPL) is currently trading at $175.50"

Thought: Now that I have the price, I need to calculate the total cost for 100 shares.
Action: calculate: "175.50 * 100"
PAUSE

CLOSE THE CURRENT LOOP SESSION
You will be called again with this:

Observation: "17550.0"

Thought: I have both pieces of information needed to answer the question.
Answer: Apple Inc. (AAPL) is currently trading at $175.50 per share, and it would cost $17,550 to buy 100 shares.

Make sure to only output one Answer at the end of the loop.

ONLY USE YOUR OWN KNOWLEDGE BASE IF GOOGLE CONSTANTLY FAILS TO FIND THE ANSWER MORE THAN 2 TIMES.
Now it's your turn:
""".strip()

def search_web(query: str, num_results: int = 3) -> str:
    try:
        search = GoogleSearchAPIWrapper(
            google_api_key=os.environ.get("GOOGLE_API_KEY"),
            google_cse_id=os.environ.get("GOOGLE_CSE_ID")
        )
        results = search.results(query, num_results)
        return str(results)
    except Exception as e:
        return f"Error: {str(e)}"

def calculate(expression: str) -> str:
    try:
        result = eval(expression.replace('"', "").replace(" ", ""))
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"

def stock_lookup(ticker: str) -> str:
    try:
        api_key = os.environ.get("ALPHA_VANTAGE_API_KEY")
        if not api_key:
            return "Error: Alpha Vantage API key not found in environment variables"
            
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker.replace('"', '').replace(" ", '')}&apikey={api_key}"
        response = requests.get(url)
        data = response.json()
        
        if "Time Series (Daily)" not in data:
            return f"Error: Could not find data for {ticker}"
            
        # Get the most recent date's data
        time_series = data["Time Series (Daily)"]
        most_recent_date = max(time_series.keys())
        most_recent_data = time_series[most_recent_date]
        
        current_price = most_recent_data["4. close"]
        return f"{ticker} is currently trading at ${current_price}"
    except Exception as e:
        return f"Error: {str(e)}"

def loop(max_iterations: int = 10, query: str = "") -> None:
    agent = Agent(system=system_prompt)
    tools = ["search_web", "calculate", "stock_lookup"]
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
    loop(query="What is the current price of Apple stock and how much would it cost to buy 100 shares?")
