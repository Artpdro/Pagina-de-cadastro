import sqlite3
from tkinter.ttk import *
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog as fd
from PIL import ImageTk, Image

#banco de dados

from view import *

#-------------------------------------------------

co0 = "#000000" #preta
co1 = "#feffff" #branca
co2 = "#5ab5d9" #azul
co3 = "#38c15d" #vermelho
co4 = "#da1111" #verde
co5 = "#9b9b9b"

janela = Tk()
janela.title("")
janela.geometry("850x650")
janela.configure(background="white")
janela.resizable(width=FALSE, height=FALSE)

style = Style(janela)
style.theme_use("clam")

# frames
frame_logo = Frame(janela, width=850, height=50, bg=co2)
frame_logo.grid(row=0, column=0, pady=0, padx=0, sticky=NSEW)
 
ttk.Separator(janela, orient=HORIZONTAL).grid(row=1, columnspan=1, ipadx=680)

frame_dados = Frame(janela, width=850, height=65, bg=co1)
frame_dados.grid(row=2, column=0, pady=0, padx=0, sticky=NSEW)

ttk.Separator(janela, orient=HORIZONTAL).grid(row=3, columnspan=1, ipadx=680)

frame_detalhes = Frame(janela, width=850, height=250, bg=co1)
frame_detalhes.grid(row=4, column=0, pady=0, padx=10, sticky=NSEW)

frame_tabela = Frame(janela, width=850, height=200, bg=co1)
frame_tabela.grid(row=5, column=0, pady=0, padx=10, sticky=NSEW)

app_lg = Image.open('logo.png')
app_lg = app_lg.resize((132,48  ))
app_lg = ImageTk.PhotoImage(app_lg)
app_logo = Label(frame_logo, image=app_lg, text="Cadastro de contadores", width=850, compound=LEFT, relief=RAISED, anchor=NW, font=('Ivy 20 bold'), bg= co2, fg=co1)
app_logo.place(x=0, y=0)

#---- cadastro 

def cadastro():
    frame_tabela_contadores = Frame(frame_tabela, width=830, height=200, bg=co5)
    frame_tabela_contadores.grid(row=0, column=0, pady=0, padx=0, sticky=NSEW)

    l_cnpj = Label(frame_detalhes, text="CNPJ *", height=1, anchor=NW, font=('Ivy 10 bold'), bg=co1, fg=co0)
    l_cnpj.place(x=4, y=10)
    e_cnpj = Entry(frame_detalhes, width=35, justify='left', relief='solid')
    e_cnpj.place(x=7, y=40)

    l_municipio = Label(frame_detalhes, text="Municipio *", height=1, anchor=NW, font=('Ivy 10 bold'), bg=co1, fg=co0)
    l_municipio.place(x=320, y=10)
    e_municipio = Entry(frame_detalhes, width=35, justify='left', relief='solid')
    e_municipio.place(x=323, y=40)

    l_empresa = Label(frame_detalhes, text="Razão social *", height=1, anchor=NW, font=('Ivy 10 bold'), bg=co1, fg=co0)
    l_empresa.place(x=4, y=70)
    e_empresa = Entry(frame_detalhes, width=35, justify='left', relief='solid')
    e_empresa.place(x=7, y=100)

    l_nome = Label(frame_detalhes, text="Nome fantasia *", height=1, anchor=NW, font=('Ivy 10 bold'), bg=co1, fg=co0)
    l_nome.place(x=320, y=70)
    e_nome = Entry(frame_detalhes, width=35, justify='left', relief='solid')
    e_nome.place(x=323, y=100)

    l_contador = Label(frame_detalhes, text="Contador *", height=1, anchor=NW, font=('Ivy 10 bold'), bg=co1, fg=co0)    
    l_contador.place(x=4, y=130)
    e_contador = Entry(frame_detalhes, width=35, justify='left', relief='solid')
    e_contador.place(x=7, y=160)

    l_tel_contador = Label(frame_detalhes, text="Telefone contador *", height=1, anchor=NW, font=('Ivy 10 bold'), bg=co1, fg=co0)    
    l_tel_contador.place(x=320, y=130)
    e_tel_contador = Entry(frame_detalhes, width=35, justify='left', relief='solid')
    e_tel_contador.place(x=323, y=160)


