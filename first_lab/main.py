import tkinter as tk
from tkinter import ttk
from first_api import call_first_api  # Импорт API 1
from second_api import call_second_api  # Импорт API 2

# Функция для обработки ответа от API 1
def check_sentiment_api_1(text):
    try:
        result = call_first_api(text)  # Получаем результат из API 1
        # Возвращаем строку с результатами
        return f"Фраза позитивна с вероятностью {result['pos']}%\nФраза негативна с вероятностью {result['neg']}%"
    except Exception as e:
        return f"Ошибка API 1: {str(e)}"

# Функция для обработки ответа от API 2
def check_sentiment_api_2(text):
    try:
        result = call_second_api(text)  # Получаем результат из API 2
        # Возвращаем строку с результатами
        return f"Фраза позитивна с вероятностью {result['pos']}%\nФраза негативна с вероятностью {result['neg']}%\nФраза нейтральна с вероятностью {result['neu']}%"
    except Exception as e:
        return f"Ошибка API 2: {str(e)}"

# Функция для анализа текста через обе API
def analyze_sentiment():
    user_text = input_text.get()
    
    result_api_1 = check_sentiment_api_1(user_text)
    result_api_2 = check_sentiment_api_2(user_text)
    
    # Отображение результатов в GUI
    result_label_1.config(text=f"{result_api_1}")
    result_label_2.config(text=f"{result_api_2}")

# Интерфейс с помощью tkinter
root = tk.Tk()
root.title("Sentimental Analysis Master")
root.geometry("800x500")
root.configure(bg='#f0f0f0')

# Заголовок
title_label = tk.Label(root, text="Оценка тональности текста", font=("Helvetica", 20, "bold"), bg='#f0f0f0')
title_label.pack(pady=15)

# Поле ввода текста
input_frame = tk.Frame(root, bg='#f0f0f0')
input_frame.pack(pady=10)

input_label = tk.Label(input_frame, text="Введите текст:", font=("Helvetica", 14), bg='#f0f0f0')
input_label.grid(row=0, column=0, padx=5)

input_text = tk.Entry(input_frame, width=50, font=("Helvetica", 14), justify="center")
input_text.grid(row=0, column=1, padx=5)

# Кнопка для анализа текста
analyze_button = tk.Button(root, text="Анализировать", font=("Helvetica", 14), command=analyze_sentiment, bg='#4caf50', fg='white', padx=10, pady=5)
analyze_button.pack(pady=15)

# Рамка для разделения блоков API
result_frame = tk.Frame(root, bg='#f0f0f0')
result_frame.pack(pady=10)

# Блок для API 1
api_1_frame = tk.LabelFrame(result_frame, text="Psycology AI API", font=("Helvetica", 14, "bold"), bg='#f0f0f0', padx=10, pady=10)
api_1_frame.grid(row=0, column=0, padx=20, pady=10)

result_label_1 = tk.Label(api_1_frame, text="Ожидание...", font=("Helvetica", 14), bg='#f0f0f0')
result_label_1.pack()

# Блок для API 2
api_2_frame = tk.LabelFrame(result_frame, text="Sentiment Analyzer API", font=("Helvetica", 14, "bold"), bg='#f0f0f0', padx=10, pady=10)
api_2_frame.grid(row=1, column=0, padx=20, pady=10)

result_label_2 = tk.Label(api_2_frame, text="Ожидание...", font=("Helvetica", 14), bg='#f0f0f0')
result_label_2.pack()

# Запуск интерфейса
root.mainloop()
