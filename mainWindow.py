from tkinter import *
from numpy.core.fromnumeric import size
import pandas as pd
from tkinter import ttk, filedialog

from moduls import file_open, standard_stat , chose_hist, chose_scatplot_2, chose_scatplot_3, chose_grupowanie, connection_open, cofnij, chose_filtr, chose_kolumne, zapisz
import seaborn as sns

#Podstawowe ustawienia
root = Tk()
root.title('Program do analizy baz danych')
root.attributes("-fullscreen", True)
# root.geometry("800x600")
#Tytuł wyświetlanego pliku
title_frame = Frame(root)
title_frame.pack(side=TOP)

title_label = Label(title_frame,text = '')
title_label.pack(side = LEFT)


#Miejsce do wyświetlania danych
data_frame = Frame(root,height = 100)
data_frame.pack()

#Miejsce do wyświetlania statystyk
stat_frame = Frame(root)
stat_frame.pack()


#Mejsce do wyświetlania wykresów
plot_frame = Frame(root, height = 100)
plot_frame.pack()
#plot_tabControl = ttk.Notebook(plot_frame)
tabs = []

#Dodanie Scroolbar'ów
data_tree_scrollY = Scrollbar(data_frame)
data_tree_scrollX = Scrollbar(data_frame,orient = 'horizontal')
data_tree = ttk.Treeview(data_frame, xscrollcommand = data_tree_scrollX.set, yscrollcommand = data_tree_scrollY.set)
data_tree_scrollY.config(command=data_tree.yview)
data_tree_scrollX.config(command=data_tree.xview)


#Statystyki
stat_tabControl = ttk.Notebook(stat_frame)
#Stworzenie Menu
my_menu = Menu(root)
root.config(menu=my_menu)


error_label = Label(root, text='')
error_label.pack(pady  =20)


#Stworzenie Menu "File"
file_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="Plik", menu=file_menu)
file_menu.add_command(label="Otwórz plik", command=lambda : file_open(error_label=error_label,data_tree=data_tree,tree_scrollY = data_tree_scrollY, tree_scrollX = data_tree_scrollX, title_label = title_label))
file_menu.add_command(label = "Zapisz", command = lambda : zapisz())
file_menu.add_command(label = "Cofnij", command = lambda : cofnij(data_tree = data_tree))
file_menu.add_command(label = "Wyjdź", command = lambda : root.destroy())
#Stworzenie Menu "Podstawowe statystyki"
stat_menu = Menu(my_menu, tearoff = False)
my_menu.add_cascade(label = "Statystyki", menu = stat_menu)
stat_menu.add_command(label="Podstawowe statystyki", command = lambda : standard_stat(stat_frame = stat_frame, tabControl = stat_tabControl))

#Stworzenie Menu "Wykresy"
plot_menu = Menu(my_menu, tearoff = False)
my_menu.add_cascade(label = "Wykresy", menu = plot_menu)
plot_menu.add_command(label="Histogram", command = lambda : chose_hist(tabControl = stat_tabControl) )

scat_plot_menu=Menu(plot_menu, tearoff = False)
plot_menu.add_cascade(label = "Wykres zależności", menu = scat_plot_menu)
scat_plot_menu.add_command(label="dla 2 zmiennych",command = lambda : chose_scatplot_2(tabControl = stat_tabControl))
scat_plot_menu.add_command(label="dla 3 zmiennych",command = lambda : chose_scatplot_3(tabControl = stat_tabControl))

#Stworzenie Menu "Grupowanie"
group_menu = Menu(my_menu, tearoff =  False)
my_menu.add_cascade(label = "Grupowanie", menu = group_menu)
group_menu.add_command(label = "Grupuj", command = lambda : chose_grupowanie(tabControl = stat_tabControl, stat_frame=stat_frame))

#Łączenie tabeli
laczenie_menu = Menu(my_menu, tearoff =  False)
my_menu.add_cascade(label = "Łączenie", menu = laczenie_menu)
laczenie_menu.add_command(label = "Połącz tabele", command = lambda :connection_open(data_tree= data_tree))

#Filtrowanie
filtr_menu = Menu(my_menu, tearoff =  False)
my_menu.add_cascade(label = "Filtry", menu = filtr_menu)
filtr_menu.add_command(label = "Filtrowanie", command = lambda :chose_filtr(data_tree= data_tree))

#Dodaj kolumne
kolumna_menu = Menu(my_menu, tearoff =  False)
my_menu.add_cascade(label = "Kolumny", menu = kolumna_menu)
kolumna_menu.add_command(label = "Dodaj kolumne", command = lambda :chose_kolumne(data_tree= data_tree))




root.mainloop()