# tabela dados

    def mostrar_dados():
        app_nome = Label(frame_tabela_contadores, text="Dados", height=1, pady=0, padx=5, relief="flat", anchor=NW, font=('Ivy 15 bold'), bg=co5, fg=co2)
        app_nome.grid(row=0, column=0, padx=5, pady=5, sticky=W)

        list_header = ['CNPJ', 'Razão social', 'Nome fantasia', 'Municipio', 'Contador', 'Telefone contador']
        df_list = ver_dados()

        global tree_dados

        tree_dados = ttk.Treeview(frame_tabela_contadores, selectmode="extended", columns=list_header, show="headings")
        vsb = ttk.Scrollbar(frame_tabela_contadores, orient="vertical", command=tree_dados.yview)
        hsb = ttk.Scrollbar(frame_tabela_contadores, orient="horizontal", command=tree_dados.xview)

        tree_dados.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        tree_dados.grid(row=1, column=0, sticky='nsew')
        vsb.grid(row=1, column=1, sticky='ns')
        hsb.grid(row=2, column=0, sticky='ew')

        frame_tabela_contadores.grid_rowconfigure(1, weight=1)
        frame_tabela_contadores.grid_columnconfigure(0, weight=1)

        hd = ["nw", "nw", "nw", "nw", "nw", "nw"]
        h = [120, 150, 150, 140, 100, 150]
        n = 0

        for col in list_header:
            tree_dados.heading(col, text=col.title(), anchor=NW)
            tree_dados.column(col, width=h[n], anchor=hd[n])
            n += 1

        for item in df_list:
            tree_dados.insert('', 'end', values=item)

        #função novo cadastro

    def novo_cadastro():
        cnpj = e_cnpj.get()
        razao_social = e_empresa.get()
        nome_fantasia = e_nome.get()
        municipio = e_municipio.get()
        contador = e_contador.get()
        tel_contador = e_tel_contador.get()
        
        lista = [cnpj, razao_social, nome_fantasia, municipio, contador, tel_contador]

        for i in lista:
            if i == "":
                messagebox.showerror('Error', 'Preencha todos os campos')
                return
            
        criar_contador(lista)

        messagebox.showinfo('Sucesso' , 'Os dados foram enseridos com sucesso')

        e_cnpj.delete(0,END)
        e_empresa.delete(0,END)
        e_nome.delete(0,END)
        e_municipio.delete(0,END)
        e_contador.delete(0,END)
        e_tel_contador.delete(0,END)

        mostrar_dados()

    #função atualizar cadastro

    


    botao_carregar = Button(frame_detalhes, command=novo_cadastro, anchor=CENTER, text='Salvar'.upper(), width=10, overrelief=RIDGE, font=('Ivy 7 bold'), bg=co3, fg=co1)
    botao_carregar.place(x=7, y=200)

    botao_deletar = Button(frame_detalhes, anchor=CENTER, text='Deletar'.upper(), width=10, overrelief=RIDGE, font=('Ivy 7 bold'), bg=co4, fg=co1)
    botao_deletar.place(x=87, y=200)

    botao_atualizar = Button(frame_detalhes, anchor=CENTER, text='Atualizar'.upper(), width=10, overrelief=RIDGE, font=('Ivy 7 bold'), bg=co2, fg=co1)
    botao_atualizar.place(x=167, y=200)


    mostrar_dados()

#----- salvar

def salvar():
    print('Salvar')
    

#---- controle

def control(i):
    if i == 'cadastro':
        for widget in frame_detalhes.winfo_children():
            widget.destroy()

        for widget in frame_tabela.winfo_children():
            widget.destroy()

        cadastro()    
 

    if i == 'salvar':
        for widget in frame_detalhes.winfo_children():
            widget.destroy()

        for widget in frame_tabela.winfo_children():
            widget.destroy()

        salvar()    
    

# ------botoes

app_image_cadastro = Image.open('add.png')
app_image_cadastro = app_image_cadastro.resize((18,18))
app_image_cadastro = ImageTk.PhotoImage(app_image_cadastro)
app_cadastro = Button(frame_dados, command=lambda:control('cadastro'), image=app_image_cadastro, text="Adicionar", width=100, compound=LEFT,  overrelief=RIDGE, font=('Ivy 11'), bg= co1, fg=co0)
app_cadastro.place(x=10, y=30)

add_image_salvar = Image.open('salvar.png') 
add_image_salvar = add_image_salvar.resize((18,18))
add_image_salvar = ImageTk.PhotoImage(add_image_salvar)
app_salvar = Button(frame_dados, command=lambda:control('salvar'), image=add_image_salvar, text="Salvar", width=100, compound=LEFT,  overrelief=RIDGE, font=('Ivy 11'), bg= co1, fg=co0)
app_salvar.place(x=150, y=30)


janela.mainloop()