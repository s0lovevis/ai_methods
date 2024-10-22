import time
import tkinter as tk
from ruGPTModel import ruGPTModel
from ui import root

# Глобальные переменные для хранения моделей
model1 = None
model2 = None
model3 = None

def load_model(model_name, model_path):
    global model1, model2, model3
    start_time = time.time()
    if model_name == "ruGPT3Small":
        model1 = ruGPTModel(model_path)
    elif model_name == "ruGPT3Medium":
        model2 = ruGPTModel(model_path)
    elif model_name == "ruGPT3Large":
        model3 = ruGPTModel(model_path)
    end_time = time.time()
    elapsed_time = end_time - start_time

    new_model_info = tk.Label(root, text=f"Модель {model_name} загружена за: {elapsed_time:.1f} секунд", font=("Arial", 17, "bold"), justify="center", bg="#e0f7fa")
    new_model_info.pack(pady=20)

    root.update_idletasks()

def load_models():
    load_model("ruGPT3Small", "sberbank-ai/rugpt3small_based_on_gpt2")
    load_model("ruGPT3Medium", "sberbank-ai/rugpt3medium_based_on_gpt2")
    load_model("ruGPT3Large", "sberbank-ai/rugpt3large_based_on_gpt2")
    loading_label.config(text="Все модели загружены.")
    next_button.pack(pady=10)  # Показываем кнопку только после загрузки
