import tkinter as tk
from tkinter import filedialog
import pandas as pd 


def load_file():
    file = filedialog.askopenfilename(filetypes= [("csv","*.csv")]) 
    df = pd.read_csv(file)
    print(df.head())