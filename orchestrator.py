import asyncio
import json
from utils import llm_call, llm_call_async


async def run_llm_parallel(prompt_list):
    """Run a list of LLM calls concurrently and return the responses in completion order."""
    tasks = [llm_call_async(prompt) for prompt in prompt_list]
    responses = []

    for task in asyncio.as_completed(tasks):
        result = await task
        responses.append(result)
    return responses


def get_orchestrator_prompt(user_query: str) -> str:
    return f"""
Analyse the user’s question below and break it down into **up to three** related sub‑questions.

Respond **exactly** in the following JSON format:

{{
    "analysis": "Explain your understanding of the user’s question and the rationale for each sub‑question you created.",
    "subtasks": [
        {{
            "description": "Describe the focus and intent of this sub‑question.",
            "sub_question": "Question 1"
        }},
        {{
            "description": "Describe the focus and intent of this sub‑question.",
            "sub_question": "Question 2"
        }}
        // Include a third sub‑question object if needed
    ]
}}

User question: {user_query}
"""


def get_worker_prompt(user_query: str, sub_question: str, description: str) -> str:
    return f"""
You are responsible for answering a **sub‑question** derived from the user’s original query.

Original question: {user_query}
Sub‑question:     {sub_question}

Guidance: {description}

Please provide a comprehensive and detailed response that thoroughly addresses the sub‑question.
"""


async def orchestrate_task(user_query: str) -> str:
    """
    Run the orchestrator to decompose the original question, call workers in parallel,
    and then aggregate their answers into one final response.
    """

    orchestrator_prompt = get_orchestrator_prompt(user_query)
    print("\n============================ ORCHESTRATOR PROMPT ============================\n")
    print(orchestrator_prompt)

    orchestrator_response = llm_call(orchestrator_prompt, model="gpt-4o")

    print("\n============================ ORCHESTRATOR RESPONSE ===========================\n")
    print(orchestrator_response)

    response_json = json.loads(
        orchestrator_response.replace("```json", "").replace("```", "")
    )
    analysis = response_json.get("analysis", "")
    sub_tasks = response_json.get("subtasks", [])

    worker_prompts = [
        get_worker_prompt(user_query, task["sub_question"], task["description"])
        for task in sub_tasks
    ]
    print("\n============================ WORKER PROMPTS ============================\n")
    for prompt in worker_prompts:
        print(prompt)

    worker_responses = await run_llm_parallel(worker_prompts)

    print("\n============================ WORKER RESPONSES ============================\n")
    for response in worker_responses:
        print(response)

    aggregator_prompt = f"""Below are answers to sub‑questions derived from the user’s original query.
Please craft a **final answer** that incorporates these responses as comprehensively and clearly as possible.

User’s original question:
{user_query}

Sub‑questions and answers:
"""
    for i, task in enumerate(sub_tasks, start=1):
        aggregator_prompt += f"\n{i}. Sub‑question: {task['sub_question']}\n"
        aggregator_prompt += f"   Answer: {worker_responses[i-1]}\n"

    print("\n============================ AGGREGATOR PROMPT ============================\n")
    print(aggregator_prompt)

    final_response = llm_call(aggregator_prompt, model="gpt-4o")
    return final_response



async def main():
    user_query = "How will AI affect future jobs?"

    print("\n============================ CASE 1: DIRECT QUESTION ============================\n")
    print(llm_call(user_query, model="gpt-4o"))

    print("\n============================ CASE 2: ORCHESTRATOR PATTERN ============================\n")
    final_output = await orchestrate_task(user_query)

    # Final aggregated answer
    print("\n============================ FINAL ANSWER ============================\n")
    print(final_output)


if __name__ == "__main__":
    asyncio.run(main())
