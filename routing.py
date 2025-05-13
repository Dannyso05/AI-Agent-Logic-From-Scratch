from utils import llm_call


def run_router_workflow(user_prompt: str):
    """
    Decide which model is best suited for the user's prompt,
    call that model, and return the response.
    """
    router_prompt = f"""
    User prompt/question: {user_prompt}

    Each model excels at different tasks. Choose the model that best fits
    this question:

    - gpt-4o       : Best for general tasks (default)
    - o1-mini      : Good for coding and complex problem‑solving
    - gpt-4o-mini  : Suitable for simple arithmetic, lightweight tasks

    Respond with *only* the model name.
    """
    print(router_prompt)

    selected_model = llm_call(router_prompt)
    print("Selected model:", selected_model)

    response = llm_call(user_prompt, model=selected_model)
    print(response)
    return response


query1 = "What is 1 plus 2?"
print(query1)
run_router_workflow(query1)

query2 = "Plan a travel itinerary for Lisbon."
print(query2)
run_router_workflow(query2)

query3 = "Write an API web server in Python."
print(query3)
run_router_workflow(query3)
