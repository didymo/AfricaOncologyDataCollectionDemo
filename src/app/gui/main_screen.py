# main_screen.py
import tkinter as tk
from tkinter import ttk


class MainScreen(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        ttk.Label(
            self, text="Welcome to the Oncology Data Collection App", font=("Arial", 16)
        ).pack(pady=10)

        # Example Widget
        ttk.Button(self, text="Exit", command=parent.destroy).pack(pady=20)
