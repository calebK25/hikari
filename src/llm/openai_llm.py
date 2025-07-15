from openai import OpenAI
client = OpenAI()

def chat(messages, model="gpt-4o-mini"):
    return client.chat.completions.create(model=model, messages=messages)