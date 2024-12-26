import tkinter as tk
from tkinter import ttk


class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("My Tkinter App")
        self.geometry("800x600")

        # Configure main window
        self.configure(padx=10, pady=10)

        # Create main frame
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(expand=True, fill="both")

        # Add your widgets here
        self.label = ttk.Label(self.main_frame, text="Hello, World!")
        self.label.pack(pady=20)

    def run(self):
        self.mainloop()
