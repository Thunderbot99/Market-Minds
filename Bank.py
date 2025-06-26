import json
import tkinter as tk
from tkinter import ttk
import yfinance as yf


class BankTab:
    def __init__(self, window):
        self.root = ttk.Frame(master=window)
        self.root.pack(side="left", anchor="nw")
        bankFrame = tk.Frame(
            master=self.root,
            background="#2F2A2A"
        )
        bankFrame.pack(anchor="nw")

        addFrame = tk.Frame(
            master=bankFrame,
            background="#2F2A2A",
            padx=20
        )
        addFrame.pack(anchor="nw", side="left")

        addTitle = ttk.Label(
            master=addFrame,
            text="Add",
            foreground="#FFFFFF",
            background="#2F2A2A",
            font="Calibri 40 bold"
        )
        addTitle.pack(anchor="nw")

        def is_numeric(input):
            return input.isdigit() or input == ""

        vcmd = self.root.register(is_numeric)

        addBar = tk.Entry(
            master=addFrame,
            bg="#898686",
            font="Calibri 20",
            fg="#FFFFFF",
            validate="key",
            validatecommand=(vcmd, "%P")
        )

        def add(event):
            with open("save.json", "r") as f:
                data = json.load(f)
            data["Bank"] += float(addBar.get())
            with open("save.json", "w") as f:
                json.dump(data, f, indent=3)

        addBar.bind("<Return>", add)
        addBar.pack(anchor="nw")

        removeFrame = tk.Frame(
            master=bankFrame,
            background="#2F2A2A",
            padx=20
        )
        removeFrame.pack(anchor="nw", side="left")

        removeTitle = ttk.Label(
            master=removeFrame,
            text="Remove",
            foreground="#FFFFFF",
            background="#2F2A2A",
            font="Calibri 40 bold"
        )
        removeTitle.pack(anchor="nw")

        removeBar = tk.Entry(
            master=removeFrame,
            bg="#898686",
            font="Calibri 20",
            fg="#FFFFFF",
            validate="key",
            validatecommand=(vcmd, "%P")
        )

        def remove(event):
            with open("save.json", "r") as f:
                data = json.load(f)
            data["Bank"] -= float(removeBar.get())
            if data["Bank"] < 0:
                data["Bank"] = 0
            with open("save.json", "w") as f:
                json.dump(data, f, indent=3)

        removeBar.bind("<Return>", remove)
        removeBar.pack(anchor="nw")
