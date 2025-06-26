import tkinter as tk
from tkinter import ttk
import json
import yfinance as yf
import conversionRates
import os
import pandas as pd


class PortfolioTab:
    def __init__(self, window):
        self.root = tk.Frame(
            master=window,
            background="#2F2A2A"
        )
        self.root.pack(side="left", anchor="nw", fill="both", expand=True)

        Shares = tk.Frame(
            master=self.root,
            background="#2F2A2A"
        )
        Shares.pack(side="left", anchor="n", fill="both", padx="10", expand=True)
        overviewTitle = ttk.Label(
            master=Shares,
            text="Overview",
            foreground="#FFFFFF",
            background="#2F2A2A",
            font="Calibri 40 bold"
        )
        overviewTitle.pack(anchor="nw")

        overviewFrame = tk.Frame(
            master=Shares,
            background="#474040"
        )
        overviewFrame.pack(anchor="nw", fill="both", pady=10)

        valueTitle = ttk.Label(
            master=overviewFrame,
            text="Cash Balance",
            foreground="#FFFFFF",
            background="#474040",
            font="Calibri 20"
        )
        valueTitle.pack(anchor="nw", padx=10)

        with open("save.json", "r") as f:
            data = json.load(f)

        cashValue = ttk.Label(
            master=overviewFrame,
            text=f"₱{data['Bank']:.2f}",
            foreground="#FFFFFF",
            background="#474040",
            font="Calibri 40 bold"
        )
        cashValue.pack(anchor="nw", padx=20)

        portfolioTitle = ttk.Label(
            master=overviewFrame,
            text="Portfolio Value",
            foreground="#FFFFFF",
            background="#474040",
            font="Calibri 20"
        )
        portfolioTitle.pack(anchor="nw", padx=10)

        accountValue = ttk.Label(
            master=overviewFrame,
            text="₱10,000.00",
            foreground="#FFFFFF",
            background="#474040",
            font="Calibri 40 bold"
        )
        accountValue.pack(anchor="nw", padx=20)

        holdingFrame = tk.Frame(
            master=Shares,
            background="#2F2A2A",
        )
        holdingFrame.pack(anchor="nw")

        holdingTitle = ttk.Label(
            master=holdingFrame,
            text="Holdings",
            foreground="#FFFFFF",
            background="#2F2A2A",
            font="Calibri 40 bold"
        )
        holdingTitle.pack(anchor="nw", side="left")

        def is_numeric(input):
            return input.isdigit() or input == ""

        vcmd = self.root.register(is_numeric)

        sellBar = tk.Entry(
            master=holdingFrame,
            bg="#898686",
            font="Calibri 20",
            fg="#FFFFFF",
            validate="key",
            validatecommand=(vcmd, "%P")
        )
        sellBar.pack(anchor="nw", side="left", padx=10, pady=10)

        canvasing = 0
        selling = []
        def sell():
            gaining = 0
            sellingNum = int(sellBar.get())
            with open("save.json", "r") as f:
                data = json.load(f)
            for i in selling:
                if i.selling:
                    if data['Holding'][i.key][1] <= sellingNum:
                        gaining += (i.price * data['Holding'][i.key][1])
                        del data['Holding'][i.key]
                    else:
                        gaining += (i.price * sellingNum)
                        data['Holding'][i.key][1] -= sellingNum
            data["Bank"] += gaining
            with open("save.json", "w") as f:
                json.dump(data, f, indent=3)
            selling.clear()
            canvasing.__init__(canvasing.canvas)

        sellButton = tk.Button(
            master=holdingFrame,
            text="Sell",
            font="Calibri 20",
            fg="#FFFFFF",
            bg="#628840",
            activebackground="#628840",
            activeforeground="#FFFFFF",
            command=sell
        )

        sellButton.pack(anchor="nw", side="left", padx=20)

        tagFrame = tk.Frame(
            master=Shares,
            background="#2F2A2A"
        )
        tagFrame.pack(anchor="nw", fill="both")
        tk.Label(
            master=tagFrame,
            text="Company",
            foreground="#FFFFFF",
            background="#2F2A2A",
            font="Calibri 20"
        ).pack(side="left", padx=10)
        tk.Label(
            master=tagFrame,
            text="Shares",
            foreground="#FFFFFF",
            background="#2F2A2A",
            font="Calibri 20"
        ).pack(side="left", padx=(350, 0))
        tk.Label(
            master=tagFrame,
            text="Price",
            foreground="#FFFFFF",
            background="#2F2A2A",
            font="Calibri 20"
        ).pack(side="left", padx=(300, 0))



        class canvaser:
            def __init__(self, canvas):
                if canvas != 0:
                    canvas.destroy()
                canvas = tk.Canvas(
                    Shares,
                    borderwidth=0,
                    background="#474040",
                    highlightthickness=0
                )
                scrollbar = tk.Scrollbar(Shares, orient="vertical", command=canvas.yview)
                scrollable_frame = tk.Frame(canvas, background="#474040")

                scrollable_frame.bind(
                    "<Configure>",
                    lambda e: canvas.configure(
                        scrollregion=canvas.bbox("all")
                    )
                )

                canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
                canvas.configure(yscrollcommand=scrollbar.set)

                canvas.pack(side="left", fill="both", expand=True, pady=10)

                holdings = tk.Frame(scrollable_frame, bg="#474040", pady=10, padx=5)
                holdings.grid(row=0, column=0, sticky="ew", pady=3)
                holdings.grid_columnconfigure(0, minsize=400)
                holdings.grid_columnconfigure(1, minsize=100)
                holdings.grid_columnconfigure(2, minsize=300)
                holdings.grid_columnconfigure(3, minsize=100)
                num = 0

                with open("save.json", "r") as f:
                    data = json.load(f)
                total = 0

                class button:
                    def __init__(self, key, price):
                        self.selling = False
                        self.key = key
                        self.price = price
                        def press():
                            if not self.selling:
                                self.button.configure(
                                    bg="#628840"
                                )
                                self.selling = True
                            else:
                                self.button.configure(
                                    bg="#FFFFFF"
                                )
                                self.selling = False

                        self.button = tk.Button(
                            master=holdings,
                            bg="#FFFFFF",
                            width=2,
                            height=1,
                            relief="flat",
                            activebackground="#628840",
                            highlightthickness=0,
                            bd=0,
                            command=press
                        )

                for i in data["Holding"]:
                    with open("save.json", "r") as f:
                        date = json.load(f)
                    if not os.path.exists(f"cache/{date['Date']['Year']}"):
                        os.mkdir(f"./cache/{date['Date']['Year']}")
                    if not os.path.exists(f"cache/{date['Date']['Year']}/{i}.csv"):
                        stock = yf.Ticker(i)
                        hist = stock.history(start=f"{date['Date']['Year']}-01-01", end=f"{date['Date']['Year']}-12-31")
                        hist["Currency"] = stock.info.get("currency", "USD")
                        hist.to_csv(f"cache/{date['Date']['Year']}/{i}.csv")
                    else:
                        hist = pd.read_csv(f"cache/{date['Date']['Year']}/{i}.csv", index_col="Date", parse_dates=True)
                    targetDate = pd.to_datetime(f"{date['Date']['Year']}-{date['Date']['Month']}-{date['Date']['Day']}")
                    hist.index = pd.to_datetime(hist.index, utc=True).tz_localize(None)
                    hist = hist.sort_index()
                    validDates = hist.index[hist.index <= targetDate]
                    stock_price = hist.loc[validDates[-1]]["Close"] / conversionRates.rates[hist["Currency"].iloc[0]]
                    total += (stock_price * data['Holding'][i][1])
                    tk.Label(holdings, text=f"{data['Holding'][i][0]}", font=("Calibri", 15), bg="#474040",
                             fg="#FFFFFF",
                             anchor="w", padx=10).grid(row=num, column=0, sticky="w")
                    tk.Label(holdings, text=f"{data['Holding'][i][1]}", font=("Calibri", 15), bg="#474040",
                             fg="#FFFFFF",
                             anchor="e").grid(row=num, column=1, sticky="e")
                    tk.Label(holdings, text=f"₱{stock_price * data['Holding'][i][1]:.2f}", font=("Calibri", 15),
                             bg="#474040", fg="#FFFFFF",
                             anchor="e").grid(row=num, column=2, sticky="e")
                    stock_button = button(i, stock_price)
                    stock_button.button.grid(row=num, column=3, sticky="e")
                    selling.append(stock_button)
                    num += 1

                accountValue.configure(text=f"₱{total:.2f}")
                cashValue.configure(text=f"₱{data['Bank']:.2f}")

                def on_mousewheel(event):
                    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

                canvas.bind_all("<MouseWheel>", on_mousewheel)
                self.canvas = canvas

        canvasing = canvaser(0)

        performance_frame = tk.Frame(
            master=self.root,
            background="#2F2A2A"
        )
        performance_frame.pack(side="right", anchor="n", fill="both", padx="10", expand=True)
        performanceTitle = ttk.Label(
            master=performance_frame,
            text="Performance",
            foreground="#FFFFFF",
            background="#2F2A2A",
            font="Calibri 40 bold"
        )
        performanceTitle.pack(anchor="nw")
