import tkinter as tk
from tkinter import ttk
import yfinance as yf


class ResearchTab:
    def __init__(self, window):
        self.root = ttk.Frame(master=window)
        self.root.pack(side="left", anchor="nw")
        Holding_Frame = ttk.Frame(master=self.root)
        Holding_Frame.pack(side="left", anchor="nw")

        scrollbar = tk.Scrollbar(master=Holding_Frame)
        scrollbar.pack(side="right", fill="y")

        listbox = tk.Listbox(master=Holding_Frame, yscrollcommand=scrollbar.set, width=50, height=20)
        listbox.pack(side="left", fill="both")
        scrollbar.config(command=listbox.yview)

        for i in range(30):
            listbox.insert(tk.END, f"Item {i + 1}")

        def on_mousewheel(event):
            listbox.yview_scroll(int(-1 * (event.delta / 120)), "units")

        listbox.bind("<MouseWheel>", on_mousewheel)
        # Performance_Frame = tk.Frame(master=window)
        # Performance_Frame.pack(side="right")
