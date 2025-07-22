import sqlite3
from tkinter.ttk import *
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog as fd
from PIL import ImageTk, Image
import requests
import json

#banco de dados
from view import *

#-------------------------------------------------
# Paleta de cores moderna e profissional
co0 = "#2C3E50"  # Azul escuro
co1 = "#FFFFFF"  # Branco
co2 = "#3498DB"  # Azul moderno
co3 = "#27AE60"  # Verde sucesso
co4 = "#E74C3C"  # Vermelho erro
co5 = "#ECF0F1"  # Cinza claro
co6 = "#34495E"  # Cinza escuro
co7 = "#F39C12"  # Laranja
co8 = "#9B59B6"  # Roxo
co9 = "#1ABC9C"  # Verde agua

janela = Tk()
janela.title("Sistema Avancado de Cadastro - REPIS e Contadores")
janela.geometry("1200x800")
janela.configure(background=co5)
janela.resizable(width=FALSE, height=FALSE)

# Configuracao de estilo moderno
style = Style(janela)
style.theme_use("clam")

# Configuracoes de estilo personalizadas
style.configure("Modern.TLabel", font=('Segoe UI', 12), background=co1, foreground=co0)
style.configure("Title.TLabel", font=('Segoe UI', 18, 'bold'), background=co2, foreground=co1)
style.configure("Heading.TLabel", font=('Segoe UI', 14, 'bold'), background=co5, foreground=co0)

# frames principais com design moderno
frame_header = Frame(janela, width=1200, height=80, bg=co2)
frame_header.grid(row=0, column=0, pady=0, padx=0, sticky=NSEW)
frame_header.grid_propagate(False)

# Separador com gradiente visual
separator1 = Frame(janela, width=1200, height=3, bg=co6)
separator1.grid(row=1, column=0, pady=0, padx=0, sticky=NSEW)

frame_navigation = Frame(janela, width=1200, height=80, bg=co1)
frame_navigation.grid(row=2, column=0, pady=0, padx=0, sticky=NSEW)
frame_navigation.grid_propagate(False)

separator2 = Frame(janela, width=1200, height=2, bg=co5)
separator2.grid(row=3, column=0, pady=0, padx=0, sticky=NSEW)

frame_content = Frame(janela, width=1200, height=350, bg=co1)
frame_content.grid(row=4, column=0, pady=10, padx=20, sticky=NSEW)

frame_data_display = Frame(janela, width=1200, height=280, bg=co1)
frame_data_display.grid(row=5, column=0, pady=0, padx=20, sticky=NSEW)

# Header com logo e titulo estilizado
try:
    app_lg = Image.open('logo.png')
    app_lg = app_lg.resize((60, 60))
    app_lg = ImageTk.PhotoImage(app_lg)
    logo_label = Label(frame_header, image=app_lg, bg=co2)
    logo_label.place(x=20, y=10)
except:
    pass

title_label = Label(frame_header, text="Sistema Avancado de Cadastro", 
                   font=('Segoe UI', 22, 'bold'), bg=co2, fg=co1)
title_label.place(x=100, y=15)

# Variavel para controlar a aba ativa
aba_ativa = StringVar()
aba_ativa.set("repis")

def atualizar_navegacao():
    # Limpar navegacao
    for widget in frame_navigation.winfo_children():
        widget.destroy()
    
    # Criar botoes de navegacao modernos
    nav_frame = Frame(frame_navigation, bg=co1)
    nav_frame.pack(expand=True)
    
    def criar_botao_nav(text, command, ativo=False):
        bg_color = co2 if ativo else co5
        fg_color = co1 if ativo else co0
        btn = Button(nav_frame, text=text, command=command,
                    font=('Segoe UI', 12, 'bold'), bg=bg_color, fg=fg_color,
                    relief='flat', cursor='hand2', width=15, pady=10,
                    activebackground=co2, activeforeground=co1)
        return btn
    
    btn_repis = criar_botao_nav("REPIS", lambda: control('repis'), aba_ativa.get() == "repis")
    btn_repis.pack(side=LEFT, padx=10, pady=20)
    
    btn_contador = criar_botao_nav("Contador", lambda: control('contador'), aba_ativa.get() == "contador")
    btn_contador.pack(side=LEFT, padx=10, pady=20)
    
    btn_salvar = criar_botao_nav("Exportar", lambda: control('salvar'), aba_ativa.get() == "salvar")
    btn_salvar.pack(side=LEFT, padx=10, pady=20)

