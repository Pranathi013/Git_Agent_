import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
)

def get_suggestions(problems):
    if not problems:
        return "✅ No problems found! Your project looks clean."

    problems_text = "\n".join([
        f"- [{p['severity'].upper()}] {p['message']}"
        + (f" in file: {p['file']}" if p['file'] else "")
        for p in problems
    ])

    prompt = f"""
You are a friendly coding assistant helping a beginner push their project to GitHub.

These problems were found in their project:
{problems_text}

For EACH problem:
1. Explain what it means in simple terms (like talking to a 10-year-old)
2. Give a suggestion to fix it
3. Show PROS of fixing it
4. Show CONS of NOT fixing it

Keep your tone friendly, simple, and encouraging.
Use emojis to make it easier to read.
"""

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful coding assistant. Always format your responses in clear markdown.",
                },
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama-3.3-70b-versatile",
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"⚠️ An error occurred with the Groq AI: {str(e)}"