import tkinter as tk
from tkinter import ttk
import yfinance as yf


class PortfolioTab:
    def __init__(self, window):
        self.root = tk.Frame(
            master=window,
            background="#2F2A2A"
        )
        self.root.pack(side="left", anchor="nw", fill="both")

        Shares = tk.Frame(
            master=self.root,
            background="#2F2A2A"
        )
        Shares.pack(side="left", anchor="n", fill="both", padx="10")
        sharesTitle = ttk.Label(
            master=Shares,
            text="Shares",
            foreground="#FFFFFF",
            background="#2F2A2A",
            font="Calibri 40 bold"
        )
        sharesTitle.pack(anchor="nw")
        

        canvas = tk.Canvas(
            Shares,
            borderwidth=0,
            background="#2F2A2A",
            highlightthickness=0
        )
        scrollbar = tk.Scrollbar(Shares, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, background="#2F2A2A")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)

        for i in range(20):
            item = tk.Frame(scrollable_frame, bg="lightgray", pady=10, padx=10)
            tk.Label(item, text=f"Item {i + 1}", font=("Arial", 14), bg="lightgray").pack(side="left")
            tk.Button(item, text="Action", bg="#007acc", fg="white").pack(side="right")
            item.pack(fill="x", pady=5, padx=5)

        def on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", on_mousewheel)  # Windows
