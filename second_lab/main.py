import tkinter as tk
import threading
from ui import update_ui, root
from model_loader import load_models

if __name__ == "__main__":
    # Надпись про загрузку моделек
    loading_label = tk.Label(
        root,
        text="Загружаем модели из кэша...",
        font=("Arial", 18, "bold"),
        justify="center",
        bg="#e0f7fa",
    )
    loading_label.pack(pady=20)

    next_button = tk.Button(
        root,
        text="Перейти к генерациям",
        command=update_ui,
        font=("Arial", 14, "bold"),
        bg="#4CAF50",
        fg="#ffffff",
    )

    threading.Thread(target=load_models).start()

    root.mainloop()
