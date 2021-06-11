from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import pandas as pd 


# Funkcja otiwerająca plik
def file_open(error_label,data_tree,tree_scrollX,tree_scrollY):
	filename = filedialog.askopenfilename(
		initialdir="C:/gui/",
		title = "Open A File",
		filetype=(("csv files", "*.csv"), ("All Files", "*.*"))
		)

	if filename:
		try:
			filename = r"{}".format(filename)
			df = pd.read_csv(filename)
		except ValueError:
			error_label.config(text="Nie udało się otworzyć pliku!")
		except FileNotFoundError:
			error_label.config(text="PLik nie istnieje!")

	data_tree.delete(*data_tree.get_children())

	data_tree["column"] = list(df.columns)
	data_tree["show"] = "headings"

	for column in data_tree["column"]:
		data_tree.heading(column, text=column)


	df_rows = df.to_numpy().tolist()
	for row in df_rows:
		data_tree.insert("", "end", values=row)


	tree_scrollX.pack(side=BOTTOM, fill=X)
	tree_scrollY.pack(side=RIGHT, fill=Y)
	data_tree.pack()
