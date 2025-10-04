import os
from dotenv import load_dotenv
import openai
import time

# Load .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Import exceptions correctly
from openai import OpenAIError, RateLimitError

def summarize_change(prev_text: str, new_text: str) -> str:
    """Summarize the difference between previous and new text using OpenAI."""
    
    if prev_text == new_text:
        return ""

    prompt = f"Summarize the difference between:\nPrevious:\n{prev_text}\n\nNew:\n{new_text}\n"

    # Retry logic for rate limiting
    for attempt in range(5):
        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that summarizes text changes."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_tokens=80
            )
            return response.choices[0].message.content.strip()
        except RateLimitError:
            wait_time = 2 ** attempt
            print(f"Rate limit hit. Retrying in {wait_time}s...")
            time.sleep(wait_time)
        except OpenAIError as e:
            print("OpenAI API error:", e)
            return "Error: Unable to summarize changes."
    
    return "Alert:Version 2 Newly launched"
