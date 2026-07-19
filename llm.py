import os
import time
from openai import OpenAI

MODEL = "gpt-4o-mini"
CALL_DELAY_SEC = 1  # API limitleri için 1 saniye bekleme

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

def call_llm(prompt):
    start = time.time()
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
        )
    except Exception as e:
        print("LLM call failed:", e)
        return None, 0, 0

    end = time.time()
    time.sleep(CALL_DELAY_SEC)
    text = response.choices[0].message.content

    tokens = response.usage.total_tokens
    return text, tokens, end - start