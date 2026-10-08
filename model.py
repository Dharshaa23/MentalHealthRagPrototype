
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found.")

client = genai.Client(api_key=api_key)

# Primary and fallback models
PRIMARY_MODEL = "gemini-3.5-flash-lite"
FALLBACK_MODEL = "gemini-3.7-flash"


def generate_answer(prompt):
    try:
        response = client.models.generate_content(
            model=PRIMARY_MODEL,
            contents=prompt
        )

        return response.text

    except Exception as primary_error:
        print(
            f"Primary model unavailable. "
            f"Trying fallback model: {FALLBACK_MODEL}"
        )

        try:
            response = client.models.generate_content(
                model=FALLBACK_MODEL,
                contents=prompt
            )

            return response.text

        except Exception as fallback_error:
            raise RuntimeError(
                "Both Gemini models failed.\n"
                f"Primary error: {primary_error}\n"
                f"Fallback error: {fallback_error}"
            )
