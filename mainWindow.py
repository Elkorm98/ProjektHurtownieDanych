from tkinter import *
from numpy.core.fromnumeric import size
import pandas as pd
from tkinter import ttk, filedialog
from moduls import file_open

#Podstawowe ustawienia
root = Tk()
root.title('Program do analizy baz danych')
root.geometry("700x500")
#
title_label = Label(root,width="70", height= "1",text = '')
title_label.pack(padx=20)


#Miejsce do wyświetlania danych
data_frame = Frame(root)
data_frame.pack(pady=20)


#Dodanie Scroolbar'ów
tree_scrollY = Scrollbar(data_frame)
tree_scrollX = Scrollbar(data_frame,orient = 'horizontal')
data_tree = ttk.Treeview(data_frame,xscrollcommand = tree_scrollX.set, yscrollcommand = tree_scrollY.set)
tree_scrollY.config(command=data_tree.yview)
tree_scrollX.config(command=data_tree.xview)


#Stworzenie Menu
my_menu = Menu(root)
root.config(menu=my_menu)


error_label = Label(root, text='')
error_label.pack(pady  =20)


#Stworzenie Menu "File"
file_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open", command=lambda : file_open(error_label=error_label,data_tree=data_tree,tree_scrollY = tree_scrollY, tree_scrollX = tree_scrollX, title_label = title_label,s=s))











root.mainloop()