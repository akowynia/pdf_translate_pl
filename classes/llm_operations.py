from llama_cpp import Llama
import logging

class llm_operations:
    def __init__(self) -> None:
        model_path = "models/Meta-Llama-3-8B-Instruct-Q4_K_M.gguf"
        self.llm = Llama(model_path=model_path,n_gpu_layers=-1 ,verbose=False)


    def generate(self, message, system_message):
        prompt_1 = f"""
        <|begin_of_text|><|start_header_id|>system<|end_header_id|>

        {system_message}<|eot_id|><|start_header_id|>user<|end_header_id|>

        {message}<|eot_id|><|start_header_id|>assistant<|end_header_id|>
        """
        output = self.llm(
            prompt_1,
            max_tokens=200,
            temperature=0.8,
            top_p=0.95
        )

        response_text = output['choices'][0]['text']
        return response_text