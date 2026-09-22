"""Day 2: Self-consistency experiment."""

from collections import Counter

from config import client, MODEL
from cot_compare import COT_PROMPT, QUESTIONS
def banner(text):
    print("=" * 72)
    print(text)
    print("=" * 72)

RUNS = 5
TEMPERATURE = 0.8
PROMPT = (
    "Calculate carefully: (12000 + 18000 + 15000) * 0.85 / 4. "
    "Output only the numerical answer."
)
MAX_TOKENS = 300


def final_answer(text):
    """Get the text after 'Final Answer:'."""
    for line in reversed(text.splitlines()):
        if "final answer" in line.lower():
            return line.split(":", 1)[-1].strip()

    return text.splitlines()[-1].strip() if text.strip() else "(empty)"


def run_many(question, runs=RUNS, temperature=TEMPERATURE):
    answers = []

    for attempt in range(1, runs + 1):
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": PROMPT},
                {"role": "user", "content": "Calculate 45000 * 0.85 / 4. Output only the final number."},
                
            ],
            temperature=temperature,
             max_tokens=MAX_TOKENS,
        )

        answer = final_answer(response.choices[0].message.content)

        print(f"run {attempt}: {answer}")
        answers.append(answer)

    return answers


if __name__ == "__main__":
    banner("SELF-CONSISTENCY")

    question = QUESTIONS[0]

    print("QUESTION:", question, "\n")

    answers = run_many(question)

    winner, count = Counter(answers).most_common(1)[0]

    print(f"\nMajority answer ({count} of {len(answers)} runs): {winner}")