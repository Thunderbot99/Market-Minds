import json
import tkinter as tk
from tkinter import ttk
import yfinance as yf

buttons = []
pagers = {}
windowing = 0
dating = 0
class PageButton:
    def __init__(self, master, text):
        self.text = text
        self.button = tk.Button(
            master=master,
            text=text,
            background="#2F2A2A",
            foreground="#FFFFFF",
            font="Calibri 40",
            relief="flat",
            activebackground="#484242",
            activeforeground="#FFFFFF",
            highlightthickness=0,
            bd=0
        )
        self.button.configure(
            command=loadpage(self)
        )
        global buttons
        buttons.append(self.button)


def loadpage(thisbutton):
    def loading():
        global buttons
        for i in buttons:
            i.configure(background="#2F2A2A")
        thisbutton.button.configure(background="#484242")
        global pagers
        for i in pagers:
            pagers[i].root.destroy()
        global windowing, dating
        if thisbutton.text == "Time":
            pagers[thisbutton.text].__init__(windowing, dating)
        else:
            pagers[thisbutton.text].__init__(windowing)
    return loading


def pack(window, pages):
    global pagers
    pagers = pages
    global windowing
    windowing = window
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

    with open("save.json") as f:
        data = json.load(f)
    Date = tk.Label(
        master=title_frame,
        text=f"{data['Date']['Day']}-{data['Date']['Month']}-{data['Date']['Year']}",
        foreground="#FFFFFF",
        background="#2F2A2A",
        font="Calibri 40")
    Date.pack(side="right", anchor="ne")

    Page_frame = tk.Frame(master=window, background="#2F2A2A")
    Page_frame.pack(anchor="nw", fill="x")

    portfolio_button = PageButton(Page_frame, "Portfolio");
    portfolio_button.button.pack(side="left", padx="10px")

    trade_button = PageButton(Page_frame, "Trade");
    trade_button.button.pack(side="left", padx="10px")

    time_button = PageButton(Page_frame, "Time")
    time_button.button.pack(side="left", padx="10px")

    bank_button = PageButton(Page_frame, "Bank")
    bank_button.button.pack(side="left", padx="10px")

    portfolio_button.button.configure(background="#484242")
    global dating
    dating = Date
    return Date

