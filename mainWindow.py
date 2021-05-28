import tkinter as tk
import pandas as pd 
import moduls

def main():
    window = tk.Tk()
    menu = tk.Menu(window)
    window.config(menu=menu)
    window.title("Aplikacja do analizy baz danych")
    window.geometry("900x750")
    file_menu = tk.Menu(menu)
    menu.add_cascade(label = "File", menu = file_menu) 
    file_menu.add_command(label= "Load",command = moduls.load_file)
    window.mainloop()


if __name__ == '__main__':
    main()