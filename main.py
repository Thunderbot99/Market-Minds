import tkinter as tk
import json
from tkinter import ttk
import yfinance as yf


import Bank
import Portfolio
import Trade
import Time
import TopBar

window = tk.Tk()
window.title("Marketminds")
window.state("zoomed")
window.configure(bg="#2F2A2A")

pages = {}

Date = TopBar.pack(window, pages)

pages["Portfolio"] = Portfolio.PortfolioTab(window)

pages["Trade"] = Trade.TradeTab(window)
pages["Trade"].root.pack_forget()

pages["Time"] = Time.TimeTab(window, Date)
pages["Time"].root.pack_forget()

pages["Bank"] = Bank.BankTab(window)
pages["Bank"].root.pack_forget()

window.mainloop()