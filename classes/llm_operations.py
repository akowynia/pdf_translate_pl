import ollama
import json


class llm_operations:
    def __init__(self, model_name: str = "llama3") -> None:
        """
        Initializes the llm_operations class.

        This class is responsible for generating responses using an Ollama model.

        Args:
            model_name (str): The name of the model in Ollama (e.g. 'llama3', 'mistral').

        Returns:
            None
        """
        self.model_name = model_name

    def generate(self, message: str, system_message: str) -> str:
        """
        Generates a response using the Ollama model.

        Args:
            message (str): The user's message.
            system_message (str): The system's message.

        Returns:
            str: The generated response.
        """
        response = ollama.chat(
            model=self.model_name,
            messages=[
                {
                    'role': 'system',
                    'content': system_message,
                },
                {
                    'role': 'user',
                    'content': message,
                },
            ],
            options={
                'temperature': 0.8,
                'top_p': 0.95,
            }
        )
        return response['message']['content']

    def generate_batch(self, payload_dict: dict, system_message: str) -> dict:
        """
        Translates a dictionary of text blocks in a single JSON call to Ollama.

        Args:
            payload_dict (dict): Dictionary mapping string IDs to text snippets.
            system_message (str): System prompt.

        Returns:
            dict: Dictionary mapping the same string IDs to translated text snippets.
        """
        if not payload_dict:
            return {}

        user_prompt = (
            "Dostajesz słownik JSON z fragmentami tekstu do przetłumaczenia z angielskiego na język polski.\n"
            "Przetłumacz wartość każdego klucza na język polski. Zachowaj numery, punkty oraz układ.\n"
            "Tylko przetłumacz teksty. Zwróć wynik jako prawidłowy obiekt JSON o takich samych kluczach.\n\n"
            f"Wejście JSON:\n{json.dumps(payload_dict, ensure_ascii=False)}"
        )

        try:
            response = ollama.chat(
                model=self.model_name,
                messages=[
                    {
                        'role': 'system',
                        'content': system_message,
                    },
                    {
                        'role': 'user',
                        'content': user_prompt,
                    },
                ],
                format='json',
                options={
                    'temperature': 0.2,
                }
            )
            content = response['message']['content']
            parsed = json.loads(content)
            if isinstance(parsed, dict):
                return parsed
        except Exception as e:
            print(f"Batch LLM translation error ({e}), falling back to single item calls...")

        result = {}
        for key, text in payload_dict.items():
            if text and text.strip():
                result[key] = self.generate(text, system_message)
            else:
                result[key] = ""
        return result


