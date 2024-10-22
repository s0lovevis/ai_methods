import json
from transformers import GPT2Tokenizer, GPT2LMHeadModel
from typing import List, Optional

class ruGPTModel:
    def __init__(self, model_name_or_path: str):
        """
        Инициализация модели ruGPT.

        Args:
            model_name_or_path (str): Путь или имя модели для загрузки.
        """
        self.tokenizer = GPT2Tokenizer.from_pretrained(model_name_or_path)
        self.model = GPT2LMHeadModel.from_pretrained(model_name_or_path)
        self.config = self.load_config()

    def load_config(self) -> dict:
        """
        Загрузка конфигурации из файла model_config.json.

        Returns:
            dict: Словарь с параметрами конфигурации.
        """
        with open('.\\model_config.json', 'r') as file:
            config = json.load(file)
        return config

    def generate(self, text: str) -> str:
        """
        Генерация текста на основе входного текста.

        Args:
            text (str): Входной текст для генерации.

        Returns:
            str: Сгенерированный текст.
        """
        input_ids = self.tokenizer.encode(text, return_tensors="pt")

        out = self.model.generate(
            input_ids,
            max_length=self.config["max_length"],
            repetition_penalty=self.config["repetition_penalty"],
            do_sample=self.config["do_sample"],
            top_k=self.config["top_k"],
            top_p=self.config["top_p"],
            temperature=self.config["temperature"],
            num_beams=self.config["num_beams"],
            no_repeat_ngram_size=self.config["no_repeat_ngram_size"]
        )

        return list(map(self.tokenizer.decode, out))[0]
