import tkinter as tk
from tkinter import ttk, messagebox
import time
from ruGPTModel import ruGPTModel

# Блоки интерфейса кладем в глобальные переменные
model_name: str = "sberbank-ai/rugpt3small_based_on_gpt2"
model: ruGPTModel = None
root: tk.Tk = None
generate_button: ttk.Button = None
input_text_widget: tk.Text = None
output_text_widget: tk.Text = None
time_label: ttk.Label = None


def generate_text() -> None:
    """
    Функция для генерации текста на основе входного текста.
    """
    global model

    generate_button.config(state="disabled", text="Генерация...")
    root.update()

    input_text = input_text_widget.get("1.0", "end-1c")
    if not input_text:
        messagebox.showwarning("Warning", "Необходимо ввести текст!")
        generate_button.config(state="normal", text="Сгенерировать текст")
        return

    model = ruGPTModel(model_name)
    gen_start = time.time()
    generated_text = model.generate(input_text)
    gen_end = time.time()
    output_text_widget.config(state="normal")
    output_text_widget.delete("1.0", "end")
    output_text_widget.insert("1.0", generated_text)
    output_text_widget.config(state="disabled")

    time_label.config(text=f"Генерация заняла {round(gen_end-gen_start, 2)} секунд")
    generate_button.config(state="normal", text="Сгенерировать текст")

def update_model_name(*args) -> None:
    """
    Функция для обновления выбранной модели.
    """
    global model_name
    model_name = model_var.get()

# Функция для создания графического интерфейса
def create_gui(root_window: tk.Tk) -> None:
    """
    Функция для создания графического интерфейса.

    Args:
        root_window (tk.Tk): Основное окно приложения.
    """
    global root, generate_button, input_text_widget, output_text_widget, time_label, model_var

    root = root_window
    root.title("Приложение для генерации текста")

    # Выбор модели
    model_frame = ttk.LabelFrame(root, text="Выберите модель")
    model_frame.pack(padx=10, pady=10, fill="x")

    models = [
        "sberbank-ai/rugpt3small_based_on_gpt2",
        "sberbank-ai/rugpt3medium_based_on_gpt2",
        "sberbank-ai/rugpt3large_based_on_gpt2"
    ]

    model_var = tk.StringVar(value=models[0])
    model_var.trace("w", update_model_name)
    for model in models:
        ttk.Radiobutton(model_frame, text=model, variable=model_var, value=model).pack(anchor="w")

    # Ввод текста
    input_frame = ttk.LabelFrame(root, text="Введите текст")
    input_frame.pack(padx=10, pady=10, fill="x")

    input_text_widget = tk.Text(input_frame, height=5)
    input_text_widget.pack(fill="x")

    # Кнопка для генерации текста
    generate_button = ttk.Button(root, text="Сгенерировать текст", command=generate_text)
    generate_button.pack(pady=10)

    # Вывод сгенерированного текста
    output_frame = ttk.LabelFrame(root, text="Результат")
    output_frame.pack(padx=10, pady=10, fill="both", expand=True)

    output_text_widget = tk.Text(output_frame, height=10, state="disabled")
    output_text_widget.pack(fill="both", expand=True)

    # Время генерации
    time_label = ttk.Label(root, text="")
    time_label.pack(pady=10)
