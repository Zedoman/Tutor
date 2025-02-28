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

    def get_tutoring_response(self, prompt, progress_context):
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": f"You are a tutoring AI. {progress_context} Strictly follow the path restrictions in the context. Refuse to answer questions that do not match the specified path rules."
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model="llama3-8b-8192",
                temperature=0.5,
                max_tokens=1024,
                top_p=1,
                stop=None,
                stream=False,
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            return f"Error generating response: {str(e)}"
