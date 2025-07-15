from tkinter.ttk import *
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog as fd

co1 = "#feffff" #branca
co2 = "#00a7a7" #branca

janela = Tk()
janela.title("")
janela.geometry("850x650")
janela.configure(background="white")
janela.resizable(width=FALSE, height=FALSE)

style = Style(janela)
style.theme_use("clam")

# frames
frame_logo = Frame(janela, width=850, height=52, bg=co2)
frame_logo.grid(row=0, column=0, pady=0, padx=0, sticky=NSEW)

ttk.Separator(janela, orient=HORIZONTAL).grid(row=1, columnspan=1, ipadx=680)

frame_dados = Frame(janela, width=850, height=65, bg=co1)
frame_dados.grid(row=0, column=2, pady=0, padx=0, sticky=NSEW)

ttk.Separator(janela, orient=HORIZONTAL).grid(row=3, columnspan=1, ipadx=680)

frame_detalhes = Frame(janela, width=850, height=250, bg=co1)
frame_detalhes.grid(row=4, column=0, pady=0, padx=10, sticky=NSEW)

frame_tabela = Frame(janela, width=850, height=200, bg=co1)
frame_tabela.grid(row=5, column=2, pady=0, padx=10, sticky=NSEW)

janela.mainloop()