def criar_botao_moderno(parent, text, command, bg_color, width=12):
    btn = Button(parent, text=text, command=command,
                font=('Segoe UI', 10, 'bold'), bg=bg_color, fg=co1, 
                relief='flat', cursor='hand2', width=width, pady=8,
                activebackground=bg_color, activeforeground=co1)
    return btn

#---- REPIS com design moderno
def repis():
    # Limpar frames
    for widget in frame_content.winfo_children():
        widget.destroy()
    for widget in frame_data_display.winfo_children():
        widget.destroy()
    
    aba_ativa.set("repis")
    atualizar_navegacao()
    
    # Container principal
    main_container = Frame(frame_content, bg=co1, relief="solid", bd=1)
    main_container.pack(fill=BOTH, expand=True, padx=10, pady=10)
    
    # Titulo da secao
    title_frame = Frame(main_container, bg=co2, height=50)
    title_frame.pack(fill=X, padx=5, pady=5)
    title_frame.pack_propagate(False)
    
    section_title = Label(title_frame, text="Cadastro REPIS", 
                         font=('Segoe UI', 16, 'bold'), bg=co2, fg=co1)
    section_title.pack(pady=12)
    
    # Frame de pesquisa estilizado
    search_frame = LabelFrame(main_container, text="Pesquisa Rapida", 
                             font=('Segoe UI', 12, 'bold'), bg=co1, fg=co0,
                             relief="solid", bd=1)
    search_frame.pack(fill=X, padx=10, pady=5)
    
    search_inner = Frame(search_frame, bg=co1)
    search_inner.pack(fill=X, padx=10, pady=10)
    
    Label(search_inner, text="CNPJ:", font=('Segoe UI', 10, 'bold'), bg=co1, fg=co0).grid(row=0, column=0, sticky=W, padx=5)
    e_pesquisa = Entry(search_inner, width=25, font=('Segoe UI', 10), relief='solid', bd=2)
    e_pesquisa.grid(row=0, column=1, padx=10, pady=5)
    
    def pesquisar_cnpj():
        cnpj = e_pesquisa.get()
        if cnpj:
            resultado = buscar_repis_por_cnpj(cnpj)
            if resultado:
                e_cnpj.delete(0, END)
                e_cnpj.insert(0, resultado[0])
                e_email.delete(0, END)
                e_email.insert(0, resultado[1] if resultado[1] else "")
                e_endereco.delete(0, END)
                e_endereco.insert(0, resultado[2] if resultado[2] else "")
                combo_certificado.set(resultado[3] if resultado[3] else "")
                combo_situacao.set(resultado[4] if resultado[4] else "")
                messagebox.showinfo('Sucesso', 'Dados encontrados!')
            else:
                messagebox.showwarning('Aviso', 'CNPJ nao encontrado!')
        else:
            messagebox.showerror('Erro', 'Digite um CNPJ para pesquisar')

    search_btn = criar_botao_moderno(search_inner, 'Pesquisar', pesquisar_cnpj, co2)
    search_btn.grid(row=0, column=2, padx=10)
    
    # Frame do formulario com layout em grid moderno
    form_frame = LabelFrame(main_container, text="Dados do Cadastro", 
                           font=('Segoe UI', 12, 'bold'), bg=co1, fg=co0,
                           relief="solid", bd=1)
    form_frame.pack(fill=BOTH, expand=True, padx=10, pady=5)
    
    form_inner = Frame(form_frame, bg=co1)
    form_inner.pack(fill=BOTH, expand=True, padx=15, pady=15)
    
    # Configurar grid
    form_inner.columnconfigure(1, weight=1)
    form_inner.columnconfigure(3, weight=1)
    
    # Campos do formulario com estilo moderno
    Label(form_inner, text="CNPJ *", font=('Segoe UI', 10, 'bold'), bg=co1, fg=co0).grid(row=0, column=0, sticky=W, pady=5)
    e_cnpj = Entry(form_inner, width=30, font=('Segoe UI', 10), relief='solid', bd=2)
    e_cnpj.grid(row=0, column=1, sticky=EW, padx=10, pady=5)

    Label(form_inner, text="Email *", font=('Segoe UI', 10, 'bold'), bg=co1, fg=co0).grid(row=0, column=2, sticky=W, pady=5)
    e_email = Entry(form_inner, width=30, font=('Segoe UI', 10), relief='solid', bd=2)
    e_email.grid(row=0, column=3, sticky=EW, padx=10, pady=5)

    Label(form_inner, text="Endereco *", font=('Segoe UI', 10, 'bold'), bg=co1, fg=co0).grid(row=1, column=0, sticky=W, pady=5)
    e_endereco = Entry(form_inner, width=60, font=('Segoe UI', 10), relief='solid', bd=2)
    e_endereco.grid(row=1, column=1, columnspan=3, sticky=EW, padx=10, pady=5)

    Label(form_inner, text="Possui Certificado *", font=('Segoe UI', 10, 'bold'), bg=co1, fg=co0).grid(row=2, column=0, sticky=W, pady=5)
    combo_certificado = ttk.Combobox(form_inner, width=15, values=["Sim", "Nao"], font=('Segoe UI', 10))
    combo_certificado.grid(row=2, column=1, sticky=W, padx=10, pady=5)

    Label(form_inner, text="Situacao *", font=('Segoe UI', 10, 'bold'), bg=co1, fg=co0).grid(row=2, column=2, sticky=W, pady=5)
    combo_situacao = ttk.Combobox(form_inner, width=15, values=["Em analise", "Aguardando", "Concluido"], font=('Segoe UI', 10))
    combo_situacao.grid(row=2, column=3, sticky=W, padx=10, pady=5)
    
    # Botoes com design moderno
    button_frame = Frame(form_inner, bg=co1)
    button_frame.grid(row=3, column=0, columnspan=4, pady=20)
    
    # Tabela dados REPIS
    table_frame = Frame(frame_data_display, bg=co1, relief="solid", bd=1)
    table_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)
    
    table_title = Frame(table_frame, bg=co6, height=40)
    table_title.pack(fill=X)
    table_title.pack_propagate(False)
    
    Label(table_title, text="Dados REPIS Cadastrados", 
          font=('Segoe UI', 14, 'bold'), bg=co6, fg=co1).pack(pady=10)

    def mostrar_dados_repis():
        # Limpar tabela existente
        for widget in table_frame.winfo_children():
            if isinstance(widget, ttk.Treeview):
                widget.destroy()
        
        list_header = ['CNPJ', 'Email', 'Endereco', 'Possui Certificado', 'Situacao']
        df_list = ver_dados_repis()

        global tree_dados_repis
        
        tree_frame = Frame(table_frame, bg=co1)
        tree_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        tree_dados_repis = ttk.Treeview(tree_frame, selectmode="extended", columns=list_header, show="headings", height=8)
        
        # Scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree_dados_repis.yview)
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree_dados_repis.xview)
        tree_dados_repis.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        tree_dados_repis.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')

        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        # Configurar colunas
        widths = [150, 200, 300, 120, 120]
        for i, col in enumerate(list_header):
            tree_dados_repis.heading(col, text=col, anchor=W)
            tree_dados_repis.column(col, width=widths[i], anchor=W)

        # Inserir dados com cores alternadas
        for i, item in enumerate(df_list):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            tree_dados_repis.insert('', 'end', values=item, tags=(tag,))
        
        # Configurar tags para cores alternadas
        tree_dados_repis.tag_configure('evenrow', background=co5)
        tree_dados_repis.tag_configure('oddrow', background=co1)

    # Funcao novo cadastro REPIS
    def novo_cadastro_repis():
        cnpj = e_cnpj.get()
        email = e_email.get()
        endereco = e_endereco.get()
        possui_certificado = combo_certificado.get()
        situacao = combo_situacao.get()
        
        lista = [cnpj, email, endereco, possui_certificado, situacao]

        for i in lista:
            if i == "":
                messagebox.showerror('Erro', 'Preencha todos os campos')
                return
            
        try:
            criar_repis(lista)
            messagebox.showinfo('Sucesso', 'Os dados foram inseridos com sucesso')
            
            # Limpar campos
            e_cnpj.delete(0,END)
            e_email.delete(0,END)
            e_endereco.delete(0,END)
            combo_certificado.set("")
            combo_situacao.set("")
            
            mostrar_dados_repis()
        except sqlite3.IntegrityError:
            messagebox.showerror('Erro', 'CNPJ ja cadastrado!')

    # Funcao atualizar REPIS
    def atualizar_repis_func():
        try:
            selected_item = tree_dados_repis.selection()[0]
            cnpj_selecionado = tree_dados_repis.item(selected_item, 'values')[0]
            
            cnpj = e_cnpj.get()
            email = e_email.get()
            endereco = e_endereco.get()
            possui_certificado = combo_certificado.get()
            situacao = combo_situacao.get()
            
            if not all([cnpj, email, endereco, possui_certificado, situacao]):
                messagebox.showerror('Erro', 'Preencha todos os campos')
                return
                
            atualizar_repis(cnpj_selecionado, email=email, endereco=endereco, 
                          possui_certificado=possui_certificado, situacao=situacao)
            
            messagebox.showinfo('Sucesso', 'Dados atualizados com sucesso')
            mostrar_dados_repis()
            
        except IndexError:
            messagebox.showerror('Erro', 'Selecione um item na tabela')

    # Funcao deletar REPIS
    def deletar_repis_func():
        try:
            selected_item = tree_dados_repis.selection()[0]
            cnpj_selecionado = tree_dados_repis.item(selected_item, 'values')[0]
            
            resposta = messagebox.askyesno('Confirmacao', f'Deseja realmente excluir o registro do CNPJ {cnpj_selecionado}?')
            if resposta:
                excluir_repis(cnpj_selecionado)
                messagebox.showinfo('Sucesso', 'Registro excluido com sucesso')
                mostrar_dados_repis()
                
        except IndexError:
            messagebox.showerror('Erro', 'Selecione um item na tabela')

    # Criar botoes
    btn_salvar = criar_botao_moderno(button_frame, "SALVAR", novo_cadastro_repis, co3)
    btn_salvar.pack(side=LEFT, padx=5)
    
    btn_atualizar = criar_botao_moderno(button_frame, "ATUALIZAR", atualizar_repis_func, co2)
    btn_atualizar.pack(side=LEFT, padx=5)
    
    btn_deletar = criar_botao_moderno(button_frame, "DELETAR", deletar_repis_func, co4)
    btn_deletar.pack(side=LEFT, padx=5)

    mostrar_dados_repis()

