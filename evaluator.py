from utils import llm_call

def loop_workflow(user_query: str, evaluator_prompt: str, max_retries: int = 5) -> str:
    """
    Re‑run the summarisation + evaluation loop until the evaluator says PASS
    or until max_retries attempts have been made. Returns the last summary.
    """
    retries = 0
    while retries < max_retries:
        print(f"\n========== 📝 SUMMARY PROMPT (attempt {retries + 1}/{max_retries}) ==========\n")
        print(user_query)

        summary = llm_call(user_query, model="gpt-4o-mini")
        print(f"\n========== 📝 SUMMARY RESULT (attempt {retries + 1}/{max_retries}) ==========\n")
        print(summary)

        final_evaluator_prompt = evaluator_prompt + summary
        evaluation_result = llm_call(final_evaluator_prompt, model="gpt-4o").strip()

        print(f"\n========== 🔍 EVALUATION PROMPT (attempt {retries + 1}/{max_retries}) ==========\n")
        print(final_evaluator_prompt)

        print(f"\n========== 🔍 EVALUATION RESULT (attempt {retries + 1}/{max_retries}) ==========\n")
        print(evaluation_result)

        if "Evaluation Result = PASS" in evaluation_result:
            print("\n✅ Passed! Final summary approved.\n")
            return summary

        retries += 1
        print(f"\n🔄 Retry required… ({retries}/{max_retries})\n")

        if retries >= max_retries:
            print("❌ Reached maximum retries. Returning the last summary.")
            return summary

        # Append history for the next attempt
        user_query += f"\nAttempt {retries} summary:\n{summary}\n"
        user_query += f"Attempt {retries} feedback:\n{evaluation_result}\n\n"


def main() -> None:
    # Article link: https://zdnet.co.kr/view/?no=20250213091248
    input_article = """
OpenAI will release a new model called “GPT‑4.5” within the next few weeks,
consolidating its previously fragmented generative‑AI lineup. The company
plans to retire the inference‑focused “o” series and fold everything back
into the non‑inference “GPT” line.

According to industry sources on February 13, OpenAI CEO Sam Altman stated
on X (formerly Twitter) the previous day that GPT‑4.5 would launch soon.
Internally codenamed “Orion,” it will be the last non‑inference model,
succeeding the current generation “GPT‑4o.”

At present, OpenAI customers—including ChatGPT users—choose between models
such as “GPT‑4o,” “o1,” “o3‑mini,” and “GPT‑4.” The newest release is
“GPT‑4o,” an enhanced version of GPT‑4; GPT‑4 debuted in late 2023, while
GPT‑4o arrived in early 2024.

OpenAI had planned to unveil GPT‑5 last year, but the launch was postponed
after internal tests showed lower‑than‑expected performance. In the interim,
the company promoted the “o”‑series inference models, which boost
performance by allowing longer compute times.

Altman added, “Starting with GPT‑5 we’ll merge the inference ‘o’ series with
the ‘GPT’ series. We know our model lineup has become complicated, and we
want things to ‘just work’ rather than make users pick between models.”
    """

    user_query = f"""
Your task is to summarise the following news article.
If earlier attempts and feedback exist, incorporate that feedback and
produce an improved summary.

Article:
{input_article}
    """

    evaluator_prompt = """
Evaluate the following summary.

## Criteria
1. **Coverage of key content**
   - Must retain main ideas and logical flow of the original.
   - Omitting >15 % of critical information = FAIL.

2. **Accuracy**
   - No distortion of meaning; names, numbers, and dates must be correct.
   - Major misinterpretations or factual errors = FAIL.

3. **Conciseness & readability**
   - Avoid long, repetitive sentences.
   - Natural, clear wording is fine; extremely awkward prose = FAIL.

4. **Grammar & mechanics**
   - >5 spelling/spacing errors = FAIL.
   - Errors that change meaning = FAIL.

## Evaluation‑result format
- If all criteria are met, output exactly **“Evaluation Result = PASS”**.
- Otherwise list specific issues and suggestions, and output
  **“Evaluation Result = FAIL”** at the end.

Summary to evaluate:
    """

    final_summary = loop_workflow(user_query, evaluator_prompt, max_retries=5)
    print("\n✅ FINAL SUMMARY:\n", final_summary)


if __name__ == "__main__":
    main()
