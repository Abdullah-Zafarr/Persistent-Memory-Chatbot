# ═══ IMPORTS ═══
import os
from dotenv import load_dotenv

# ═══ LLM CONNECTOR CLASS — Connects to Groq and generates AI responses ═══
class LLMConnector:

    # ── CONSTRUCTOR: Reads GROQ_API_KEY from .env and sets up the provider ──
    def __init__(self, provider: str = "Groq", api_key: str = None):
        load_dotenv()
        self.provider = "groq"
        self.api_key = api_key or os.environ.get("GROQ_API_KEY")
        self.client = None
        self._initialize_client()

    # ── CLIENT SETUP: Initializes the Groq client using OpenAI-compatible SDK ──
    def _initialize_client(self):
        if not self.api_key:
            return
        from openai import OpenAI
        # Groq is fully OpenAI-compatible — just swap the base_url
        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://api.groq.com/openai/v1"
        )

    # ── HEALTH CHECK: Returns True only if an API key is present ──
    def is_configured(self) -> bool:
        return self.api_key is not None and self.api_key != ""

    # ═══ STANDARD RESPONSE: Returns full reply as a string (non-streaming) ═══
    def generate_response(self, prompt: str, chat_history: list[dict], memories: list[str], temperature: float = 0.7) -> str:
        if not self.is_configured():
            return "Error: GROQ_API_KEY is not configured. Please add it to your .env file."

        if self.client is None:
            self._initialize_client()
            if self.client is None:
                return "Error: Failed to initialize Groq client."

        # ── Build system instruction — inject memories if available ──
        if memories:
            memory_context = "\n".join([f"- {m}" for m in memories])
            system_instruction = (
                "You are a helpful, conversational, and personalized AI chatbot.\n"
                "You have access to the following persistent memories/facts about this user:\n"
                f"{memory_context}\n\n"
                "Please use this memory context to deliver personalized and relevant answers where appropriate, "
                "without directly stating 'According to my memories...' unless asked. Keep your tone natural."
            )
        else:
            system_instruction = (
                "You are a helpful, conversational, and personalized AI chatbot.\n"
                "Try to remember relevant user details in the conversation where appropriate."
            )

        # ── Build messages list and call Groq ──
        try:
            messages = [{"role": "system", "content": system_instruction}]
            for msg in chat_history:
                messages.append({"role": msg["role"], "content": msg["content"]})
            messages.append({"role": "user", "content": prompt})

            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                temperature=temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error during generation: {str(e)}"

    # ═══ STREAMING RESPONSE: Yields text chunks in real-time (for typing effect in UI) ═══
    def generate_response_stream(self, prompt: str, chat_history: list[dict], memories: list[str], temperature: float = 0.7):
        if not self.is_configured():
            yield "Error: GROQ_API_KEY is not configured. Please add it to your .env file."
            return

        if self.client is None:
            self._initialize_client()
            if self.client is None:
                yield "Error: Failed to initialize Groq client."
                return

        # ── Build system instruction — inject memories if available ──
        if memories:
            memory_context = "\n".join([f"- {m}" for m in memories])
            system_instruction = (
                "You are a helpful, conversational, and personalized AI chatbot.\n"
                "You have access to the following persistent memories/facts about this user:\n"
                f"{memory_context}\n\n"
                "Please use this memory context to deliver personalized and relevant answers where appropriate, "
                "without directly stating 'According to my memories...' unless asked. Keep your tone natural."
            )
        else:
            system_instruction = (
                "You are a helpful, conversational, and personalized AI chatbot.\n"
                "Try to remember relevant user details in the conversation where appropriate."
            )

        # ── Stream response chunks from Groq one by one ──
        try:
            messages = [{"role": "system", "content": system_instruction}]
            for msg in chat_history:
                messages.append({"role": msg["role"], "content": msg["content"]})
            messages.append({"role": "user", "content": prompt})

            response_stream = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                temperature=temperature,
                stream=True
            )
            for chunk in response_stream:
                if chunk.choices and len(chunk.choices) > 0:
                    delta = chunk.choices[0].delta
                    if hasattr(delta, "content") and delta.content:
                        yield delta.content

        except Exception as e:
            yield f"Error during streaming: {str(e)}"