#---- CONTADOR com design moderno
def contador():
    # Limpar frames
    for widget in frame_content.winfo_children():
        widget.destroy()
    for widget in frame_data_display.winfo_children():
        widget.destroy()
    
    aba_ativa.set("contador")
    atualizar_navegacao()
    
    # Container principal
    main_container = Frame(frame_content, bg=co1, relief="solid", bd=1)
    main_container.pack(fill=BOTH, expand=True, padx=10, pady=10)
    
    # Titulo da secao
    title_frame = Frame(main_container, bg=co9, height=50)
    title_frame.pack(fill=X, padx=5, pady=5)
    title_frame.pack_propagate(False)
    
    section_title = Label(title_frame, text="Cadastro de Contadores", 
                         font=('Segoe UI', 16, 'bold'), bg=co9, fg=co1)
    section_title.pack(pady=12)
    
    # Frame de pesquisa
    search_frame = LabelFrame(main_container, text="Pesquisa por CNPJ ou Nome", 
                             font=('Segoe UI', 12, 'bold'), bg=co1, fg=co0,
                             relief="solid", bd=1)
    search_frame.pack(fill=X, padx=10, pady=5)
    
    search_inner = Frame(search_frame, bg=co1)
    search_inner.pack(fill=X, padx=10, pady=10)
    
    Label(search_inner, text="Termo:", font=('Segoe UI', 10, 'bold'), bg=co1, fg=co0).grid(row=0, column=0, sticky=W, padx=5)
    e_pesquisa_cont = Entry(search_inner, width=25, font=('Segoe UI', 10), relief='solid', bd=2)
    e_pesquisa_cont.grid(row=0, column=1, padx=10, pady=5)
    
    def pesquisar_contador():
        termo = e_pesquisa_cont.get()
        if termo:
            resultado = buscar_contador_por_cnpj_ou_nome(termo)
            if resultado:
                e_cnpj.delete(0, END)
                e_cnpj.insert(0, resultado[0])
                e_nome.delete(0, END)
                e_nome.insert(0, resultado[1])
                e_municipio.delete(0, END)
                e_municipio.insert(0, resultado[2])
                e_socio.delete(0, END)
                e_socio.insert(0, resultado[3])
                e_contato.delete(0, END)
                e_contato.insert(0, resultado[4])
                combo_tipo_pessoa.set(resultado[5] if resultado[5] else "")
                combo_tipo_telefone.set(resultado[6] if resultado[6] else "")
                messagebox.showinfo('Sucesso', 'Dados encontrados!')
            else:
                messagebox.showwarning('Aviso', 'Registro nao encontrado!')
        else:
            messagebox.showerror('Erro', 'Digite um CNPJ ou nome para pesquisar')

    search_btn = criar_botao_moderno(search_inner, 'Pesquisar', pesquisar_contador, co9)
    search_btn.grid(row=0, column=2, padx=10)
    
    # Frame do formulario
    form_frame = LabelFrame(main_container, text="Dados do Contador", 
                           font=('Segoe UI', 12, 'bold'), bg=co1, fg=co0,
                           relief="solid", bd=1)
    form_frame.pack(fill=BOTH, expand=True, padx=10, pady=5)
    
    form_inner = Frame(form_frame, bg=co1)
    form_inner.pack(fill=BOTH, expand=True, padx=15, pady=15)
    
    # Configurar grid
    form_inner.columnconfigure(1, weight=1)
    form_inner.columnconfigure(3, weight=1)
    
    # Campos do formulario
    Label(form_inner, text="CNPJ *", font=('Segoe UI', 10, 'bold'), bg=co1, fg=co0).grid(row=0, column=0, sticky=W, pady=5)
    e_cnpj = Entry(form_inner, width=30, font=('Segoe UI', 10), relief='solid', bd=2)
    e_cnpj.grid(row=0, column=1, sticky=EW, padx=10, pady=5)

    Label(form_inner, text="Nome *", font=('Segoe UI', 10, 'bold'), bg=co1, fg=co0).grid(row=0, column=2, sticky=W, pady=5)
    e_nome = Entry(form_inner, width=30, font=('Segoe UI', 10), relief='solid', bd=2)
    e_nome.grid(row=0, column=3, sticky=EW, padx=10, pady=5)

    Label(form_inner, text="Municipio *", font=('Segoe UI', 10, 'bold'), bg=co1, fg=co0).grid(row=1, column=0, sticky=W, pady=5)
    e_municipio = Entry(form_inner, width=30, font=('Segoe UI', 10), relief='solid', bd=2)
    e_municipio.grid(row=1, column=1, sticky=EW, padx=10, pady=5)

    Label(form_inner, text="Socio *", font=('Segoe UI', 10, 'bold'), bg=co1, fg=co0).grid(row=1, column=2, sticky=W, pady=5)
    e_socio = Entry(form_inner, width=30, font=('Segoe UI', 10), relief='solid', bd=2)
    e_socio.grid(row=1, column=3, sticky=EW, padx=10, pady=5)

    Label(form_inner, text="Contato *", font=('Segoe UI', 10, 'bold'), bg=co1, fg=co0).grid(row=2, column=0, sticky=W, pady=5)
    e_contato = Entry(form_inner, width=30, font=('Segoe UI', 10), relief='solid', bd=2)
    e_contato.grid(row=2, column=1, sticky=EW, padx=10, pady=5)

    Label(form_inner, text="Tipo de Pessoa *", font=('Segoe UI', 10, 'bold'), bg=co1, fg=co0).grid(row=3, column=0, sticky=W, pady=5)
    combo_tipo_pessoa = ttk.Combobox(form_inner, width=15, values=["Pessoa Fisica", "Empresa"], font=('Segoe UI', 10))
    combo_tipo_pessoa.grid(row=3, column=1, sticky=W, padx=10, pady=5)

    Label(form_inner, text="Tipo de Telefone *", font=('Segoe UI', 10, 'bold'), bg=co1, fg=co0).grid(row=3, column=2, sticky=W, pady=5)
    combo_tipo_telefone = ttk.Combobox(form_inner, width=15, values=["Gerente", "Responsavel"], font=('Segoe UI', 10))
    combo_tipo_telefone.grid(row=3, column=3, sticky=W, padx=10, pady=5)
    
    # Botoes
    button_frame = Frame(form_inner, bg=co1)
    button_frame.grid(row=4, column=0, columnspan=4, pady=20)
    
    # Tabela dados Contadores
    table_frame = Frame(frame_data_display, bg=co1, relief="solid", bd=1)
    table_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)
    
    table_title = Frame(table_frame, bg=co9, height=40)
    table_title.pack(fill=X)
    table_title.pack_propagate(False)
    
    Label(table_title, text="Contadores Cadastrados", 
          font=('Segoe UI', 14, 'bold'), bg=co9, fg=co1).pack(pady=10)

    def mostrar_dados_contadores():
        # Limpar tabela existente
        for widget in table_frame.winfo_children():
            if isinstance(widget, ttk.Treeview):
                widget.destroy()
        
        list_header = ['CNPJ', 'Nome', 'Municipio', 'Socio', 'Contato', 'Tipo Pessoa', 'Tipo Telefone']
        df_list = ver_dados_contadores()

        global tree_dados_contadores
        
        tree_frame = Frame(table_frame, bg=co1)
        tree_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        tree_dados_contadores = ttk.Treeview(tree_frame, selectmode="extended", columns=list_header, show="headings", height=8)
        
        # Scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree_dados_contadores.yview)
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree_dados_contadores.xview)
        tree_dados_contadores.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        tree_dados_contadores.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')

        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        # Configurar colunas
        widths = [120, 150, 120, 120, 120, 100, 100]
        for i, col in enumerate(list_header):
            tree_dados_contadores.heading(col, text=col, anchor=W)
            tree_dados_contadores.column(col, width=widths[i], anchor=W)

        # Inserir dados com cores alternadas
        for i, item in enumerate(df_list):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            tree_dados_contadores.insert('', 'end', values=item, tags=(tag,))
        
        # Configurar tags para cores alternadas
        tree_dados_contadores.tag_configure('evenrow', background=co5)
        tree_dados_contadores.tag_configure('oddrow', background=co1)

    # Funcoes CRUD
    def novo_cadastro_contador():
        cnpj = e_cnpj.get()
        nome = e_nome.get()
        municipio = e_municipio.get()
        socio = e_socio.get()
        contato = e_contato.get()
        tipo_pessoa = combo_tipo_pessoa.get()
        tipo_telefone = combo_tipo_telefone.get()
        
        lista = [cnpj, nome, municipio, socio, contato, tipo_pessoa, tipo_telefone]

        for i in lista:
            if i == "":
                messagebox.showerror('Erro', 'Preencha todos os campos')
                return
            
        try:
            criar_contador_novo(lista)
            messagebox.showinfo('Sucesso', 'Os dados foram inseridos com sucesso')

            # Limpar campos
            e_cnpj.delete(0,END)
            e_nome.delete(0,END)
            e_municipio.delete(0,END)
            e_socio.delete(0,END)
            e_contato.delete(0,END)
            combo_tipo_pessoa.set("")
            combo_tipo_telefone.set("")

            mostrar_dados_contadores()
        except sqlite3.IntegrityError:
            messagebox.showerror('Erro', 'CNPJ ja cadastrado!')

    def atualizar_contador_func():
        try:
            selected_item = tree_dados_contadores.selection()[0]
            cnpj_selecionado = tree_dados_contadores.item(selected_item, 'values')[0]
            
            cnpj = e_cnpj.get()
            nome = e_nome.get()
            municipio = e_municipio.get()
            socio = e_socio.get()
            contato = e_contato.get()
            tipo_pessoa = combo_tipo_pessoa.get()
            tipo_telefone = combo_tipo_telefone.get()
            
            if not all([cnpj, nome, municipio, socio, contato, tipo_pessoa, tipo_telefone]):
                messagebox.showerror('Erro', 'Preencha todos os campos')
                return
                
            atualizar_contador_novo(cnpj_selecionado, nome=nome, municipio=municipio, 
                                  socio=socio, contato=contato, tipo_pessoa=tipo_pessoa, 
                                  tipo_telefone=tipo_telefone)
            
            messagebox.showinfo('Sucesso', 'Dados atualizados com sucesso')
            mostrar_dados_contadores()
            
        except IndexError:
            messagebox.showerror('Erro', 'Selecione um item na tabela')

    def deletar_contador_func():
        try:
            selected_item = tree_dados_contadores.selection()[0]
            cnpj_selecionado = tree_dados_contadores.item(selected_item, 'values')[0]
            
            resposta = messagebox.askyesno('Confirmacao', f'Deseja realmente excluir o registro do CNPJ {cnpj_selecionado}?')
            if resposta:
                excluir_contador_novo(cnpj_selecionado)
                messagebox.showinfo('Sucesso', 'Registro excluido com sucesso')
                mostrar_dados_contadores()
                
        except IndexError:
            messagebox.showerror('Erro', 'Selecione um item na tabela')

    # Criar botoes
    btn_salvar = criar_botao_moderno(button_frame, "SALVAR", novo_cadastro_contador, co3)
    btn_salvar.pack(side=LEFT, padx=5)
    
    btn_atualizar = criar_botao_moderno(button_frame, "ATUALIZAR", atualizar_contador_func, co2)
    btn_atualizar.pack(side=LEFT, padx=5)
    
    btn_deletar = criar_botao_moderno(button_frame, "DELETAR", deletar_contador_func, co4)
    btn_deletar.pack(side=LEFT, padx=5)

    mostrar_dados_contadores()

