from typing import List
from utils import llm_call


def prompt_chain_workflow(initial_input: str, prompt_chain: List[str]) -> List[str]:
    """
    Execute a simple prompt chain: each step receives the previous response
    as the new user input.
    """
    response_chain = []
    response = initial_input

    for i, prompt in enumerate(prompt_chain, 1):
        print(f"\n==== Step {i} ====\n")
        final_prompt = f"{prompt}\nUser input:\n{response}"
        print(f"🔹 Prompt:\n{final_prompt}\n")

        response = llm_call(final_prompt)
        response_chain.append(response)
        print(f"✅ Response:\n{response}\n")

    return response_chain


def prompt_chain_workflow_2(initial_input: str, prompt_chain: List[str]) -> List[str]:
    """
    Execute a prompt chain, passing the **entire** accumulated context plus
    the original user input into each step.
    """
    response_chain = []
    response = initial_input

    for i, prompt in enumerate(prompt_chain, 1):
        print(f"\n==== Step {i} ====\n")
        final_prompt = (
            f"{prompt}\n\n🔹 Context:\n{response}\n🔹 Original user input: {initial_input}"
        )
        print(f"🔹 Prompt:\n{final_prompt}\n")

        response = llm_call(final_prompt)
        response_chain.append(response)
        print(f"✅ Response:\n{response}\n")

    return response_chain


initial_input = """
I'm planning a summer vacation. I like warm weather and enjoy visiting natural
scenery and historical sites. Which destinations would suit me?
"""

# Prompt chain: guide the LLM through trip‑planning steps
prompt_chain = [
    (
        "Based on the user's travel preferences, recommend three suitable "
        "destinations.\n"
        "- First, summarize the user's stated wishes.\n"
        "- Explain why each destination matches those wishes.\n"
        "- Describe each destination's climate, major attractions, and activities."
    ),

    (
        "Choose **one** of the three destinations above and state which one you "
        "picked and why.\n"
        "- List five key activities available there.\n"
        "- Include a variety such as nature exploration, historical tours, and "
        "food experiences."
    ),

    (
        "The user wants to spend a single day at this destination.\n"
        "- Create a schedule divided into morning, afternoon, and evening.\n"
        "- For each time block, suggest suitable activities and provide brief details."
    ),
]

responses = prompt_chain_workflow_2(initial_input, prompt_chain)

final_answer = responses[-1]
print(final_answer)
