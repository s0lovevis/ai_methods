from transformers import AutoModelForCausalLM, AutoTokenizer
from typing import Tuple
from translator import Translator

class RecipeModel:
    def __init__(self, model_name: str = "gpt2"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        
        # Устанавливаем токен для паддинга
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

        self.model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto", torch_dtype="auto")
        self.translator = Translator()

    def generate_recipe(self, ingredients: str, country: str, cooking_time: str) -> str:
        # Перевод входных данных на английский
        ingredients_en = self.translator.translate_to_en(ingredients)
        country_en = self.translator.translate_to_en(country)
        cooking_time_en = self.translator.translate_to_en(cooking_time)

        # Формирование промта
        prompt = (
            f"Here is recipe from {country_en} cuisine using {ingredients_en}. The preparation time is {cooking_time_en}."
        )

        # Генерация текста с помощью модели
        inputs = self.tokenizer(prompt, return_tensors="pt", padding=True, truncation=True)
        
        # Явно указываем attention_mask и pad_token_id
        attention_mask = inputs["attention_mask"]
        inputs["pad_token_id"] = self.tokenizer.pad_token_id

        # Генерация с использованием do_sample=True и top_p
        outputs = self.model.generate(
            inputs["input_ids"], 
            attention_mask=attention_mask, 
            do_sample=True, 
            top_p=0.9, 
            max_length=250, 
            min_length=100,
            temperature=0.7,
            repetition_penalty = 1.2,
            pad_token_id=50256,
            bos_token_id=50256,
            no_repeat_ngram_size=4
        )

        recipe_en = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Перевод результата на русский
        recipe_ru = self.translator.translate_to_ru(recipe_en)
        return recipe_ru

# Пример использования
if __name__ == "__main__":
    model = RecipeModel("gpt2")
    ingredients = "картофель, морковь, кетчуп, баран"
    country = "Россия"
    cooking_time = "30 минут"

    recipe = model.generate_recipe(ingredients, country, cooking_time)
    print(recipe)
