import json

from config import client, MODEL
from tools import get_course_fee, calculate, TOOLS


SYSTEM_PROMPT = """
You are a helpful college assistant.

Rules:
- Never guess course fees.
- Always use get_course_fee for course fees.
- Use calculate for arithmetic.
- Available courses: CS101, AI202, DS303.
- If no tool is needed, answer directly.
"""


def agent(question, max_steps=8):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": question}
    ]

    for step in range(max_steps):
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
            temperature=0
        )

        message = response.choices[0].message

        print(f"\nStep {step + 1}")

        if not message.tool_calls:
            print("Final answer:", message.content)
            return message.content

        messages.append(message)

        for tool_call in message.tool_calls:
            tool_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)

            print("Tool:", tool_name)
            print("Arguments:", arguments)

            if tool_name == "get_course_fee":
                result = get_course_fee(arguments["course_code"])

            elif tool_name == "calculate":
                result = calculate(arguments["expression"])

            else:
                result = "Unknown tool"

            print("Result:", result)

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(result)
            })

    return "Agent stopped after maximum steps."