#----- EXPORTAR com design moderno
def exportar():
    # Limpar frames
    for widget in frame_content.winfo_children():
        widget.destroy()
    for widget in frame_data_display.winfo_children():
        widget.destroy()
    
    aba_ativa.set("salvar")
    atualizar_navegacao()
    
    # Container principal
    main_container = Frame(frame_content, bg=co1, relief="solid", bd=1)
    main_container.pack(fill=BOTH, expand=True, padx=10, pady=10)
    
    # Titulo da secao
    title_frame = Frame(main_container, bg=co7, height=50)
    title_frame.pack(fill=X, padx=5, pady=5)
    title_frame.pack_propagate(False)
    
    section_title = Label(title_frame, text="Opcoes de Exportacao e Importacao", 
                         font=('Segoe UI', 16, 'bold'), bg=co7, fg=co1)
    section_title.pack(pady=12)
    
    # Frame de opcoes
    options_frame = Frame(main_container, bg=co1)
    options_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)
    
    # Selecao de tabela
    Label(options_frame, text="Selecione a tabela:", font=('Segoe UI', 12, 'bold'), bg=co1, fg=co0).pack(pady=10)
    combo_tabela = ttk.Combobox(options_frame, width=20, values=["REPIS", "Contadores"], font=('Segoe UI', 12))
    combo_tabela.pack(pady=10)
    
    # Frame de botoes de exportacao
    export_frame = LabelFrame(options_frame, text="Exportar Dados", 
                             font=('Segoe UI', 12, 'bold'), bg=co1, fg=co0,
                             relief="solid", bd=1)
    export_frame.pack(fill=X, pady=20)
    
    export_buttons = Frame(export_frame, bg=co1)
    export_buttons.pack(pady=20)
    
    def exportar_pdf():
        tabela = combo_tabela.get()
        if not tabela:
            messagebox.showerror('Erro', 'Selecione uma tabela')
            return
        exportar_para_pdf(tabela)
    
    def exportar_word():
        tabela = combo_tabela.get()
        if not tabela:
            messagebox.showerror('Erro', 'Selecione uma tabela')
            return
        exportar_para_word(tabela)
    
    def exportar_excel():
        tabela = combo_tabela.get()
        if not tabela:
            messagebox.showerror('Erro', 'Selecione uma tabela')
            return
        exportar_para_excel(tabela)
    
    # Botoes de exportacao
    btn_pdf = criar_botao_moderno(export_buttons, 'Exportar PDF', exportar_pdf, co4, 15)
    btn_pdf.pack(side=LEFT, padx=10)
    
    btn_word = criar_botao_moderno(export_buttons, 'Exportar Word', exportar_word, co2, 15)
    btn_word.pack(side=LEFT, padx=10)
    
    btn_excel = criar_botao_moderno(export_buttons, 'Exportar Excel', exportar_excel, co7, 15)
    btn_excel.pack(side=LEFT, padx=10)
    
    # Frame de importacao
    import_frame = LabelFrame(options_frame, text="Importar Dados do Excel", 
                             font=('Segoe UI', 12, 'bold'), bg=co1, fg=co0,
                             relief="solid", bd=1)
    import_frame.pack(fill=X, pady=20)
    
    import_buttons = Frame(import_frame, bg=co1)
    import_buttons.pack(pady=20)
    
    def importar_excel():
        arquivo = fd.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
        if arquivo:
            importar_de_excel(arquivo)
    
    btn_importar = criar_botao_moderno(import_buttons, 'Importar Excel', importar_excel, co8, 15)
    btn_importar.pack()
    
    # Informacoes sobre importacao
    info_frame = Frame(options_frame, bg=co5, relief="solid", bd=1)
    info_frame.pack(fill=X, pady=20)
    
    Label(info_frame, text="Selecione a tabela para ser exportada", 
          font=('Segoe UI', 12, 'bold'), bg=co5, fg=co0).pack(pady=10)
    
    Label(info_frame, text="Para importar dados selecione a tabela e o formato para exportar.", 
          font=('Segoe UI', 10), bg=co5, fg=co0, justify=CENTER).pack(pady=10)

#---- CONTROLE
def control(i):
    if i == 'repis':
        repis()
    elif i == 'contador':
        contador()    
    elif i == 'salvar':
        exportar()

# Inicializar com REPIS
repis()

janela.mainloop()