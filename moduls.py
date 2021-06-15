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
# import plotly.express as px
# from tkinter import simpledialog
from mpl_toolkits.mplot3d import Axes3D
# import matplotlib.pyplot as plt


df = pd.DataFrame()
df_list = []

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
			error_label.config(text="Plik nie istnieje!")

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



def standard_stat(stat_frame, tabControl):
	global df
	tab = ttk.Frame(tabControl, height = 100)
	stat_tree_scrollY = Scrollbar(tab)
	stat_tree_scrollX = Scrollbar(tab,orient = 'horizontal')
	stat_tree = ttk.Treeview(tab, xscrollcommand = stat_tree_scrollX.set, yscrollcommand = stat_tree_scrollY.set)
	stat_tree_scrollY.config(command=stat_tree.yview)
	stat_tree_scrollX.config(command=stat_tree.xview)

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
	

		stat_tree_scrollX.pack(side=BOTTOM, fill=X)
		stat_tree_scrollY.pack(side=RIGHT, fill=Y)
		stat_tree.pack()
		tabControl.add(tab, text = "Podstawowe statystyki")
		tabControl.pack()



def draw_hist(tabControl,window, var):
	global df
	window.destroy()
	tab = ttk.Frame(tabControl)
	figure = Figure(figsize=(10, 10))
	ax = figure.subplots()
	hist = sns.histplot(df[var], ax = ax)
	canvas = FigureCanvasTkAgg(figure, master=tab)
	canvas.draw()
	canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
	tabControl.add(tab, text = var)
	tabControl.pack()


def chose_hist(tabControl):
	global df
	if df.empty:
		messagebox.showerror("Brak Danych", "Brakuje do analizy!")
	else:
		window = Toplevel()
		value = []
		for column in list(df.columns):
			value.append(column)
		label_1 = Label(window, text ="Wybierz zmienną dla której ma zostać wygenerowany histpgram" )
		label_1.pack()
		Lista_1 = ttk.Combobox(window, values = value)
		Lista_1.pack()
		button = Button(window,  text = "Ok", command= lambda: draw_hist(tabControl= tabControl,var = Lista_1.get(), window = window))
		button.pack()


def draw_scatplot_2(tabControl,var_1,var_2,window):
	global df
	tab = ttk.Frame(tabControl, height = 100)
	figure = Figure(figsize=(6, 6))
	ax = figure.subplots()
	scat = sns.scatterplot(data = df, x = var_1, y = var_2, ax = ax)
	ax.set_title("Wykres Zależności")
	canvas = FigureCanvasTkAgg(figure, master=tab)
	canvas.draw()
	canvas.get_tk_widget().pack()
	tabControl.add(tab, text = "Scatter " + var_1 + "x" + var_2)
	tabControl.pack()
	window.destroy()


def draw_scatplot_3(tabControl,var_1,var_2,var_3,window):
	global df
	tab = ttk.Frame(tabControl, height = 100)
	figure = Figure(figsize=(5, 4), dpi=100)
	ax = figure.add_subplot(111, projection="3d")
	ax.scatter(df[var_1], df[var_2], df[var_3])

	ax.set_title("Wykres zależności")
	ax.set_xlabel(var_1)
	ax.set_ylabel(var_2)
	ax.set_zlabel(var_3)

	canvas = FigureCanvasTkAgg(figure, master=tab)
	canvas.draw()
	canvas.get_tk_widget().pack()
	toolbar = NavigationToolbar2Tk(canvas, tab)
	tabControl.add(tab, text = "Catter "+ var_1 +"x" + var_2 + "x" + var_3)
	tabControl.pack()
	toolbar.update()
	window.destroy()

	

def chose_scatplot_2(tabControl):
	global df
	if df.empty:
		messagebox.showerror("Brak Danych", "Brakuje do analizy!")
	else:
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
	if df.empty:
		messagebox.showerror("Brak Danych", "Brakuje do analizy!")
	else:
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


def grupowanie(stat_frame,tabControl,var_wyswietlana, var_grupowana, window):
	global df
	tab = ttk.Frame(tabControl, height = 100)
	stat_tree_scrollY = Scrollbar(tab)
	stat_tree_scrollX = Scrollbar(tab,orient = 'horizontal')
	stat_tree = ttk.Treeview(tab, xscrollcommand = stat_tree_scrollX.set, yscrollcommand = stat_tree_scrollY.set)
	stat_tree_scrollY.config(command=stat_tree.yview)
	stat_tree_scrollX.config(command=stat_tree.xview)
	
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
	tabControl.pack()
	window.destroy()
	stat_tree_scrollX.pack(side=BOTTOM, fill=X)
	stat_tree_scrollY.pack(side=RIGHT, fill=Y)

