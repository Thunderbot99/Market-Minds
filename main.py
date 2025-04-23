import tkinter as tk
from tkinter import ttk
import yfinance as yf


class PageButton:
    def __init__(self, master, text):
        self.button = tk.Button(
            master=master,
            text=text,
            background="#2F2A2A",
            foreground="#FFFFFF",
            font="Calibri 40",
            relief="flat",
            command=loadpage(text)
        )


def search():
    searched = yf.Search(query=entryStr.get()).quotes[0]
    print(searched)
    stocks = yf.Ticker(searched['symbol'])
    output_label.config(text=f"{searched['shortname']}: {stocks.fast_info['lastPrice']}")


def loadpage(page):
    def loading():
        portfolio_button.button.configure(background="#2F2A2A")
        trade_button.button.configure(background="#2F2A2A")
        research_button.button.configure(background="#2F2A2A")
        if page == "Portfolio":
            portfolio_button.button.configure(background="#484242")
        if page == "Trade":
            trade_button.button.configure(background="#484242")
        if page == "Research":
            research_button.button.configure(background="#484242")
    return loading

window = tk.Tk()
window.title("Marketminds")
window.state("zoomed")
window.configure(bg="#2F2A2A")

title_frame_style = ttk.Style()
title_frame_style.configure("Main.TFrame", background="#2F2A2A")
title_frame = ttk.Frame(
    master=window,
    style="Main.TFrame"
)
title_frame.pack(anchor="nw", padx="5px", fill="x")

title_label_market = ttk.Label(
    master=title_frame,
    text="Market",
    foreground="#628840",
    background="#2F2A2A",
    font="Calibri 40 bold")
title_label_market.pack(side="left")

title_label_minds = ttk.Label(
    master=title_frame,
    text="Minds",
    foreground="#CDAE33",
    background="#2F2A2A",
    font="Calibri 40 bold")
title_label_minds.pack(side="left")

Balance = ttk.Label(
    master=title_frame,
    text="₱100,000",
    foreground="#FFFFFF",
    background="#2F2A2A",
    font="Calibri 40")
Balance.pack(side="right",anchor="ne")

Page_frame = tk.Frame(master=window, background="#2F2A2A")
Page_frame.pack(side="left", anchor="nw")

portfolio_button = PageButton(Page_frame, "Portfolio");
portfolio_button.button.pack(side="left",padx="10px")

trade_button = PageButton(Page_frame, "Trade");
trade_button.button.pack(side="left",padx="10px")

research_button = PageButton(Page_frame, "Research")
research_button.button.pack(side="left",padx="10px")

active_tab = "Portfolio"
portfolio_button.button.configure(background="#484242")

input_frame = ttk.Frame(master=window)

entryStr = tk.StringVar()
entry = ttk.Entry(
    master=input_frame,
    textvariable=entryStr)

button = ttk.Button(
    master=input_frame,
    text="Convert",
    command=search)

input_frame.pack(pady=10)
entry.pack(
    side="left",
    padx=10)
button.pack()


output_label = ttk.Label(
    master=window,
    text="Output",
    font="Calibri 24")

output_label.pack(pady=5)

window.mainloop()