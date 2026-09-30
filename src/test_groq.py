from groq import Groq

client = Groq()

response = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[
        {
            "role": "user",
            "content": "Reply with exactly: Groq connection successful"
        }
    ]
)

print(response.choices[0].message.content)