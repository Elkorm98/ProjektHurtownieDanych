from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
import pandas as pd 
import os
import seaborn as sns
from matplotlib.backend_bases import key_press_handler
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import plotly.express as px
from tkinter import simpledialog
import plotly.io as pio
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt


df = pd.DataFrame()
# Funkcja otiwerająca plik
def file_open(error_label, data_tree, tree_scrollX, tree_scrollY, title_label):
	'''
	Ta funkcja otwiera plik 
	'''
	global df
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
	title_label.config(text = os.path.basename(filename))
	data_tree.pack()



def standard_stat(stat_tree,tree_scrollX, tree_scrollY, tabControl):
	global df
	if df.empty:
		messagebox.showerror("Brak Danych", "Brakuje do analizy!")
	else:
		d = df.describe()
		d.insert(0,"Podstawowe statystyki",d.index,True)
		stat_tree.delete(*stat_tree.get_children())

		stat_tree["column"] = list(d.columns)

		stat_tree["show"] = "headings"
		for column in stat_tree["column"]:
			stat_tree.heading(column, text=column)

		d_rows = d.to_numpy().tolist()

		for row in d_rows:
			stat_tree.insert("", "end", values=row)
		

		tree_scrollX.pack(side=BOTTOM, fill=X)
		tree_scrollY.pack(side=RIGHT, fill=Y)
		stat_tree.pack()
		tabControl.add(stat_tree, text = "Podstawowe statystyki")
		tabControl.pack(expand = 1, fill ="both")



def draw_hist(tabControl):
	global df
	if df.empty:
		messagebox.showerror("Brak Danych", "Brakuje do analizy!")
	else:
		for i in df.columns:
			tab = ttk.Frame(tabControl)
			figure = Figure(figsize=(6, 6))
			ax = figure.subplots()
			hist = sns.histplot(df[i],ax = ax)
			canvas = FigureCanvasTkAgg(figure, master=tab)
			canvas.draw()
			canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
			tabControl.add(tab, text = i)
			tabControl.pack(expand = 1, fill ="both")


def draw_scatplot_2(tabControl,var_1,var_2,window):
	global df
	tab = ttk.Frame(tabControl)
	figure = Figure(figsize=(6, 6))
	ax = figure.subplots()
	scat = sns.scatterplot(data = df, x = var_1, y = var_2, ax = ax)
	canvas = FigureCanvasTkAgg(figure, master=tab)
	canvas.draw()
	canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
	tabControl.add(tab, text = "New Scater")
	tabControl.pack(expand = 1, fill ="both")
	window.destroy()


def draw_scatplot_3(tabControl,var_1,var_2,var_3,window):
	global df
	tab = ttk.Frame(tabControl)
	figure = Figure(figsize=(5, 4), dpi=100)
	ax = figure.add_subplot(111, projection="3d")
	ax.scatter(df[var_1], df[var_2], df[var_3])
	
	canvas = FigureCanvasTkAgg(figure, master=tab)
	canvas.draw()
	canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
	toolbar = NavigationToolbar2Tk(canvas, tab)
	tabControl.add(tab, text = "New Scater")
	tabControl.pack(expand = 1, fill ="both")
	toolbar.update()
	window.destroy()

	

def chose_scatplot_2(tabControl):
	global df
	window = Toplevel()
	value = []
	for column in list(df.columns):
		value.append(column)
	label_1 = Label(window, text ="Wybierz pierwszą zmienną" )
	label_1.pack()
	Lista_1 = ttk.Combobox(window, values = value)
	Lista_1.pack()
	label_2 = Label(window, text ="Wybierz drugą zmienną" )
	label_2.pack()
	Lista_2 = ttk.Combobox(window, values = value)
	Lista_2.pack()
	button = Button(window,  text= "Ok", command= lambda: draw_scatplot_2(tabControl= tabControl,var_1 = Lista_1.get(), var_2 = Lista_2.get(),window = window))
	button.pack()


def chose_scatplot_3(tabControl):
	global df
	window = Toplevel()
	value = []
	for column in list(df.columns):
		value.append(column)
	label_1 = Label(window, text ="Wybierz pierwszą zmienną" )
	label_1.pack()
	Lista_1 = ttk.Combobox(window, values = value)
	Lista_1.pack()
	label_2 = Label(window, text ="Wybierz drugą zmienną" )
	label_2.pack()
	Lista_2 = ttk.Combobox(window, values = value)
	Lista_2.pack()
	label_3 = Label(window, text ="Wybierz trzecią zmienną" )
	label_3.pack()
	Lista_3 = ttk.Combobox(window, values = value)
	Lista_3.pack()
	button = Button(window,  text= "Ok", command= lambda: draw_scatplot_3(tabControl= tabControl,var_1 = Lista_1.get(), var_2 = Lista_2.get(), var_3 = Lista_3.get(),window = window))
	button.pack()


def grupowanie(tabControl,var_wyswietlana, var_grupowana, window):
	global df
	tab = ttk.Frame(tabControl)
	stat_tree = ttk.Treeview(tab)
	d = df.groupby(var_grupowana).describe()[var_wyswietlana]
	d.insert(0,"Grupa",d.index,True)
	stat_tree.delete(*stat_tree.get_children())

	stat_tree["column"] = list(d.columns)

	stat_tree["show"] = "headings"
	for column in stat_tree["column"]:
		stat_tree.heading(column, text=column)

	d_rows = d.to_numpy().tolist()

	for row in d_rows:
		stat_tree.insert("", "end", values=row)
	stat_tree.pack()
	tabControl.add(tab, text = var_grupowana + " x " + var_wyswietlana)
	tabControl.pack(expand = 1, fill ="both")
	window.destroy()


def chose_wyswietlana(var_1,window,tabControl):
	window.destroy()
	global df
	window = Toplevel()
	value = []
	for column in list(df.columns):
		value.append(column)
	value.remove(var_1)
	label_1 = Label(window, text ="Wybierz zmienną do grupowania" )
	label_1.pack()
	Lista_1 = ttk.Combobox(window, values = value)
	Lista_1.pack()
	button = Button(window,  text = "Ok", command= lambda: grupowanie(tabControl= tabControl,var_wyswietlana = Lista_1.get(),var_grupowana = var_1, window = window))
	button.pack()


def sprawdz(var_1, window, tabControl):
	global df
	x = df[var_1].unique().size
	if x <= 10:
		chose_wyswietlana(var_1 = var_1, window = window, tabControl = tabControl)
	else:
		messagebox.showerror("Zbyt duża liczba grup", "Zbyt duża liczba grup (max : 10)")
		window.destroy()


def chose_grupowanie(tabControl):
	global df
	window = Toplevel()
	value = []
	for column in list(df.columns):
		value.append(column)
	label_1 = Label(window, text ="Wybierz zmienną do grupowania" )
	label_1.pack()
	Lista_1 = ttk.Combobox(window, values = value)
	Lista_1.pack()
	button = Button(window,  text = "Ok", command = lambda : sprawdz(var_1 = Lista_1.get(), window = window, tabControl= tabControl))
	button.pack()