def chose_wyswietlana(stat_frame,var_1,window,tabControl):
	window.destroy()
	global df
	window = Toplevel()
	value = []
	for column in list(df.columns):
		value.append(column)
	value.remove(var_1)
	label_1 = Label(window, text ="Wybierz zmienną której podsumowanie chcesz wyświetlić" )
	label_1.pack()
	Lista_1 = ttk.Combobox(window, values = value)
	Lista_1.pack()
	button = Button(window,  text = "Ok", command= lambda: grupowanie(stat_frame = stat_frame,tabControl= tabControl,var_wyswietlana = Lista_1.get(),var_grupowana = var_1, window = window))
	button.pack()


def sprawdz(stat_frame,var_1, window, tabControl):
	global df
	x = df[var_1].unique().size
	if x <= 10:
		chose_wyswietlana(stat_frame = stat_frame,var_1 = var_1, window = window, tabControl = tabControl)
	else:
		messagebox.showerror("Zbyt duża liczba grup", "Zbyt duża liczba grup (max : 10)")
		window.destroy()


def chose_grupowanie(tabControl,stat_frame):
	global df
	if df.empty:
		messagebox.showerror("Brak Danych", "Brakuje do analizy!")
	else:
		window = Toplevel()
		value = []
		for column in list(df.columns):
			value.append(column)
		label_1 = Label(window, text ="Wybierz zmienną do grupowania" )
		label_1.pack()
		Lista_1 = ttk.Combobox(window, values = value)
		Lista_1.pack()
		button = Button(window,  text = "Ok", command = lambda : sprawdz(var_1 = Lista_1.get(), window = window, tabControl= tabControl, stat_frame= stat_frame))
		button.pack()


def connection_open(data_tree):
	global df
	
	if df.empty:
		messagebox.showerror("Brak Danych", "Brakuje do analizy!")
	else:
		filename = filedialog.askopenfilename(
			initialdir="C:/gui/",
			title = "Open A File",
			filetype=(("csv files", "*.csv"), ("All Files", "*.*"))
			)

		if filename:
			try:
				filename = r"{}".format(filename)
				df_connect = pd.read_csv(filename)
			except ValueError:
				error_label.config(text="Nie udało się otworzyć pliku!")
			except FileNotFoundError:
				error_label.config(text="PLik nie istnieje!")


			window = Toplevel()
			value_1 = []
			value_2 = []
			for column in list(df.columns):
					value_1.append(column)
			for column in list(df_connect.columns):
				value_2.append(column)
			
			label_1 = Label(window, text ="Wybierz kolumnę tabeli podstawowej do dokonania złączenia" )
			label_1.pack()
			Lista_1 = ttk.Combobox(window, values = value_1)
			Lista_1.pack()

			label_2 = Label(window, text ="Wybierz kolumnę tabeli wczytanej do dokonania złączenia" )
			label_2.pack()
			Lista_2 = ttk.Combobox(window, values = value_2)
			Lista_2.pack()

			button = Button(window,  text = "Ok", command = lambda : connecting(var_1 = Lista_1.get(), var_2 = Lista_2.get(), window = window, df_connect =df_connect, data_tree = data_tree))
			button.pack()


def connecting(var_1, var_2, window, df_connect, data_tree):
	global df
	global df_list
	window.destroy()
	df_list.append(df)

	df = pd.merge(df,df_connect, left_on = var_1, right_on = var_2)

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


def cofnij(data_tree):
	global df
	global df_list
	if not len(df_list):
		messagebox.showerror("Brak porzednich stanów tabeli", "Brak porzednich stanów tabeli!")
	else:
		df = df_list[-1]
		df_list.pop(-1)
		data_tree.delete(*data_tree.get_children())

	data_tree["column"] = list(df.columns)
	data_tree["show"] = "headings"

	for column in data_tree["column"]:
		data_tree.heading(column, text=column)


	df_rows = df.to_numpy().tolist()
	for row in df_rows:
		data_tree.insert("", "end", values=row)


	data_tree.pack()


def chose_filtr(data_tree):
	global df
	if df.empty:
		messagebox.showerror("Brak wczytanych danych", "Brak wczytanych danych!")
	else:
		window = Toplevel()
		value = []
		for column in list(df.columns):
			value.append(column)

		label_1 = Label(window, text ="Wybierz zmienną na której ma zadziałać filtr" )
		label_1.pack()
		Lista_1 = ttk.Combobox(window, values = value)
		Lista_1.pack()
		label_2=Label(window,text="Filtrowana wartość")
		label_2.pack()
		entry = Text(window, width = 10, height = 1)
		entry.pack()
		button = Button(window,  text = "Ok", command = lambda : filtrowanie(var = Lista_1.get(), val = entry.get("1.0","end-1c"), window = window,data_tree = data_tree))
		button.pack()

def filtrowanie(var, val, window, data_tree):
	global df_list
	global df
	window.destroy()
	df_list.append(df)
	
	try:
		df = df[df[var] == int(val)]
	except:
		df = df[df[var] == val]
	data_tree.delete(*data_tree.get_children())

	data_tree["column"] = list(df.columns)
	data_tree["show"] = "headings"

	for column in data_tree["column"]:
		data_tree.heading(column, text=column)


	df_rows = df.to_numpy().tolist()
	for row in df_rows:
		data_tree.insert("", "end", values=row)

	data_tree.pack()


