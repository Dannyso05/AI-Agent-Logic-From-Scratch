import asyncio
from utils import llm_call_async


async def run_llm_parallel(prompt_details):
    """Launch multiple LLM calls concurrently and collect their responses."""
    tasks = [
        llm_call_async(prompt["user_prompt"], prompt["model"])
        for prompt in prompt_details
    ]
    responses = []

    # Gather results as soon as each model finishes
    for task in asyncio.as_completed(tasks):
        result = await task
        print("LLM response completed:", result)
        responses.append(result)

    return responses


async def main():
    # User question for all models
    question = (
        'Translate the sentence below into natural Korean:\n'
        '"Do what you can, with what you have, where you are." — Theodore Roosevelt'
    )

    # Run the same prompt on three different models
    parallel_prompt_details = [
        {"user_prompt": question, "model": "gpt-4o"},
        {"user_prompt": question, "model": "gpt-4o-mini"},
        {"user_prompt": question, "model": "o1-mini"},
    ]

    # Collect individual model outputs
    responses = await run_llm_parallel(parallel_prompt_details)

    aggregator_prompt = (
        "Below are responses from several AI models to the same user question.\n"
        "Your task is to synthesize these responses into a single, high‑quality answer.\n"
        "Some answers may be inaccurate or biased, so produce a reliable and accurate final response.\n\n"
        "User question:\n"
        f"{question}\n\n"
        "Model responses:"
    )

    for i, resp in enumerate(responses, start=1):
        aggregator_prompt += f"\n{i}. Model response: {resp}\n"

    print("---------------------------Aggregation Prompt:-----------------------\n", aggregator_prompt)

    final_response = await llm_call_async(aggregator_prompt, model="gpt-4o")
    print("---------------------------Final Aggregated Response:-----------------------\n", final_response)


asyncio.run(main())
