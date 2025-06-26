import json
import tkinter as tk
from tkinter import ttk
from datetime import datetime, date
import yfinance as yf


class TimeTab:
    def __init__(self, window, topbarDate):
        self.root = tk.Frame(
            master=window,
            background="#2F2A2A"
        )
        self.root.pack(side="left", anchor="nw", fill="both")
        timeFrame = tk.Frame(
            master=self.root,
            background="#2F2A2A"
        )
        timeFrame.pack(anchor="nw")

        dayFrame = tk.Frame(
            master=timeFrame,
            background="#2F2A2A",
            padx=20
        )
        dayFrame.pack(anchor="nw", side="left")

        dayTitle = ttk.Label(
            master=dayFrame,
            text="Day",
            foreground="#FFFFFF",
            background="#2F2A2A",
            font="Calibri 40 bold"
        )
        dayTitle.pack(anchor="nw")

        def is_numeric(input):
            return input.isdigit() or input == ""

        vcmd = self.root.register(is_numeric)

        dayBar = tk.Entry(
            master=dayFrame,
            bg="#898686",
            font="Calibri 20",
            fg="#FFFFFF",
            validate="key",
            validatecommand=(vcmd, "%P")
        )
        dayBar.pack(anchor="nw")

        monthFrame = tk.Frame(
            master=timeFrame,
            background="#2F2A2A",
            padx=20
        )
        monthFrame.pack(anchor="nw", side="left")

        monthTitle = ttk.Label(
            master=monthFrame,
            text="Month",
            foreground="#FFFFFF",
            background="#2F2A2A",
            font="Calibri 40 bold"
        )
        monthTitle.pack(anchor="nw")

        monthBar = tk.Entry(
            master=monthFrame,
            bg="#898686",
            font="Calibri 20",
            fg="#FFFFFF",
            validate="key",
            validatecommand=(vcmd, "%P")
        )
        monthBar.pack(anchor="nw")

        yearFrame = tk.Frame(
            master=timeFrame,
            background="#2F2A2A",
            padx=20
        )
        yearFrame.pack(anchor="nw", side="left")

        yearTitle = ttk.Label(
            master=yearFrame,
            text="Year",
            foreground="#FFFFFF",
            background="#2F2A2A",
            font="Calibri 40 bold"
        )
        yearTitle.pack(anchor="nw")

        yearBar = tk.Entry(
            master=yearFrame,
            bg="#898686",
            font="Calibri 20",
            fg="#FFFFFF",
            validate="key",
            validatecommand=(vcmd, "%P")
        )

        yearBar.pack(anchor="nw")

        dateFrame = tk.Frame(
            master=self.root,
            background="#2F2A2A"
        )
        dateFrame.pack(anchor="nw", side="left", fill="both")

        dateTitle = ttk.Label(
            master=dateFrame,
            text="0-0-0",
            foreground="#FFFFFF",
            background="#2F2A2A",
            font="Calibri 40 bold"
        )
        dateTitle.pack(anchor="nw", padx=20)

        def travel():
            def valid_date():
                try:
                    travelDate = datetime.strptime(f"{dayVar.get()}-{monthVar.get()}-{yearVar.get()}", "%d-%m-%Y").date()
                    if travelDate <= date.today():
                        return True
                    else:
                        return False
                except ValueError:
                    return False
            if valid_date():
                with open("save.json", "r") as f:
                    data = json.load(f)
                day = int(dayVar.get())
                month = int(monthVar.get())
                if day < 10:
                    day = f"0{day}"
                if month < 10:
                    month = f"0{month}"
                data["Date"]["Day"] = day
                data["Date"]["Month"] = month
                data["Date"]["Year"] = yearVar.get()
                with open("save.json", "w") as f:
                    json.dump(data, f, indent=3)
                invalidTitle.configure(
                    text=""
                )
                topbarDate.configure(
                    text=update()
                )
            else:
                invalidTitle.configure(
                    text="Invalid Date"
                )

        travelButton = tk.Button(
            master=dateFrame,
            text="Travel",
            font="Calibri 20",
            fg="#FFFFFF",
            bg="#628840",
            activebackground="#628840",
            activeforeground="#FFFFFF",
            command=travel
        )

        travelButton.pack(anchor="nw", side="left", padx=20)

        invalidTitle = ttk.Label(
            master=dateFrame,
            text="",
            foreground="#D4241E",
            background="#2F2A2A",
            font="Calibri 40 bold"
        )
        invalidTitle.pack(anchor="nw", padx=20)

        def update(*args):
            day = dayVar.get()
            month = monthVar.get()
            if day != "":
                if int(day) < 10:
                    day = "0" + day
            if month != "":
                if int(month) < 10:
                    month = "0" + month
            dateTitle.configure(
                text=f"{day}-{month}-{yearVar.get()}"
            )
            return f"{day}-{month}-{yearVar.get()}"

        dayVar = tk.StringVar()
        dayVar.trace_add("write", update)
        dayBar.configure(textvariable=dayVar)

        monthVar = tk.StringVar()
        monthVar.trace_add("write", update)
        monthBar.configure(textvariable=monthVar)

        yearVar = tk.StringVar()
        yearVar.trace_add("write", update)
        yearBar.configure(textvariable=yearVar)