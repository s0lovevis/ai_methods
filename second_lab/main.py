import tkinter as tk
from ruGPTModel import ruGPTModel
import threading
import time

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
    next_button.pack(pady=10)

def update_ui():
    # Очищаем окно
    for widget in root.winfo_children():
        widget.destroy()

    # Устанавливаем фон окна
    root.configure(bg="#e0f7fa")  # Пастельный цвет фона

    # Устанавливаем шрифты
    title_font = ("Arial", 18, "bold")
    input_font = ("Arial", 12)
    button_font = ("Arial", 14, "bold")
    output_font = ("Arial", 12)

    # Создаем заголовок
    title_label = tk.Label(root, text="Напиши предложение и модели семейства ruGPT его закончат!",
                           font=title_font, justify="center", bg="#e0f7fa")
    title_label.grid(row=0, column=0, columnspan=3, pady=20)

    # Создаем текстовое поле для ввода
    global text_input
    text_input = tk.Text(root, height=5, width=50, wrap=tk.WORD, font=input_font, bg="#ffffff", fg="#000000")
    text_input.grid(row=1, column=0, columnspan=3, pady=10)

    # Создаем кнопку отправки
    global submit_button
    submit_button = tk.Button(root, text="Отправить", command=on_submit, font=button_font, bg="#4CAF50", fg="#ffffff")
    submit_button.grid(row=2, column=0, columnspan=3, pady=10)

    # Создаем три LabelFrame для вывода результатов
    frame1 = tk.LabelFrame(root, text="ruGPT3Small", font=("Arial", 14, "bold"), bg="#ffffff", relief=tk.SUNKEN, bd=2, padx=10, pady=10)
    frame1.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")
    global output_label1, time_label1
    output_label1 = tk.Label(frame1, text="", font=output_font, wraplength=200, justify="left", bg="#ffffff", fg="#000000")
    output_label1.pack(fill=tk.BOTH, expand=True)
    time_label1 = tk.Label(frame1, text="", font=output_font, bg="#ffffff", fg="#000000")
    time_label1.pack()

    frame2 = tk.LabelFrame(root, text="ruGPT3Medium", font=("Arial", 14, "bold"), bg="#ffffff", relief=tk.SUNKEN, bd=2, padx=10, pady=10)
    frame2.grid(row=3, column=1, padx=10, pady=10, sticky="nsew")
    global output_label2, time_label2
    output_label2 = tk.Label(frame2, text="", font=output_font, wraplength=200, justify="left", bg="#ffffff", fg="#000000")
    output_label2.pack(fill=tk.BOTH, expand=True)
    time_label2 = tk.Label(frame2, text="", font=output_font, bg="#ffffff", fg="#000000")
    time_label2.pack()

    frame3 = tk.LabelFrame(root, text="ruGPT3Large", font=("Arial", 14, "bold"), bg="#ffffff", relief=tk.SUNKEN, bd=2, padx=10, pady=10)
    frame3.grid(row=3, column=2, padx=10, pady=10, sticky="nsew")
    global output_label3, time_label3
    output_label3 = tk.Label(frame3, text="", font=output_font, wraplength=200, justify="left", bg="#ffffff", fg="#000000")
    output_label3.pack(fill=tk.BOTH, expand=True)
    time_label3 = tk.Label(frame3, text="", font=output_font, bg="#ffffff", fg="#000000")
    time_label3.pack()

    # Настройка сетки для растяжения фреймов
    root.grid_rowconfigure(3, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    root.grid_columnconfigure(2, weight=1)

def on_submit():
    input_text = text_input.get("1.0", tk.END).strip()
    if input_text:
        # Очищаем прошлые ответы
        output_label1.config(text="")
        output_label2.config(text="")
        output_label3.config(text="")
        time_label1.config(text="")
        time_label2.config(text="")
        time_label3.config(text="")

        # Изменяем состояние кнопки
        submit_button.config(state=tk.DISABLED, text="Модель думает", bg="#cccccc")
        # Запускаем генерацию в отдельном потоке
        threading.Thread(target=generate_and_update, args=(input_text,)).start()

def generate_and_update(input_text):
    def update_output(label, result, time_label, elapsed_time):
        label.config(text=result)
        time_label.config(text=f"Время: {elapsed_time:.1f} секунд")
        submit_button.config(state=tk.NORMAL, text="Отправить", bg="#4CAF50")

    def generate_model(model, input_text, label, time_label):
        start_time = time.time()
        result = model.generate(input_text)
        end_time = time.time()
        elapsed_time = end_time - start_time
        update_output(label, result, time_label, elapsed_time)

    # Запускаем генерацию для каждой модели в отдельном потоке
    threading.Thread(target=generate_model, args=(model1, input_text, output_label1, time_label1)).start()
    threading.Thread(target=generate_model, args=(model2, input_text, output_label2, time_label2)).start()
    threading.Thread(target=generate_model, args=(model3, input_text, output_label3, time_label3)).start()

def on_next():
    update_ui()

# Создаем основное окно
root = tk.Tk()
root.title("Генерация предложений")
root.geometry("900x700")
root.resizable(False, False)

# Устанавливаем фон окна
root.configure(bg="#e0f7fa")  # Пастельный цвет фона

# Создаем метку для отображения загрузки моделей
loading_label = tk.Label(root, text="Загружаем модели из кэша...", font=("Arial", 18, "bold"), justify="center", bg="#e0f7fa")
loading_label.pack(pady=20)

# Создаем кнопку для перехода к генерациям
next_button = tk.Button(root, text="Перейти к генерациям", command=on_next, font=("Arial", 14, "bold"), bg="#4CAF50", fg="#ffffff")

# Запускаем загрузку моделей в отдельном потоке
threading.Thread(target=load_models).start()

root.mainloop()