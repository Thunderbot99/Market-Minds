import json
import tkinter as tk
from tkinter import ttk
import yfinance as yf
import threading
import conversionRates
import os
import pandas as pd

class TradeTab:
    def __init__(self, window):
        self.root = tk.Frame(
            master=window,
            bg="#2F2A2A"
        )
        self.root.pack(side="left", anchor="nw", fill="both", expand=True)
        inputsFrame = tk.Frame(
            master=self.root,
            background="#2F2A2A"
        )
        inputsFrame.pack(anchor="nw")

        searchFrame = tk.Frame(
            master=inputsFrame,
            background="#2F2A2A",
            padx=20
        )
        searchFrame.pack(anchor="nw", side="left")

        searchTitle = ttk.Label(
            master=searchFrame,
            text="Company",
            foreground="#FFFFFF",
            background="#2F2A2A",
            font="Calibri 40 bold"
        )
        searchTitle.pack(anchor="nw")

        searchBar = tk.Entry(
            master=searchFrame,
            bg="#898686",
            font="Calibri 20",
            fg="#FFFFFF"
        )

        stockFrame = tk.Frame(
            master=inputsFrame,
            background="#2F2A2A",
            padx=20
        )
        stockFrame.pack(anchor="nw", side="left")

        stockTitle = ttk.Label(
            master=stockFrame,
            text="Stocks",
            foreground="#FFFFFF",
            background="#2F2A2A",
            font="Calibri 40 bold"
        )
        stockTitle.pack(anchor="nw")

        def is_numeric(input):
            return input.isdigit() or input == ""

        vcmd = self.root.register(is_numeric)

        stockBar = tk.Entry(
            master=stockFrame,
            bg="#898686",
            font="Calibri 20",
            fg="#FFFFFF",
            validate="key",
            validatecommand=(vcmd, "%P")
        )
        stockBar.pack(anchor="nw", pady=10)

        priceFrame = tk.Frame(
            master=inputsFrame,
            background="#2F2A2A",
            padx=20
        )
        priceFrame.pack(anchor="nw", side="left")

        priceTitle = tk.Label(
            master=priceFrame,
            text="₱0.00",
            foreground="#FFFFFF",
            background="#2F2A2A",
            font="Calibri 40 bold"
        )
        priceTitle.pack(anchor="nw", side="left")

        buttons = []

        def buy():
            with open("save.json", "r") as f:
                data = json.load(f)
            if data["Bank"] >= float(priceTitle["text"][1:]):
                for i in buttons:
                    if i.buying:
                        if i.symbol in data["Holding"]:
                            data["Holding"][i.symbol] = [i.name, int(stockBar.get()) + data["Holding"][i.symbol][1]]
                        else:
                            data["Holding"][i.symbol] = [i.name, int(stockBar.get())]
                data["Bank"] -= float(priceTitle["text"][1:])
            else:
                print("Insufficient Funds")
            with open("save.json", "w") as f:
                json.dump(data, f, indent=3)

        buyButton = tk.Button(
            master=priceFrame,
            text="Buy",
            font="Calibri 20",
            fg="#FFFFFF",
            bg="#628840",
            activebackground="#628840",
            activeforeground="#FFFFFF",
            command=buy
        )

        buyButton.pack(anchor="nw", side="left", padx=20)

        self.canvas = 0

        def update(*args):
            total = 0
            if stock_var.get() != "":
                for i in buttons:
                    if i.buying:
                        total += i.price * int(stockBar.get())
            priceTitle.configure(
                text=f"₱{total:.2f}"
            )

        stock_var = tk.StringVar()
        stock_var.trace_add("write", update)
        stockBar.configure(textvariable=stock_var)
        class stock:
            def __init__(self, stocking, companies, price):
                self.price = price
                self.symbol = stocking['symbol']
                self.name = stocking['longname']
                self.buying = False


                def press():
                    if not self.buying:
                        self.button.configure(
                            bg="#628840"
                        )
                        self.buying = True
                    else:
                        self.button.configure(
                            bg="#FFFFFF"
                        )
                        self.buying = False
                    update()

                self.button = tk.Button(
                    companies,
                    bg="#FFFFFF",
                    width=2,
                    height=1,
                    relief="flat",
                    activebackground="#628840",
                    highlightthickness=0,
                    bd=0,
                    command=press
                )
        def search(event):
            if self.canvas != 0:
                self.canvas.destroy()
            searched = yf.Search(query=searchBar.get()).quotes
            #output_label.config(text=f"{searched['shortname']}: {stocks.fast_info['lastPrice']}")
            self.canvas = tk.Canvas(
                self.root,
                borderwidth=0,
                background="#474040",
                highlightthickness=0
            )
            scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
            scrollable_frame = tk.Frame(self.canvas, background="#474040")

            scrollable_frame.bind(
                "<Configure>",
                lambda e: self.canvas.configure(
                    scrollregion=self.canvas.bbox("all")
                )
            )

            self.canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            self.canvas.configure(yscrollcommand=scrollbar.set)

            self.canvas.pack(side="left", fill="both", expand=True, pady=20, padx=20)

            companies = tk.Frame(scrollable_frame, bg="#474040", pady=10, padx=5)
            companies.grid(row=0, column=0, sticky="ew", pady=3)
            companies.grid_columnconfigure(0, minsize=500)
            companies.grid_columnconfigure(1, minsize=100)
            companies.grid_columnconfigure(2, minsize=100)
            def searching():
                num = 0
                buttons.clear()
                for i in searched:
                    try:
                        with open("save.json", "r") as f:
                            date = json.load(f)
                        if not os.path.exists(f"cache/{date['Date']['Year']}"):
                            os.mkdir(f"./cache/{date['Date']['Year']}")
                        if not os.path.exists(f"cache/{date['Date']['Year']}/{i}.csv"):
                            stocker = yf.Ticker(i['symbol'])
                            hist = stocker.history(start=f"{date['Date']['Year']}-01-01",
                                                 end=f"{date['Date']['Year']}-12-31")
                            hist["Currency"] = stocker.info.get("currency", "USD")
                            hist.to_csv(f"cache/{date['Date']['Year']}/{i['symbol']}.csv")
                        else:
                            hist = pd.read_csv(f"cache/{date['Date']['Year']}/{i['symbol']}.csv", index_col="Date",
                                               parse_dates=True)
                        targetDate = pd.to_datetime(
                            f"{date['Date']['Year']}-{date['Date']['Month']}-{date['Date']['Day']}")
                        hist.index = pd.to_datetime(hist.index, utc=True).tz_localize(None)
                        hist = hist.sort_index()
                        validDates = hist.index[hist.index <= targetDate]
                        stock_price = hist.loc[validDates[-1]]["Close"] / conversionRates.rates[
                            hist["Currency"].iloc[0]]
                        tk.Label(companies, text=f"₱{stock_price:.2f}", font=("Calibri", 15),
                                 bg="#474040",
                                 fg="#FFFFFF", anchor="e").grid(row=num, column=1, sticky="e")
                        tk.Label(companies, text=f"{i['longname']}", font=("Calibri", 15), bg="#474040", fg="#FFFFFF",
                                 anchor="w", padx=10).grid(row=num, column=0, sticky="w")
                        buttons.append(stock(i, companies, stock_price))
                        buttons[num].button.grid(
                            row=num,
                            column=2,
                            sticky="e"
                        )
                    except Exception as e:
                        print(e)
                        continue
                    num += 1

            threading.Thread(target=searching).start()

            def on_mousewheel(event):
                self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

            self.canvas.bind_all("<MouseWheel>", on_mousewheel)
        searchBar.bind("<Return>", search)
        searchBar.pack(anchor="nw", pady=10)

        tagFrame = tk.Frame(
            master=self.root,
            background="#2F2A2A"
        )
        tagFrame.pack(anchor="nw", fill="both")
        tk.Label(
            master=tagFrame,
            text="Company",
            foreground="#FFFFFF",
            background="#2F2A2A",
            font="Calibri 20"
        ).pack(side="left", padx=30)
        tk.Label(
            master=tagFrame,
            text="Price",
            foreground="#FFFFFF",
            background="#2F2A2A",
            font="Calibri 20"
        ).pack(side="left", padx=(400, 10))
        tk.Label(
            master=tagFrame,
            text="Buy",
            foreground="#FFFFFF",
            background="#2F2A2A",
            font="Calibri 20"
        ).pack(side="left", padx=50)