from tkinter import *
from numpy.core.fromnumeric import size
import pandas as pd
from tkinter import ttk, filedialog
from moduls import file_open, standard_stat , draw_hist, chose_scatplot_2, chose_scatplot_3, chose_grupowanie
import seaborn as sns
import plotly.io as pio

#Podstawowe ustawienia
root = Tk()
root.title('Program do analizy baz danych')
root.geometry("700x500")
#Tytuł wyświetlanego pliku
title_frame = Frame(root)
title_frame.pack(side=TOP)

title_label = Label(title_frame,text = '')
title_label.pack(side = LEFT)


#Miejsce do wyświetlania danych
data_frame = Frame(root)
data_frame.pack()

#Miejsce do wyświetlania statystyk
stat_frame = Frame(root,maxsize=300)
stat_frame.pack(side = LEFT)


#Mejsce do wyświetlania wykresów
plot_frame = Frame(root,  maxsize=300)
plot_frame.pack(side = RIGHT)
plot_tabControl = ttk.Notebook(plot_frame)
tabs = []

#Dodanie Scroolbar'ów
data_tree_scrollY = Scrollbar(data_frame)
data_tree_scrollX = Scrollbar(data_frame,orient = 'horizontal')
data_tree = ttk.Treeview(data_frame, xscrollcommand = data_tree_scrollX.set, yscrollcommand = data_tree_scrollY.set)
data_tree_scrollY.config(command=data_tree.yview)
data_tree_scrollX.config(command=data_tree.xview)


#Statystyki
stat_tree_scrollY = Scrollbar(stat_frame)
stat_tree_scrollX = Scrollbar(stat_frame,orient = 'horizontal')
stat_tree = ttk.Treeview(stat_frame, xscrollcommand = stat_tree_scrollX.set, yscrollcommand = stat_tree_scrollY.set)
stat_tree_scrollY.config(command=stat_tree.yview)
stat_tree_scrollX.config(command=stat_tree.xview)
stat_tabControl = ttk.Notebook(stat_frame)
#Stworzenie Menu
my_menu = Menu(root)
root.config(menu=my_menu)


error_label = Label(root, text='')
error_label.pack(pady  =20)


#Stworzenie Menu "File"
file_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="PLik", menu=file_menu)
file_menu.add_command(label="Otwórz plik", command=lambda : file_open(error_label=error_label,data_tree=data_tree,tree_scrollY = data_tree_scrollY, tree_scrollX = data_tree_scrollX, title_label = title_label))

#Stworzenie Menu "Podstawowe statystyki"
stat_menu = Menu(my_menu, tearoff = False)
my_menu.add_cascade(label = "Statystyki", menu = stat_menu)
stat_menu.add_command(label="Podstawowe statystyki", command = lambda : standard_stat(stat_tree = stat_tree,tree_scrollY = stat_tree_scrollY, tree_scrollX = stat_tree_scrollX, tabControl = stat_tabControl))

#Stworzenie Menu "Wykresy"
plot_menu = Menu(my_menu, tearoff = False)
my_menu.add_cascade(label = "Wykresy", menu = plot_menu)
plot_menu.add_command(label="Histogram", command = lambda : draw_hist(tabControl = plot_tabControl) )

scat_plot_menu=Menu(plot_menu, tearoff = False)
plot_menu.add_cascade(label = "Wykres zależności", menu = scat_plot_menu)
scat_plot_menu.add_command(label="dla 2 zmiennych",command = lambda : chose_scatplot_2(tabControl = plot_tabControl))
scat_plot_menu.add_command(label="dla 3 zmiennych",command = lambda : chose_scatplot_3(tabControl = plot_tabControl))

#Stworzenie Menu "Grupowanie"
group_menu = Menu(my_menu, tearoff =  False)
my_menu.add_cascade(label = "Grupowanie", menu = group_menu)
group_menu.add_command(label = "Grupuj", command = lambda : chose_grupowanie(tabControl = stat_tabControl))







root.mainloop()