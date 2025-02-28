import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from .env file
load_dotenv()

class GroqClient:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")  # Fetch API key from environment
        if not api_key:
            raise ValueError("GROQ_API_KEY is not set in the environment")
        self.client = Groq(api_key=api_key)

    def get_tutoring_response(self, prompt, student_history=None):
        if student_history:
            prompt = f"Student history: {student_history}\nQuery: {prompt}"
        response = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-70b-8192"
        )
        return response.choices[0].message.content
