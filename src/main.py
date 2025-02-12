# Main.py
import os
import pandas as pd
import webbrowser
import json

from MainWindow import MainWindow

filepath = "/home/auttieb/Documents/college/TA/211LSP25/120251-PHYS-211-labs-1.csv"
submitpath = "/home/auttieb/Documents/college/TA/211LSP25/submissions/lab1/L3E"

pd.options.mode.copy_on_write = True



mw = MainWindow()
mw.run()

