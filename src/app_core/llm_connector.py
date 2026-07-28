import os
from dotenv import load_dotenv

class LLMConnector:
    def __init__(self, provider: str = "Gemini", api_key: str = None):
        """
        Initialize LLM Client based on selected provider.
        Supports: Gemini, OpenAI, Groq
        """
        load_dotenv()
        self.provider = provider.strip().lower()
        
        # Determine the API key (passed to constructor, or read from env)
        if api_key:
            self.api_key = api_key
        else:
            if self.provider == "gemini":
                self.api_key = os.environ.get("GEMINI_API_KEY")
            elif self.provider == "openai":
                self.api_key = os.environ.get("OPENAI_API_KEY")
            elif self.provider == "groq":
                self.api_key = os.environ.get("GROQ_API_KEY") or os.environ.get("OPENAI_API_KEY")
            else:
                self.api_key = None

        self.client = None
        self._initialize_client()

    def _initialize_client(self):
        if not self.api_key:
            # We don't fail immediately, we let the UI handle prompt/validation
            return

        if self.provider == "gemini":
            try:
                # Attempt to use google-genai
                from google import genai
                self.client = genai.Client(api_key=self.api_key)
                self.has_new_genai = True
            except ImportError:
                # Fallback to legacy google-generativeai
                import google.generativeai as genai
                genai.configure(api_key=self.api_key)
                self.client = genai
                self.has_new_genai = False
        
        elif self.provider == "openai":
            from openai import OpenAI
            self.client = OpenAI(api_key=self.api_key)
            
        elif self.provider == "groq":
            from openai import OpenAI
            # Groq is fully compatible with OpenAI client
            self.client = OpenAI(
                api_key=self.api_key,
                base_url="https://api.groq.com/openai/v1"
            )

    def is_configured(self) -> bool:
        return self.api_key is not None and self.api_key != ""

    def generate_response(self, prompt: str, chat_history: list[dict], memories: list[str], temperature: float = 0.7) -> str:
        """
        Generate chat response with memory context injected.
        """
        if not self.is_configured():
            return f"Error: API Key for {self.provider.capitalize()} is not configured. Please supply it in the sidebar or .env file."
        
        if self.client is None:
            self._initialize_client()
            if self.client is None:
                return f"Error: Failed to initialize {self.provider.capitalize()} API client."

        # 1. Format memory context
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

        # 2. Call the provider model
        try:
            if self.provider == "gemini":
                # Default model name
                model_name = "gemini-1.5-flash" # Safe legacy/current naming that always exists
                if self.has_new_genai:
                    # google-genai client
                    from google.genai import types
                    # Build contents including system instruction and history
                    contents = []
                    # Add system instruction as prefix or configuration if supported, or inline
                    # Let's use config with system_instruction
                    config = types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        temperature=temperature
                    )
                    
                    # Convert chat history to list of google content parts
                    for msg in chat_history:
                        role = "user" if msg["role"] == "user" else "model"
                        contents.append(f"{role}: {msg['content']}")
                    
                    # Append active prompt
                    contents.append(prompt)
                    
                    response = self.client.models.generate_content(
                        model=model_name,
                        contents=contents,
                        config=config
                    )
                    return response.text
                else:
                    # google-generativeai legacy wrapper
                    # Combine system instruction and prompt/history
                    chat = self.client.GenerativeModel(
                        model_name=model_name,
                        system_instruction=system_instruction
                    ).start_chat()
                    
                    # Push history
                    for msg in chat_history[:-1]:
                        if msg["role"] == "user":
                            chat.send_message(msg["content"])
                    
                    # Send prompt
                    response = chat.send_message(prompt)
                    return response.text

            elif self.provider in ["openai", "groq"]:
                # Default models
                model_name = "gpt-4o-mini" if self.provider == "openai" else "llama-3.3-70b-versatile"
                
                # Build messages payload
                messages = [{"role": "system", "content": system_instruction}]
                
                # History messages
                for msg in chat_history:
                    messages.append({"role": msg["role"], "content": msg["content"]})
                
                # Active user input
                messages.append({"role": "user", "content": prompt})
                
                response = self.client.chat.completions.create(
                    model=model_name,
                    messages=messages,
                    temperature=temperature
                )
                return response.choices[0].message.content
        except Exception as e:
            return f"Error during generation with {self.provider.capitalize()}: {str(e)}"

    def generate_response_stream(self, prompt: str, chat_history: list[dict], memories: list[str], temperature: float = 0.7):
        """
        Generate chat response stream with memory context injected.
        Yields text chunks as they arrive.
        """
        if not self.is_configured():
            yield f"Error: API Key for {self.provider.capitalize()} is not configured. Please supply it in the sidebar or .env file."
            return
        
        if self.client is None:
            self._initialize_client()
            if self.client is None:
                yield f"Error: Failed to initialize {self.provider.capitalize()} API client."
                return

        # 1. Format memory context
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

        # 2. Call the provider model in streaming mode
        try:
            if self.provider == "gemini":
                model_name = "gemini-1.5-flash"
                if self.has_new_genai:
                    from google.genai import types
                    contents = []
                    config = types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        temperature=temperature
                    )
                    for msg in chat_history:
                        role = "user" if msg["role"] == "user" else "model"
                        contents.append(f"{role}: {msg['content']}")
                    contents.append(prompt)
                    
                    response_stream = self.client.models.generate_content_stream(
                        model=model_name,
                        contents=contents,
                        config=config
                    )
                    for chunk in response_stream:
                        if chunk.text:
                            yield chunk.text
                else:
                    chat = self.client.GenerativeModel(
                        model_name=model_name,
                        system_instruction=system_instruction
                    ).start_chat()
                    for msg in chat_history[:-1]:
                        if msg["role"] == "user":
                            chat.send_message(msg["content"])
                    response_stream = chat.send_message(prompt, stream=True)
                    for chunk in response_stream:
                        if chunk.text:
                            yield chunk.text

            elif self.provider in ["openai", "groq"]:
                model_name = "gpt-4o-mini" if self.provider == "openai" else "llama-3.3-70b-versatile"
                messages = [{"role": "system", "content": system_instruction}]
                for msg in chat_history:
                    messages.append({"role": msg["role"], "content": msg["content"]})
                messages.append({"role": "user", "content": prompt})
                
                response_stream = self.client.chat.completions.create(
                    model=model_name,
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
            yield f"Error during streaming with {self.provider.capitalize()}: {str(e)}"

