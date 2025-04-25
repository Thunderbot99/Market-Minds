import tkinter as tk
from tkinter import ttk
import yfinance as yf

import Portfolio
import Trade
import Research
import TopBar

window = tk.Tk()
window.title("Marketminds")
window.state("zoomed")
window.configure(bg="#2F2A2A")

pages = {}

TopBar.pack(window, pages)

pages["Portfolio"] = Portfolio.PortfolioTab(window)

pages["Trade"] = Trade.TradeTab(window)
pages["Trade"].root.pack_forget()

pages["Research"] = Research.ResearchTab(window)
pages["Research"].root.pack_forget()

window.mainloop()