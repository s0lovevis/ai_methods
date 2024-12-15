from deep_translator import GoogleTranslator
from deep_translator.exceptions import NotValidPayload, TranslationNotFound

class Translator:
    def __init__(self, source_lang: str = "ru", target_lang: str = "en"):
        self.translator = GoogleTranslator(source=source_lang, target=target_lang)

    def translate_to_en(self, text: str) -> str:
        try:
            return self.translator.translate(text)
        except (NotValidPayload, TranslationNotFound) as e:
            return f"Ошибка перевода: {str(e)}"

    def translate_to_ru(self, text: str) -> str:
        try:
            return GoogleTranslator(source='en', target='ru').translate(text)
        except (NotValidPayload, TranslationNotFound) as e:
            return f"Ошибка перевода: {str(e)}"