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

    def generate(self, text: str,
                 do_sample: bool = True, max_length: int = 100, repetition_penalty: float = 5.0,
                 top_k: int = 5, top_p: float = 0.95, temperature: float = 0.8,
                 num_beams: int = 10, no_repeat_ngram_size: int = 3) -> str:
        """
        Генерация продолжения входящего текста

        Args:
            text (str): Входной текст для генерации.
            do_sample (bool, optional): Флаг для использования сэмплинга. По умолчанию True.
            max_length (int, optional): Максимальная длина генерируемого текста. По умолчанию 60.
            repetition_penalty (float, optional): Штраф за повторение. По умолчанию 5.0.
            top_k (int, optional): Количество топ-k токенов для сэмплинга. По умолчанию 5.
            top_p (float, optional): Параметр для сэмплинга с учетом вероятности. По умолчанию 0.95.
            temperature (float, optional): Температура для сэмплинга. По умолчанию 0.8.
            num_beams (int, optional): Количество лучей для поиска. По умолчанию 10.
            no_repeat_ngram_size (int, optional): Размер n-граммы для предотвращения повторений. По умолчанию 3.

        Returns:
            str: Сгенерированный текст.
        """
        input_ids = self.tokenizer.encode(text, return_tensors="pt")

        out = self.model.generate(
            input_ids,
            max_length=max_length,
            repetition_penalty=repetition_penalty,
            do_sample=do_sample,
            top_k=top_k, top_p=top_p, temperature=temperature,
            num_beams=num_beams, no_repeat_ngram_size=no_repeat_ngram_size
        )

        return list(map(self.tokenizer.decode, out))[0]