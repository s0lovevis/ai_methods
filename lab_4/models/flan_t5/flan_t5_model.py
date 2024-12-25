import yaml
import os
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

class FlanT5LargeRecipeGenerator:
    def __init__(self, config_path: str = None):

        current_dir = os.path.dirname(os.path.abspath(__file__))
        if config_path is None:
            config_path = os.path.join(current_dir, "config.yaml")

        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
        
        self.model_name = config["model_name"]
        self.generation_params = config["generation_params"]

        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name)

    def generate(self, prompt: str) -> str:
        """
        Генерация одного рецепта на основе промпта.

        :param prompt: Строка-инструкция для модели (на английском).
        :return: Строка сгенерированного рецепта.
        """
        inputs = self.tokenizer(prompt, return_tensors="pt", padding=True, truncation=True)

        output = self.model.generate(
            **inputs,
            max_length=self.generation_params["max_length"],
            min_length=self.generation_params["min_length"],
            temperature=self.generation_params["temperature"],
            top_p=self.generation_params["top_p"],
            num_return_sequences=1,
            do_sample=True,
        )

        recipe = self.tokenizer.decode(output[0], skip_special_tokens=True)
        return recipe
    
a = FlanT5LargeRecipeGenerator()