# Main.py
from tkinter import *
from tkinter import ttk, filedialog
import os
import pandas as pd
import webbrowser
from csvgrader.gui.mainWindow import MainWindow

filepath = "/home/auttieb/Documents/college/TA/211LSP25/120251-PHYS-211-labs-1.csv"
submitpath = "/home/auttieb/Documents/college/TA/211LSP25/submissions/lab1/L3E"

pd.options.mode.copy_on_write = True

rubric = {"1":{"1_1":"fail", "2_1":"ish", "3_1":"pass"}, "2":{"1_3":"fail", "2_2":"ish", "3_2":"pass"}}

if __name__ == "__main__":
    mw = MainWindow()
    mw.run()