def chose_kolumne(data_tree):
	global df
	if df.empty:
		messagebox.showerror("Brak wczytanych danych", "Brak wczytanych danych!")
	else:
		dzialania = ["+","-","*"]
		typy = ["Integer", "Float"]
		window = Toplevel()
		value = []
		for column in list(df.columns):
			value.append(column)

		label_7 = Label(window, text ="Wybierz nazwę nowej kolumny")
		label_7.pack()
		entry_7 = Text(window,width = 10, height = 1)
		entry_7.pack()

		label_1 = Label(window, text ="Wybierz skalar do pierwszej zmmiennej" )
		label_1.pack()
		entry_1 = Text(window,width = 10, height = 1)
		entry_1.pack()

		label_2 = Label(window, text ="Wybierz pierwszą zmienną" )
		label_2.pack()
		Lista_1 = ttk.Combobox(window, values = value)
		Lista_1.pack()

		label_3 = Label(window, text ="Wybierz działanie" )
		label_3.pack()
		Lista_3 = ttk.Combobox(window, values = dzialania)
		Lista_3.pack()

		label_4 = Label(window, text ="Wybierz skalar do drugiej zmmiennej")
		label_4.pack()
		entry_4 = Text(window,width = 10, height = 1)
		entry_4.pack()

		label_5 = Label(window, text ="Wybierz drugą zmienną" )
		label_5.pack()
		Lista_5 = ttk.Combobox(window, values = value)
		Lista_5.pack()

		label_6 = Label(window, text ="Wybierz wyraz wolny")
		label_6.pack()
		entry_6 = Text(window,width = 10, height = 1)
		entry_6.pack()

		label_8 = Label(window, text ="Wybierz typ kolumny" )
		label_8.pack()
		Lista_8 = ttk.Combobox(window, values = typy)
		Lista_8.pack()

		button = Button(window,  text = "Ok", command = lambda : dodaj_kolumne(tytul =entry_7.get("1.0","end-1c"),
		skalar_1 = entry_1.get("1.0","end-1c"), zmienna_1 = Lista_1.get(), dzialania = Lista_3.get(), skalar_2 = entry_4.get("1.0","end-1c"),
		zmienna_2 = Lista_5.get(), wyraz_wolny = entry_6.get("1.0","end-1c"),typy = Lista_8.get(),
		window = window, data_tree = data_tree))
		button.pack()


def dodaj_kolumne(tytul, skalar_1, zmienna_1, dzialania, skalar_2, zmienna_2, wyraz_wolny, typy, window, data_tree):
	global df
	global df_list
	window.destroy()
	df_list.append(df)

	if typy == "Float":
		df[tytul] = df.apply(
		lambda x:
		x[zmienna_1] * float(skalar_1) + x[zmienna_2] * float(skalar_2) + float(wyraz_wolny) if dzialania =="+" else 
		x[zmienna_1] * float(skalar_1) - x[zmienna_2] * float(skalar_2) + float(wyraz_wolny) if dzialania =="-" else 
		x[zmienna_1] * float(skalar_1) * x[zmienna_2] * float(skalar_2) + float(wyraz_wolny) if dzialania =="*" else 
		np.nan, axis = 1)
	elif typy == "Integer":
		df[tytul] = df.apply(
		lambda x:
		round(x[zmienna_1] * float(skalar_1) + x[zmienna_2] * float(skalar_2) + float(wyraz_wolny),0) if dzialania =="+" else 
		round(x[zmienna_1] * float(skalar_1) - x[zmienna_2] * float(skalar_2) + float(wyraz_wolny),0) if dzialania =="-" else 
		round(x[zmienna_1] * float(skalar_1) * x[zmienna_2] * float(skalar_2) + float(wyraz_wolny),0) if dzialania =="*" else	
		np.nan, axis = 1)
	data_tree.delete(*data_tree.get_children())

	data_tree["column"] = list(df.columns)
	data_tree["show"] = "headings"

	for column in data_tree["column"]:
		data_tree.heading(column, text=column)


	df_rows = df.to_numpy().tolist()
	for row in df_rows:
		data_tree.insert("", "end", values=row)

	data_tree.pack()


def zapisz():
	global df
	if df.empty:
		messagebox.showerror("Brak danych do zapisu", "Brak danych do zapisu!")
	else:
		filename = filedialog.asksaveasfilename(
			initialdir="C:/gui/",
			title = "Save A File",
			filetype=(("csv files", "*.csv"), ("All Files", "*.*")))
		if filename:
			try:
				filename = r"{}".format(filename)
				df.to_csv(filename, index = False)
			except ValueError:
				error_label.config(text="Nie udało się zapisać pliku!")
			except FileNotFoundError:
				error_label.config(text="Plik nie istnieje!")