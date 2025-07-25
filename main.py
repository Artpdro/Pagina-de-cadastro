from tkinter.ttk import *
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog as fd
from PIL import ImageTk, Image
import requests
import json
import sqlite3

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
janela.title("Sindnorte - REPIS e Contadores")
janela.geometry("1400x900")
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
frame_header = Frame(janela, width=1400, height=80, bg=co2)
frame_header.grid(row=0, column=0, pady=0, padx=0, sticky=NSEW)
frame_header.grid_propagate(False)

# Separador com gradiente visual
separator1 = Frame(janela, width=1400, height=3, bg=co6)
separator1.grid(row=1, column=0, pady=0, padx=0, sticky=NSEW)

frame_navigation = Frame(janela, width=1400, height=80, bg=co1)
frame_navigation.grid(row=2, column=0, pady=0, padx=0, sticky=NSEW)
frame_navigation.grid_propagate(False)

separator2 = Frame(janela, width=1400, height=2, bg=co5)
separator2.grid(row=3, column=0, pady=0, padx=0, sticky=NSEW)

frame_content = Frame(janela, width=1400, height=400, bg=co1)
frame_content.grid(row=4, column=0, pady=10, padx=20, sticky=NSEW)

frame_data_display = Frame(janela, width=1400, height=320, bg=co1)
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
    
    btn_empresas = criar_botao_nav("Empresas", lambda: control('empresas'), aba_ativa.get() == "empresas")
    btn_empresas.pack(side=LEFT, padx=10, pady=20)
    
    btn_preenchimento = criar_botao_nav("Preenchimento PDF", lambda: control('preenchimento'), aba_ativa.get() == "preenchimento")
    btn_preenchimento.pack(side=LEFT, padx=10, pady=20)
    
    btn_salvar = criar_botao_nav("Exportar", lambda: control('salvar'), aba_ativa.get() == "salvar")
    btn_salvar.pack(side=LEFT, padx=10, pady=20)

def criar_botao_moderno(parent, text, command, bg_color, width=12):
    btn = Button(parent, text=text, command=command,
                font=('Segoe UI', 10, 'bold'), bg=bg_color, fg=co1, 
                relief='flat', cursor='hand2', width=width, pady=8,
                activebackground=bg_color, activeforeground=co1)
    return btn

#---- REPIS com design moderno e novos campos
def repis():
    # Limpar frames
    for widget in frame_content.winfo_children():
        widget.destroy()
    for widget in frame_data_display.winfo_children():
        widget.destroy()
    
    aba_ativa.set("repis")
    atualizar_navegacao()
    
    # Container principal com scroll
    main_container = Frame(frame_content, bg=co1, relief="solid", bd=1)
    main_container.pack(fill=BOTH, expand=True, padx=10, pady=10)
    
    # Canvas para scroll
    canvas = Canvas(main_container, bg=co1)
    scrollbar = Scrollbar(main_container, orient="vertical", command=canvas.yview)
    scrollable_frame = Frame(canvas, bg=co1)
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    # Titulo da secao
    title_frame = Frame(scrollable_frame, bg=co2, height=50)
    title_frame.pack(fill=X, padx=5, pady=5)
    title_frame.pack_propagate(False)
    
    section_title = Label(title_frame, text="Cadastro REPIS", 
                         font=('Segoe UI', 16, 'bold'), bg=co2, fg=co1)
    section_title.pack(pady=12)
    
    # Frame de pesquisa estilizado
    search_frame = LabelFrame(scrollable_frame, text="Pesquisa Rapida", 
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
                # Preencher todos os campos
                e_cnpj.delete(0, END)
                e_cnpj.insert(0, resultado[0])
                e_razao_social.delete(0, END)
                e_razao_social.insert(0, resultado[1] if resultado[1] else "")
                e_nome_fantasia.delete(0, END)
                e_nome_fantasia.insert(0, resultado[2] if resultado[2] else "")
                e_endereco.delete(0, END)
                e_endereco.insert(0, resultado[3] if resultado[3] else "")
                e_complemento.delete(0, END)
                e_complemento.insert(0, resultado[4] if resultado[4] else "")
                e_cep.delete(0, END)
                e_cep.insert(0, resultado[5] if resultado[5] else "")
                e_email.delete(0, END)
                e_email.insert(0, resultado[6] if resultado[6] else "")
                e_bairro.delete(0, END)
                e_bairro.insert(0, resultado[7] if resultado[7] else "")
                combo_uf.set(resultado[8] if resultado[8] else "")
                e_municipio.delete(0, END)
                e_municipio.insert(0, resultado[9] if resultado[9] else "")
                e_data_abertura.delete(0, END)
                e_data_abertura.insert(0, resultado[10] if resultado[10] else "")
                e_nome_solicitante.delete(0, END)
                e_nome_solicitante.insert(0, resultado[11] if resultado[11] else "")
                combo_solicitante_tipo.set(resultado[12] if resultado[12] else "")
                e_telefone.delete(0, END)
                e_telefone.insert(0, resultado[13] if resultado[13] else "")
                e_email_solicitante.delete(0, END)
                e_email_solicitante.insert(0, resultado[14] if resultado[14] else "")
                e_cpf.delete(0, END)
                e_cpf.insert(0, resultado[15] if resultado[15] else "")
                e_rg.delete(0, END)
                e_rg.insert(0, resultado[16] if resultado[16] else "")
                e_contador.delete(0, END)
                e_contador.insert(0, resultado[17] if resultado[17] else "")
                e_telefone_contador.delete(0, END)
                e_telefone_contador.insert(0, resultado[18] if resultado[18] else "")
                e_email_contador.delete(0, END)
                e_email_contador.insert(0, resultado[19] if resultado[19] else "")
                messagebox.showinfo('Sucesso', 'Dados encontrados!')
            else:
                messagebox.showwarning('Aviso', 'CNPJ nao encontrado!')
        else:
            messagebox.showerror('Erro', 'Digite um CNPJ para pesquisar')

    search_btn = criar_botao_moderno(search_inner, 'Pesquisar', pesquisar_cnpj, co2)
    search_btn.grid(row=0, column=2, padx=10)
    
    # Frame do formulario com layout em grid moderno
    form_frame = LabelFrame(scrollable_frame, text="Dados do Cadastro REPIS", 
                           font=('Segoe UI', 12, 'bold'), bg=co1, fg=co0,
                           relief="solid", bd=1)
    form_frame.pack(fill=BOTH, expand=True, padx=10, pady=5)
    
    form_inner = Frame(form_frame, bg=co1)
    form_inner.pack(fill=BOTH, expand=True, padx=15, pady=15)
    
    # Configurar grid
    form_inner.columnconfigure(1, weight=1)
    form_inner.columnconfigure(3, weight=1)
    
    # Campos do formulario com estilo moderno
    row = 0
    
    # Linha 1: CNPJ e Razão Social
    Label(form_inner, text="CNPJ *", font=('Segoe UI', 10, 'bold'), bg=co1, fg=co0).grid(row=row, column=0, sticky=W, pady=5)
    e_cnpj = Entry(form_inner, width=30, font=('Segoe UI', 10), relief='solid', bd=2)
    e_cnpj.grid(row=row, column=1, sticky=EW, padx=10, pady=5)

    Label(form_inner, text="Razão Social *", font=('Segoe UI', 10, 'bold'), bg=co1, fg=co0).grid(row=row, column=2, sticky=W, pady=5)
    e_razao_social = Entry(form_inner, width=30, font=('Segoe UI', 10), relief='solid', bd=2)
    e_razao_social.grid(row=row, column=3, sticky=EW, padx=10, pady=5)
    row += 1

    # Linha 2: Nome Fantasia e E-mail
    Label(form_inner, text="Nome Fantasia", font=('Segoe UI', 10, 'bold'), bg=co1, fg=co0).grid(row=row, column=0, sticky=W, pady=5)
    e_nome_fantasia = Entry(form_inner, width=30, font=('Segoe UI', 10), relief='solid', bd=2)
    e_nome_fantasia.grid(row=row, column=1, sticky=EW, padx=10, pady=5)

    Label(form_inner, text="E-mail *", font=('Segoe UI', 10, 'bold'), bg=co1, fg=co0).grid(row=row, column=2, sticky=W, pady=5)
    e_email = Entry(form_inner, width=30, font=('Segoe UI', 10), relief='solid', bd=2)
    e_email.grid(row=row, column=3, sticky=EW, padx=10, pady=5)
    row += 1

    # Linha 3: Endereço
    Label(form_inner, text="Endereço *", font=('Segoe UI', 10, 'bold'), bg=co1, fg=co0).grid(row=row, column=0, sticky=W, pady=5)
    e_endereco = Entry(form_inner, width=60, font=('Segoe UI', 10), relief='solid', bd=2)
    e_endereco.grid(row=row, column=1, columnspan=3, sticky=EW, padx=10, pady=5)
    row += 1

    # Linha 4: Complemento e CEP
    Label(form_inner, text="Complemento", font=('Segoe UI', 10, 'bold'), bg=co1, fg=co0).grid(row=row, column=0, sticky=W, pady=5)
    e_complemento = Entry(form_inner, width=30, font=('Segoe UI', 10), relief='solid', bd=2)
    e_complemento.grid(row=row, column=1, sticky=EW, padx=10, pady=5)

    Label(form_inner, text="CEP *", font=('Segoe UI', 10, 'bold'), bg=co1, fg=co0).grid(row=row, column=2, sticky=W, pady=5)
    e_cep = Entry(form_inner, width=30, font=('Segoe UI', 10), relief='solid', bd=2)
    e_cep.grid(row=row, column=3, sticky=EW, padx=10, pady=5)
    row += 1

    # Linha 5: Bairro e UF
    Label(form_inner, text="Bairro *", font=('Segoe UI', 10, 'bold'), bg=co1, fg=co0).grid(row=row, column=0, sticky=W, pady=5)
    e_bairro = Entry(form_inner, width=30, font=('Segoe UI', 10), relief='solid', bd=2)
    e_bairro.grid(row=row, column=1, sticky=EW, padx=10, pady=5)

    Label(form_inner, text="UF *", font=('Segoe UI', 10, 'bold'), bg=co1, fg=co0).grid(row=row, column=2, sticky=W, pady=5)
    combo_uf = ttk.Combobox(form_inner, width=15, values=["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"], font=('Segoe UI', 10))
    combo_uf.grid(row=row, column=3, sticky=W, padx=10, pady=5)
    row += 1

    # Linha 6: Município e Data de Abertura
    Label(form_inner, text="Município *", font=('Segoe UI', 10, 'bold'), bg=co1, fg=co0).grid(row=row, column=0, sticky=W, pady=5)
    e_municipio = Entry(form_inner, width=30, font=('Segoe UI', 10), relief='solid', bd=2)
    e_municipio.grid(row=row, column=1, sticky=EW, padx=10, pady=5)

    Label(form_inner, text="Data de Abertura", font=('Segoe UI', 10, 'bold'), bg=co1, fg=co0).grid(row=row, column=2, sticky=W, pady=5)
    e_data_abertura = Entry(form_inner, width=30, font=('Segoe UI', 10), relief='solid', bd=2)
    e_data_abertura.grid(row=row, column=3, sticky=EW, padx=10, pady=5)
    row += 1

    # Separador
    separator = Frame(form_inner, bg=co6, height=2)
    separator.grid(row=row, column=0, columnspan=4, sticky=EW, pady=10)
    row += 1

    # Seção do Solicitante
    Label(form_inner, text="DADOS DO SOLICITANTE", font=('Segoe UI', 12, 'bold'), bg=co1, fg=co2).grid(row=row, column=0, columnspan=4, pady=10)
    row += 1

    # Linha 7: Nome do Solicitante e Tipo
    Label(form_inner, text="Nome do Solicitante *", font=('Segoe UI', 10, 'bold'), bg=co1, fg=co0).grid(row=row, column=0, sticky=W, pady=5)
    e_nome_solicitante = Entry(form_inner, width=30, font=('Segoe UI', 10), relief='solid', bd=2)
    e_nome_solicitante.grid(row=row, column=1, sticky=EW, padx=10, pady=5)

    Label(form_inner, text="Solicitante é *", font=('Segoe UI', 10, 'bold'), bg=co1, fg=co0).grid(row=row, column=2, sticky=W, pady=5)
    combo_solicitante_tipo = ttk.Combobox(form_inner, width=15, values=["Sócio", "Contador"], font=('Segoe UI', 10))
    combo_solicitante_tipo.grid(row=row, column=3, sticky=W, padx=10, pady=5)
    row += 1

    # Linha 8: Telefone e Email do Solicitante
    Label(form_inner, text="Telefone *", font=('Segoe UI', 10, 'bold'), bg=co1, fg=co0).grid(row=row, column=0, sticky=W, pady=5)
    e_telefone = Entry(form_inner, width=30, font=('Segoe UI', 10), relief='solid', bd=2)
    e_telefone.grid(row=row, column=1, sticky=EW, padx=10, pady=5)

    Label(form_inner, text="Email do Solicitante", font=('Segoe UI', 10, 'bold'), bg=co1, fg=co0).grid(row=row, column=2, sticky=W, pady=5)
    e_email_solicitante = Entry(form_inner, width=30, font=('Segoe UI', 10), relief='solid', bd=2)
    e_email_solicitante.grid(row=row, column=3, sticky=EW, padx=10, pady=5)
    row += 1

    # Linha 9: CPF e RG
    Label(form_inner, text="CPF *", font=('Segoe UI', 10, 'bold'), bg=co1, fg=co0).grid(row=row, column=0, sticky=W, pady=5)
    e_cpf = Entry(form_inner, width=30, font=('Segoe UI', 10), relief='solid', bd=2)
    e_cpf.grid(row=row, column=1, sticky=EW, padx=10, pady=5)

    Label(form_inner, text="RG", font=('Segoe UI', 10, 'bold'), bg=co1, fg=co0).grid(row=row, column=2, sticky=W, pady=5)
    e_rg = Entry(form_inner, width=30, font=('Segoe UI', 10), relief='solid', bd=2)
    e_rg.grid(row=row, column=3, sticky=EW, padx=10, pady=5)
    row += 1

    # Separador
    separator2 = Frame(form_inner, bg=co6, height=2)
    separator2.grid(row=row, column=0, columnspan=4, sticky=EW, pady=10)
    row += 1

    # Seção do Contador
    Label(form_inner, text="DADOS DO CONTADOR", font=('Segoe UI', 12, 'bold'), bg=co1, fg=co2).grid(row=row, column=0, columnspan=4, pady=10)
    row += 1

    # Linha 10: Contador e Telefone do Contador
    Label(form_inner, text="Contador", font=('Segoe UI', 10, 'bold'), bg=co1, fg=co0).grid(row=row, column=0, sticky=W, pady=5)
    e_contador = Entry(form_inner, width=30, font=('Segoe UI', 10), relief='solid', bd=2)
    e_contador.grid(row=row, column=1, sticky=EW, padx=10, pady=5)

    Label(form_inner, text="Telefone do Contador", font=('Segoe UI', 10, 'bold'), bg=co1, fg=co0).grid(row=row, column=2, sticky=W, pady=5)
    e_telefone_contador = Entry(form_inner, width=30, font=('Segoe UI', 10), relief='solid', bd=2)
    e_telefone_contador.grid(row=row, column=3, sticky=EW, padx=10, pady=5)
    row += 1

    # Linha 11: Email do Contador
    Label(form_inner, text="Email do Contador", font=('Segoe UI', 10, 'bold'), bg=co1, fg=co0).grid(row=row, column=0, sticky=W, pady=5)
    e_email_contador = Entry(form_inner, width=30, font=('Segoe UI', 10), relief='solid', bd=2)
    e_email_contador.grid(row=row, column=1, sticky=EW, padx=10, pady=5)
    row += 1
    
    # Botoes com design moderno
    button_frame = Frame(form_inner, bg=co1)
    button_frame.grid(row=row, column=0, columnspan=4, pady=20)
    
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
        
        list_header = ['CNPJ', 'Razão Social', 'Nome Fantasia', 'Endereço', 'CEP', 'E-mail', 'Município', 'Nome Solicitante', 'Tipo Solicitante']
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
        widths = [120, 150, 120, 200, 80, 150, 120, 150, 100]
        for i, col in enumerate(list_header):
            tree_dados_repis.heading(col, text=col, anchor=W)
            tree_dados_repis.column(col, width=widths[i], anchor=W)

        # Inserir dados com cores alternadas (mostrar apenas campos principais)
        for i, item in enumerate(df_list):
            # Mostrar apenas os campos principais na tabela
            item_display = [item[0], item[1], item[2], item[3], item[5], item[6], item[9], item[11], item[12]]
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            tree_dados_repis.insert('', 'end', values=item_display, tags=(tag,))
        
        # Configurar tags para cores alternadas
        tree_dados_repis.tag_configure('evenrow', background=co5)
        tree_dados_repis.tag_configure('oddrow', background=co1)

    # Funcao novo cadastro REPIS
    def novo_cadastro_repis():
        cnpj = e_cnpj.get()
        razao_social = e_razao_social.get()
        nome_fantasia = e_nome_fantasia.get()
        endereco = e_endereco.get()
        complemento = e_complemento.get()
        cep = e_cep.get()
        email = e_email.get()
        bairro = e_bairro.get()
        uf = combo_uf.get()
        municipio = e_municipio.get()
        data_abertura = e_data_abertura.get()
        nome_solicitante = e_nome_solicitante.get()
        solicitante_tipo = combo_solicitante_tipo.get()
        telefone = e_telefone.get()
        email_solicitante = e_email_solicitante.get()
        cpf = e_cpf.get()
        rg = e_rg.get()
        contador = e_contador.get()
        telefone_contador = e_telefone_contador.get()
        email_contador = e_email_contador.get()
        
        lista = [cnpj, razao_social, nome_fantasia, endereco, complemento, cep, email, bairro, uf, municipio, data_abertura, nome_solicitante, solicitante_tipo, telefone, email_solicitante, cpf, rg, contador, telefone_contador, email_contador]

        # Verificar campos obrigatórios
        campos_obrigatorios = [cnpj, razao_social, endereco, cep, email, bairro, uf, municipio, nome_solicitante, solicitante_tipo, telefone, cpf]
        if any(campo == "" for campo in campos_obrigatorios):
            messagebox.showerror('Erro', 'Preencha todos os campos obrigatórios (*)')
            return
            
        try:
            criar_repis(lista)
            messagebox.showinfo('Sucesso', 'Os dados foram inseridos com sucesso')
            
            # Limpar campos
            for entry in [e_cnpj, e_razao_social, e_nome_fantasia, e_endereco, e_complemento, e_cep, e_email, e_bairro, e_municipio, e_data_abertura, e_nome_solicitante, e_telefone, e_email_solicitante, e_cpf, e_rg, e_contador, e_telefone_contador, e_email_contador]:
                entry.delete(0, END)
            combo_uf.set("")
            combo_solicitante_tipo.set("")
            
            mostrar_dados_repis()
        except sqlite3.IntegrityError:
            messagebox.showerror('Erro', 'CNPJ ja cadastrado!')

    # Funcao atualizar REPIS
    def atualizar_repis_func():
        try:
            selected_item = tree_dados_repis.selection()[0]
            cnpj_selecionado = tree_dados_repis.item(selected_item, 'values')[0]
            
            # Coletar todos os dados
            dados = {
                'razao_social': e_razao_social.get(),
                'nome_fantasia': e_nome_fantasia.get(),
                'endereco': e_endereco.get(),
                'complemento': e_complemento.get(),
                'cep': e_cep.get(),
                'email': e_email.get(),
                'bairro': e_bairro.get(),
                'uf': combo_uf.get(),
                'municipio': e_municipio.get(),
                'data_abertura': e_data_abertura.get(),
                'nome_solicitante': e_nome_solicitante.get(),
                'solicitante_tipo': combo_solicitante_tipo.get(),
                'telefone': e_telefone.get(),
                'email_solicitante': e_email_solicitante.get(),
                'cpf': e_cpf.get(),
                'rg': e_rg.get(),
                'contador': e_contador.get(),
                'telefone_contador': e_telefone_contador.get(),
                'email_contador': e_email_contador.get()
            }
            
            # Verificar campos obrigatórios
            campos_obrigatorios = ['razao_social', 'endereco', 'cep', 'email', 'bairro', 'uf', 'municipio', 'nome_solicitante', 'solicitante_tipo', 'telefone', 'cpf']
            if any(dados[campo] == "" for campo in campos_obrigatorios):
                messagebox.showerror('Erro', 'Preencha todos os campos obrigatórios (*)')
                return
                
            atualizar_repis(cnpj_selecionado, **dados)
            
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

#---- CONTADOR com design moderno e novos campos
def contador():
    # Limpar frames
    for widget in frame_content.winfo_children():
        widget.destroy()
    for widget in frame_data_display.winfo_children():
        widget.destroy()
    
    aba_ativa.set("contador")
    atualizar_navegacao()
    
    # Container principal com scroll
    main_container = Frame(frame_content, bg=co1, relief="solid", bd=1)
    main_container.pack(fill=BOTH, expand=True, padx=10, pady=10)
    
    # Canvas para scroll
    canvas = Canvas(main_container, bg=co1)
    scrollbar = Scrollbar(main_container, orient="vertical", command=canvas.yview)
    scrollable_frame = Frame(canvas, bg=co1)
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    # Titulo da secao
    title_frame = Frame(scrollable_frame, bg=co9, height=50)
    title_frame.pack(fill=X, padx=5, pady=5)
    title_frame.pack_propagate(False)
    
    section_title = Label(title_frame, text="Contadores", 
                         font=('Segoe UI', 16, 'bold'), bg=co9, fg=co1)
    section_title.pack(pady=12)
    
    # Frame de pesquisa
    search_frame = LabelFrame(scrollable_frame, text="Pesquisa por CNPJ ou Nome", 
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
                e_empresas_representadas.delete(0, END)
                e_empresas_representadas.insert(0, resultado[7] if resultado[7] else "")
                e_empresa_associada_1.delete(0, END)
                e_empresa_associada_1.insert(0, resultado[8] if resultado[8] else "")
                e_empresa_associada_2.delete(0, END)
                e_empresa_associada_2.insert(0, resultado[9] if resultado[9] else "")
                e_empresa_associada_3.delete(0, END)
                e_empresa_associada_3.insert(0, resultado[10] if resultado[10] else "")
                e_email.delete(0, END)
                e_email.insert(0, resultado[11] if resultado[11] else "")
                messagebox.showinfo('Sucesso', 'Dados encontrados!')
            else:
                messagebox.showwarning('Aviso', 'Registro nao encontrado!')
        else:
            messagebox.showerror('Erro', 'Digite um CNPJ ou nome para pesquisar')

    search_btn = criar_botao_moderno(search_inner, 'Pesquisar', pesquisar_contador, co9)
    search_btn.grid(row=0, column=2, padx=10)
    
    # Frame do formulario
    form_frame = LabelFrame(scrollable_frame, text="Dados do Contador", 
                           font=('Segoe UI', 12, 'bold'), bg=co1, fg=co0,
                           relief="solid", bd=1)
    form_frame.pack(fill=BOTH, expand=True, padx=10, pady=5)
    
    form_inner = Frame(form_frame, bg=co1)
    form_inner.pack(fill=BOTH, expand=True, padx=15, pady=15)
    
    # Configurar grid
    form_inner.columnconfigure(1, weight=1)
    form_inner.columnconfigure(3, weight=1)
    
    # Campos do formulario
    row = 0
    
    Label(form_inner, text="CNPJ *", font=('Segoe UI', 10, 'bold'), bg=co1, fg=co0).grid(row=row, column=0, sticky=W, pady=5)
    e_cnpj = Entry(form_inner, width=30, font=('Segoe UI', 10), relief='solid', bd=2)
    e_cnpj.grid(row=row, column=1, sticky=EW, padx=10, pady=5)

    Label(form_inner, text="Nome *", font=('Segoe UI', 10, 'bold'), bg=co1, fg=co0).grid(row=row, column=2, sticky=W, pady=5)
    e_nome = Entry(form_inner, width=30, font=('Segoe UI', 10), relief='solid', bd=2)
    e_nome.grid(row=row, column=3, sticky=EW, padx=10, pady=5)
    row += 1

    Label(form_inner, text="Municipio *", font=('Segoe UI', 10, 'bold'), bg=co1, fg=co0).grid(row=row, column=0, sticky=W, pady=5)
    e_municipio = Entry(form_inner, width=30, font=('Segoe UI', 10), relief='solid', bd=2)
    e_municipio.grid(row=row, column=1, sticky=EW, padx=10, pady=5)

    Label(form_inner, text="Socio *", font=('Segoe UI', 10, 'bold'), bg=co1, fg=co0).grid(row=row, column=2, sticky=W, pady=5)
    e_socio = Entry(form_inner, width=30, font=('Segoe UI', 10), relief='solid', bd=2)
    e_socio.grid(row=row, column=3, sticky=EW, padx=10, pady=5)
    row += 1

    Label(form_inner, text="Contato *", font=('Segoe UI', 10, 'bold'), bg=co1, fg=co0).grid(row=row, column=0, sticky=W, pady=5)
    e_contato = Entry(form_inner, width=30, font=('Segoe UI', 10), relief='solid', bd=2)
    e_contato.grid(row=row, column=1, sticky=EW, padx=10, pady=5)

    Label(form_inner, text="Tipo de Pessoa *", font=('Segoe UI', 10, 'bold'), bg=co1, fg=co0).grid(row=row, column=2, sticky=W, pady=5)
    combo_tipo_pessoa = ttk.Combobox(form_inner, width=15, values=["Pessoa Fisica", "Empresa"], font=('Segoe UI', 10))
    combo_tipo_pessoa.grid(row=row, column=3, sticky=W, padx=10, pady=5)
    row += 1

    Label(form_inner, text="Tipo de Telefone *", font=('Segoe UI', 10, 'bold'), bg=co1, fg=co0).grid(row=row, column=0, sticky=W, pady=5)
    combo_tipo_telefone = ttk.Combobox(form_inner, width=15, values=["Gerente", "Responsavel"], font=('Segoe UI', 10))
    combo_tipo_telefone.grid(row=row, column=1, sticky=W, padx=10, pady=5)

    Label(form_inner, text="Empresas Representadas", font=('Segoe UI', 10, 'bold'), bg=co1, fg=co0).grid(row=row, column=2, sticky=W, pady=5)
    e_empresas_representadas = Entry(form_inner, width=30, font=('Segoe UI', 10), relief='solid', bd=2)
    e_empresas_representadas.grid(row=row, column=3, sticky=EW, padx=10, pady=5)
    row += 1

    Label(form_inner, text="Socio da empresa 1", font=('Segoe UI', 10, 'bold'), bg=co1, fg=co0).grid(row=row, column=0, sticky=W, pady=5)
    e_empresa_associada_1 = Entry(form_inner, width=30, font=('Segoe UI', 10), relief='solid', bd=2)
    e_empresa_associada_1.grid(row=row, column=1, sticky=EW, padx=10, pady=5)

    Label(form_inner, text="Socio da empresa 2", font=('Segoe UI', 10, 'bold'), bg=co1, fg=co0).grid(row=row, column=2, sticky=W, pady=5)
    e_empresa_associada_2 = Entry(form_inner, width=30, font=('Segoe UI', 10), relief='solid', bd=2)
    e_empresa_associada_2.grid(row=row, column=3, sticky=EW, padx=10, pady=5)
    row += 1

    Label(form_inner, text="Socio da empresa 3", font=('Segoe UI', 10, 'bold'), bg=co1, fg=co0).grid(row=row, column=0, sticky=W, pady=5)
    e_empresa_associada_3 = Entry(form_inner, width=30, font=('Segoe UI', 10), relief='solid', bd=2)
    e_empresa_associada_3.grid(row=row, column=1, sticky=EW, padx=10, pady=5)

    Label(form_inner, text="Email", font=('Segoe UI', 10, 'bold'), bg=co1, fg=co0).grid(row=row, column=2, sticky=W, pady=5)
    e_email = Entry(form_inner, width=30, font=('Segoe UI', 10), relief='solid', bd=2)
    e_email.grid(row=row, column=3, sticky=EW, padx=10, pady=5)
    row += 1

    row += 1
    
    # Botoes
    button_frame = Frame(form_inner, bg=co1)
    button_frame.grid(row=row, column=0, columnspan=4, pady=20)
    
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
        
        # Cabeçalhos da tabela sem os campos do solicitante
        list_header = ['CNPJ', 'Nome', 'Município', 'Sócio', 'Contato', 'Tipo Pessoa', 'Tipo Telefone', 'Empresas Representadas', 'Socio da empresa 1', 'Socio da empresa 2', 'Socio da empresa 3', 'Email']
        df_list = ver_dados_contadores()

        global tree_dados_contadores
        
        tree_frame = Frame(table_frame, bg=co1)
        tree_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        tree_dados_contadores = ttk.Treeview(tree_frame, selectmode="extended", columns=list_header, show="headings", height=10)
        
        # Scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree_dados_contadores.yview)
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree_dados_contadores.xview)
        tree_dados_contadores.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        tree_dados_contadores.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')

        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        # Configurar colunas com larguras otimizadas
        widths = [120, 180, 120, 120, 120, 100, 100, 150, 150, 150, 150]
        for i, col in enumerate(list_header):
            tree_dados_contadores.heading(col, text=col, anchor=W)
            tree_dados_contadores.column(col, width=widths[i], anchor=W)

        # Inserir dados com cores alternadas (sem os campos do solicitante)
        for i, item in enumerate(df_list):
            # Exibir apenas os campos do contador na tabela
            item_display = [
                item[0],  # CNPJ
                item[1],  # Nome
                item[2],  # Município
                item[3],  # Sócio
                item[4],  # Contato
                item[5],  # Tipo Pessoa
                item[6],  # Tipo Telefone
                item[7] if item[7] else "N/A",  # Empresas Representadas
                item[8] if item[8] else "N/A",  # Socio da empresa 1
                item[9] if item[9] else "N/A",  # Socio da empresa 2
                item[10] if item[10] else "N/A",  # Socio da empresa 3
                item[11] if item[11] else "N/A"  # Email
            ]
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            tree_dados_contadores.insert('', 'end', values=item_display, tags=(tag,))
        
        # Configurar tags para cores alternadas
        tree_dados_contadores.tag_configure('evenrow', background=co5)
        tree_dados_contadores.tag_configure('oddrow', background=co1)
        
        # Adicionar evento de duplo clique para carregar dados no formulário
        def on_item_double_click(event):
            try:
                selected_item = tree_dados_contadores.selection()[0]
                values = tree_dados_contadores.item(selected_item, 'values')
                
                # Carregar dados nos campos do formulário
                e_cnpj.delete(0, END)
                e_cnpj.insert(0, values[0])
                e_nome.delete(0, END)
                e_nome.insert(0, values[1])
                e_municipio.delete(0, END)
                e_municipio.insert(0, values[2])
                e_socio.delete(0, END)
                e_socio.insert(0, values[3])
                e_contato.delete(0, END)
                e_contato.insert(0, values[4])
                combo_tipo_pessoa.set(values[5])
                combo_tipo_telefone.set(values[6])
                e_empresas_representadas.delete(0, END)
                e_empresas_representadas.insert(0, values[7] if values[7] != "N/A" else "")
                e_empresa_associada_1.delete(0, END)
                e_empresa_associada_1.insert(0, values[8] if values[8] != "N/A" else "")
                e_empresa_associada_2.delete(0, END)
                e_empresa_associada_2.insert(0, values[9] if values[9] != "N/A" else "")
                e_empresa_associada_3.delete(0, END)
                e_empresa_associada_3.insert(0, values[10] if values[10] != "N/A" else "")
                
            except IndexError:
                pass
        
        tree_dados_contadores.bind('<Double-1>', on_item_double_click)

    # Funcoes CRUD
    def novo_cadastro_contador():
        cnpj = e_cnpj.get()
        nome = e_nome.get()
        municipio = e_municipio.get()
        socio = e_socio.get()
        contato = e_contato.get()
        tipo_pessoa = combo_tipo_pessoa.get()
        tipo_telefone = combo_tipo_telefone.get()
        empresas_representadas = e_empresas_representadas.get()
        empresa_associada_1 = e_empresa_associada_1.get()
        empresa_associada_2 = e_empresa_associada_2.get()
        empresa_associada_3 = e_empresa_associada_3.get()
        
        lista = [cnpj, nome, municipio, socio, contato, tipo_pessoa, tipo_telefone, empresas_representadas, empresa_associada_1, empresa_associada_2, empresa_associada_3]

        # Verificar campos obrigatórios
        campos_obrigatorios = [cnpj, nome, municipio, socio, contato, tipo_pessoa, tipo_telefone]
        if any(campo == "" for campo in campos_obrigatorios):
            messagebox.showerror('Erro', 'Preencha todos os campos obrigatórios (*)')
            return
            
        try:
            criar_contador_novo(lista)
            messagebox.showinfo('Sucesso', 'Os dados foram inseridos com sucesso')

            # Limpar campos
            for entry in [e_cnpj, e_nome, e_municipio, e_socio, e_contato, e_empresas_representadas, e_empresa_associada_1, e_empresa_associada_2, e_empresa_associada_3]:
                entry.delete(0, END)
            combo_tipo_pessoa.set("")
            combo_tipo_telefone.set("")

            mostrar_dados_contadores()
        except sqlite3.IntegrityError:
            messagebox.showerror('Erro', 'CNPJ ja cadastrado!')

    def atualizar_contador_func():
        try:
            selected_item = tree_dados_contadores.selection()[0]
            cnpj_selecionado = tree_dados_contadores.item(selected_item, 'values')[0]
            
            dados = {
                'nome': e_nome.get(),
                'municipio': e_municipio.get(),
                'socio': e_socio.get(),
                'contato': e_contato.get(),
                'tipo_pessoa': combo_tipo_pessoa.get(),
                'tipo_telefone': combo_tipo_telefone.get(),
                'empresas_representadas': e_empresas_representadas.get(),
                'empresa_associada_1': e_empresa_associada_1.get(),
                'empresa_associada_2': e_empresa_associada_2.get(),
                'empresa_associada_3': e_empresa_associada_3.get()
            }
            
            # Verificar campos obrigatórios
            campos_obrigatorios = ['nome', 'municipio', 'socio', 'contato', 'tipo_pessoa', 'tipo_telefone']
            if any(dados[campo] == "" for campo in campos_obrigatorios):
                messagebox.showerror('Erro', 'Preencha todos os campos obrigatórios (*)')
                return
                
            atualizar_contador_novo(cnpj_selecionado, **dados)
            
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

#---- PREENCHIMENTO AUTOMÁTICO DE PDF
def preenchimento_pdf():
    # Limpar frames
    for widget in frame_content.winfo_children():
        widget.destroy()
    for widget in frame_data_display.winfo_children():
        widget.destroy()
    
    aba_ativa.set("preenchimento")
    atualizar_navegacao()
    
    # Container principal com scroll
    main_container = Frame(frame_content, bg=co1, relief="solid", bd=1)
    main_container.pack(fill=BOTH, expand=True, padx=10, pady=10)
    
    # Canvas para scroll
    canvas = Canvas(main_container, bg=co1)
    scrollbar = Scrollbar(main_container, orient="vertical", command=canvas.yview)
    scrollable_frame = Frame(canvas, bg=co1)
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    # Titulo da secao
    title_frame = Frame(scrollable_frame, bg=co8, height=50)
    title_frame.pack(fill=X, padx=5, pady=5)
    title_frame.pack_propagate(False)
    section_title = Label(title_frame, text="Preenchimento Automático de PDF Empresa", 
                         font=('Segoe UI', 16, 'bold'), bg=co8, fg=co1)
    section_title.pack(pady=12)
    
    # Frame de seleção individual
    selection_frame = LabelFrame(scrollable_frame, text="Opção 1: Selecionar REPIS Individual", 
                                font=('Segoe UI', 12, 'bold'), bg=co1, fg=co0,
                                relief="solid", bd=1)
    selection_frame.pack(fill=X, padx=10, pady=5)
    
    selection_inner = Frame(selection_frame, bg=co1)
    selection_inner.pack(fill=X, padx=10, pady=10)
    
    # Seleção de CNPJ REPIS
    Label(selection_inner, text="Selecionar CNPJ Empresa:", font=('Segoe UI', 10, 'bold'), bg=co1, fg=co0).grid(row=0, column=0, sticky=W, padx=5, pady=5)
    
    # Buscar todos os CNPJs das empresas
    dados_empresas = ver_dados_empresas()
    cnpjs_empresas = [item[0] for item in dados_empresas]
    
    combo_cnpj_empresa = ttk.Combobox(selection_inner, width=25, values=cnpjs_empresas, font=('Segoe UI', 10))
    combo_cnpj_empresa.grid(row=0, column=1, padx=10, pady=5)
    
    # Campo de busca ao lado
    Label(selection_inner, text="OU Buscar:", font=('Segoe UI', 10, 'bold'), bg=co1, fg=co0).grid(row=0, column=2, sticky=W, padx=5, pady=5)
    e_busca_repis = Entry(selection_inner, width=20, font=('Segoe UI', 10), relief='solid', bd=2)
    e_busca_repis.grid(row=0, column=3, padx=5, pady=5)
    
    def buscar_empresa():
        termo = e_busca_repis.get().strip()
        if not termo:
            messagebox.showerror('Erro', 'Digite um termo para buscar')
            return
        
        # Buscar na tabela de empresas
        resultado = buscar_empresa_por_cnpj(termo)
        if resultado:
            combo_cnpj_empresa.set(resultado[0])  # Definir o CNPJ encontrado no combo
            messagebox.showinfo('Sucesso', f'Empresa encontrada: {resultado[1]}')
        else:
            messagebox.showwarning('Aviso', 'Empresa não encontrada!')
    search_btn_repis = criar_botao_moderno(selection_inner, 'Buscar', buscar_empresa, co8)
    search_btn_repis.grid(row=0, column=4, padx=10)
    

    dados_contadores = ver_dados_contadores()
    cnpjs_contadores = [item[0] for item in dados_contadores]
    
    combo_cnpj_contador = ttk.Combobox(selection_inner, width=25, values=cnpjs_contadores, font=('Segoe UI', 10))
    combo_cnpj_contador.grid(row=1, column=1, padx=10, pady=5)
    
    # Campo de busca ao lado
    Label(selection_inner, text="OU Buscar:", font=('Segoe UI', 10, 'bold'), bg=co1, fg=co0).grid(row=1, column=2, sticky=W, padx=5, pady=5)
    e_busca_contador = Entry(selection_inner, width=20, font=('Segoe UI', 10), relief='solid', bd=2)
    e_busca_contador.grid(row=1, column=3, padx=5, pady=5)
    
    def buscar_contador():
        termo = e_busca_contador.get().strip()
        if not termo:
            messagebox.showerror('Erro', 'Digite um termo para buscar')
            return
        
        # Buscar contador por CNPJ ou nome
        resultado = buscar_contador_por_cnpj_ou_nome(termo)
        if resultado:
            combo_cnpj_contador.set(resultado[0])  # Definir o CNPJ encontrado no combo
            messagebox.showinfo('Sucesso', f'Contador encontrado: {resultado[1]}')
        else:
            messagebox.showwarning('Aviso', 'Contador não encontrado!')
    
    search_btn_contador = criar_botao_moderno(selection_inner, 'Buscar', buscar_contador, co8)
    search_btn_contador.grid(row=1, column=4, padx=10)
    
    # NOVA FUNCIONALIDADE: Frame de seleção por contador
    contador_frame = LabelFrame(scrollable_frame, text="Opção 2: Selecionar Contador e Empresas Vinculadas", 
                               font=('Segoe UI', 12, 'bold'), bg=co1, fg=co0,
                               relief="solid", bd=1)
    contador_frame.pack(fill=X, padx=10, pady=5)
    
    contador_inner = Frame(contador_frame, bg=co1)
    contador_inner.pack(fill=X, padx=10, pady=10)
    
    # Seleção de contador
    Label(contador_inner, text="Selecionar Contador:", font=('Segoe UI', 10, 'bold'), bg=co1, fg=co0).grid(row=0, column=0, sticky=W, padx=5, pady=5)
    
    combo_contador_empresas = ttk.Combobox(contador_inner, width=40, values=cnpjs_contadores, font=('Segoe UI', 10))
    combo_contador_empresas.grid(row=0, column=1, padx=10, pady=5)
    
    # Campo de busca para contador
    Label(contador_inner, text="OU Buscar:", font=('Segoe UI', 10, 'bold'), bg=co1, fg=co0).grid(row=0, column=2, sticky=W, padx=5, pady=5)
    e_busca_contador_empresas = Entry(contador_inner, width=20, font=('Segoe UI', 10), relief='solid', bd=2)
    e_busca_contador_empresas.grid(row=0, column=3, padx=5, pady=5)
    
    def buscar_contador_empresas():
        termo = e_busca_contador_empresas.get().strip()
        if not termo:
            messagebox.showerror('Erro', 'Digite um termo para buscar')
            return
        
        # Buscar contador por CNPJ ou nome
        resultado = buscar_contador_por_cnpj_ou_nome(termo)
        if resultado:
            combo_contador_empresas.set(resultado[0])  # Definir o CNPJ encontrado no combo
            carregar_empresas_contador()  # Carregar empresas automaticamente
            messagebox.showinfo('Sucesso', f'Contador encontrado: {resultado[1]}')
        else:
            messagebox.showwarning('Aviso', 'Contador não encontrado!')
    
    search_btn_contador_empresas = criar_botao_moderno(contador_inner, 'Buscar', buscar_contador_empresas, co9)
    search_btn_contador_empresas.grid(row=0, column=4, padx=10)
    
    # Botão para carregar empresas
    btn_carregar_empresas = criar_botao_moderno(contador_inner, 'Carregar Empresas', lambda: carregar_empresas_contador(), co9)
    btn_carregar_empresas.grid(row=0, column=5, padx=10)
    
    # Frame para exibir empresas vinculadas
    empresas_frame = LabelFrame(contador_inner, text="Empresas Vinculadas ao Contador", 
                               font=('Segoe UI', 11, 'bold'), bg=co1, fg=co0,
                               relief="solid", bd=1)
    empresas_frame.grid(row=1, column=0, columnspan=6, sticky=EW, padx=5, pady=10)
    
    empresas_inner = Frame(empresas_frame, bg=co1)
    empresas_inner.pack(fill=BOTH, expand=True, padx=10, pady=10)
    
    # Variáveis para checkboxes das empresas
    empresas_vars = {}
    empresas_checkboxes = {}
    
    def carregar_empresas_contador():
        # Limpar empresas anteriores
        for widget in empresas_inner.winfo_children():
            widget.destroy()
        empresas_vars.clear()
        empresas_checkboxes.clear()
        
        cnpj_contador = combo_contador_empresas.get().strip()
        if not cnpj_contador:
            Label(empresas_inner, text="Selecione um contador para ver as empresas vinculadas", 
                  font=('Segoe UI', 10), bg=co1, fg=co0).pack(pady=10)
            return
        
        # Buscar empresas vinculadas ao contador
        try:
            empresas = buscar_empresas_por_contador(cnpj_contador)
            
            if not empresas:
                Label(empresas_inner, text="Nenhuma empresa vinculada a este contador", 
                      font=('Segoe UI', 10), bg=co1, fg=co0).pack(pady=10)
                return
            
            # Botões para selecionar/desselecionar todas
            botoes_frame = Frame(empresas_inner, bg=co1)
            botoes_frame.pack(fill=X, pady=5)
            
            def selecionar_todas():
                for var in empresas_vars.values():
                    var.set(True)
            
            def desselecionar_todas():
                for var in empresas_vars.values():
                    var.set(False)
            
            btn_selecionar_todas = criar_botao_moderno(botoes_frame, 'Selecionar Todas', selecionar_todas, co3)
            btn_selecionar_todas.pack(side=LEFT, padx=5)
            
            btn_desselecionar_todas = criar_botao_moderno(botoes_frame, 'Desselecionar Todas', desselecionar_todas, co4)
            btn_desselecionar_todas.pack(side=LEFT, padx=5)
            
            # Lista de empresas com checkboxes
            Label(empresas_inner, text=f"Empresas encontradas ({len(empresas)}):", 
                  font=('Segoe UI', 10, 'bold'), bg=co1, fg=co0).pack(anchor=W, pady=(10,5))
            
            for i, empresa in enumerate(empresas):
                empresa_frame = Frame(empresas_inner, bg=co5, relief="solid", bd=1)
                empresa_frame.pack(fill=X, pady=2, padx=5)
                
                # Checkbox
                var = BooleanVar()
                empresas_vars[empresa[0]] = var  # CNPJ como chave
                
                checkbox = Checkbutton(empresa_frame, variable=var, bg=co5, font=('Segoe UI', 9))
                checkbox.pack(side=LEFT, padx=5, pady=5)
                empresas_checkboxes[empresa[0]] = checkbox
                
                # Informações da empresa
                info_text = f"CNPJ: {empresa[0]} | Razão Social: {empresa[1] or 'N/A'} | Município: {empresa[9] or 'N/A'}"
                Label(empresa_frame, text=info_text, font=('Segoe UI', 9), bg=co5, fg=co0).pack(side=LEFT, padx=5, pady=5)
            
        except Exception as e:
            messagebox.showerror('Erro', f'Erro ao buscar empresas: {str(e)}')
            Label(empresas_inner, text="Erro ao carregar empresas", 
                  font=('Segoe UI', 10), bg=co1, fg=co4).pack(pady=10)
    
    # Frame de preview e ações
    preview_frame = LabelFrame(scrollable_frame, text="Preview e Ações", 
                              font=('Segoe UI', 12, 'bold'), bg=co1, fg=co0,
                              relief="solid", bd=1)
    preview_frame.pack(fill=BOTH, expand=True, padx=10, pady=5)
    
    preview_inner = Frame(preview_frame, bg=co1)
    preview_inner.pack(fill=BOTH, expand=True, padx=10, pady=10)
    
    # Área de preview
    Label(preview_inner, text="Preview dos Dados:", font=('Segoe UI', 11, 'bold'), bg=co1, fg=co0).pack(anchor=W, pady=(0,5))
    
    preview_text = Text(preview_inner, font=('Segoe UI', 9), 
                       relief='solid', bd=2, bg=co5, fg=co0)
    preview_text.pack(fill=BOTH, expand=True, pady=5)
    
    # Scrollbar para o preview
    preview_scrollbar = Scrollbar(preview_inner, orient="vertical", command=preview_text.yview)
    preview_text.configure(yscrollcommand=preview_scrollbar.set)
    preview_scrollbar.pack(side="right", fill="y")
    
    # Funções para preview e geração de PDF
    def carregar_preview():
        cnpj_repis = combo_cnpj_repis.get()
        cnpj_contador = combo_cnpj_contador.get()
        
        if not cnpj_repis:
            messagebox.showerror('Erro', 'Selecione um CNPJ REPIS')
            return
        
        # Buscar dados do REPIS
        dados_repis = buscar_repis_por_cnpj(cnpj_repis)
        dados_contador = None
        
        if cnpj_contador:
            dados_contador = buscar_contador_por_cnpj_ou_nome(cnpj_contador)
        
        # Montar preview
        preview_text.delete(1.0, END)
        
        if dados_repis:
            preview_content = f"""DADOS REPIS SELECIONADOS:
CNPJ: {dados_repis[0]}
Razão Social: {dados_repis[1] or 'N/A'}
Nome Fantasia: {dados_repis[2] or 'N/A'}
Endereço: {dados_repis[3] or 'N/A'}
CEP: {dados_repis[5] or 'N/A'}
E-mail: {dados_repis[6] or 'N/A'}
Bairro: {dados_repis[7] or 'N/A'}
UF: {dados_repis[8] or 'N/A'}
Município: {dados_repis[9] or 'N/A'}
Data de Abertura: {dados_repis[10] or 'N/A'}
Nome do Solicitante: {dados_repis[11] or 'N/A'}
Tipo de Solicitante: {dados_repis[12] or 'N/A'}
Telefone: {dados_repis[13] or 'N/A'}
Email do Solicitante: {dados_repis[14] or 'N/A'}
CPF: {dados_repis[15] or 'N/A'}
RG: {dados_repis[16] or 'N/A'}
Contador: {dados_repis[17] or 'N/A'}
Telefone do Contador: {dados_repis[18] or 'N/A'}
Email do Contador: {dados_repis[19] or 'N/A'}

"""
            
            if dados_contador:
                preview_content += f"""DADOS CONTADOR SELECIONADOS:
CNPJ: {dados_contador[0]}
Nome: {dados_contador[1] or 'N/A'}
Município: {dados_contador[2] or 'N/A'}
Sócio: {dados_contador[3] or 'N/A'}
Contato: {dados_contador[4] or 'N/A'}
Tipo de Pessoa: {dados_contador[5] or 'N/A'}
Tipo de Telefone: {dados_contador[6] or 'N/A'}
Empresas Representadas: {dados_contador[7] or 'N/A'}
Socio da empresa 1: {dados_contador[8] or 'N/A'}
Socio da empresa 2: {dados_contador[9] or 'N/A'}
Socio da empresa 3: {dados_contador[10] or 'N/A'}
"""
            
            preview_text.insert(1.0, preview_content)
        else:
            preview_text.insert(1.0, "Dados não encontrados para o CNPJ selecionado.")
    
    def gerar_pdf_preenchido():
        cnpj_repis = combo_cnpj_repis.get()
        cnpj_contador = combo_cnpj_contador.get()
        
        if not cnpj_repis:
            messagebox.showerror('Erro', 'Selecione um CNPJ REPIS')
            return
        
        # Buscar dados
        dados_repis_raw = buscar_repis_por_cnpj(cnpj_repis)
        dados_contador_raw = None
        
        if cnpj_contador:
            dados_contador_raw = buscar_contador_por_cnpj_ou_nome(cnpj_contador)
        
        if not dados_repis_raw:
            # Se não encontrou no REPIS, buscar dados da empresa na tabela empresas
            dados_empresa_raw = buscar_empresa_por_cnpj(cnpj_repis)
            if dados_empresa_raw:
                # Criar dados REPIS baseados nos dados da empresa
                dados_repis_raw = [
                    dados_empresa_raw[0],  # cnpj
                    dados_empresa_raw[1],  # razao_social
                    dados_empresa_raw[2],  # nome_fantasia
                    dados_empresa_raw[3],  # endereco
                    dados_empresa_raw[4],  # complemento
                    dados_empresa_raw[5],  # cep
                    dados_empresa_raw[6],  # email
                    dados_empresa_raw[7],  # bairro
                    dados_empresa_raw[8],  # uf
                    dados_empresa_raw[9],  # municipio
                    dados_empresa_raw[12], # data_abertura
                    dados_empresa_raw[14], # responsavel como nome_solicitante
                    "Sócio",               # solicitante_tipo padrão
                    dados_empresa_raw[10], # telefone
                    dados_empresa_raw[16], # email_responsavel como email_solicitante
                    "",                    # cpf (vazio)
                    "",                    # rg (vazio)
                    dados_contador_raw[1] if dados_contador_raw else "", # contador
                    dados_contador_raw[4] if dados_contador_raw else "", # telefone_contador
                    ""                     # email_contador (vazio)
                ]
        
        if dados_repis_raw:
            # Converter para dicionário
            dados_repis = {
                'cnpj': dados_repis_raw[0],
                'razao_social': dados_repis_raw[1],
                'nome_fantasia': dados_repis_raw[2],
                'endereco': dados_repis_raw[3],
                'complemento': dados_repis_raw[4],
                'cep': dados_repis_raw[5],
                'email': dados_repis_raw[6],
                'bairro': dados_repis_raw[7],
                'uf': dados_repis_raw[8],
                'municipio': dados_repis_raw[9],
                'data_abertura': dados_repis_raw[10],
                'nome_solicitante': dados_repis_raw[11],
                'solicitante_tipo': dados_repis_raw[12],
                'telefone': dados_repis_raw[13],
                'email_solicitante': dados_repis_raw[14],
                'cpf': dados_repis_raw[15],
                'rg': dados_repis_raw[16],
                'contador': dados_repis_raw[17],
                'telefone_contador': dados_repis_raw[18],
                'email_contador': dados_repis_raw[19]
            }
            
            dados_contador = None
            if dados_contador_raw:
                dados_contador = {
                    'cnpj': dados_contador_raw[0],
                    'nome': dados_contador_raw[1],
                    'municipio': dados_contador_raw[2],
                    'socio': dados_contador_raw[3],
                    'contato': dados_contador_raw[4],
                    'tipo_pessoa': dados_contador_raw[5],
                    'tipo_telefone': dados_contador_raw[6],
                    'empresas_representadas': dados_contador_raw[7],
                    'empresa_associada_1': dados_contador_raw[8],
                    'empresa_associada_2': dados_contador_raw[9],
                    'empresa_associada_3': dados_contador_raw[10]
                }
            
            # Gerar PDF
            try:
                from pdf_filler import processar_preenchimento_pdf_novo
                arquivo_gerado = processar_preenchimento_pdf_novo(dados_repis, dados_contador)
                if arquivo_gerado:
                    messagebox.showinfo('Sucesso', f'PDF gerado com sucesso: {arquivo_gerado}')
            except Exception as e:
                messagebox.showerror('Erro', f'Erro ao gerar PDF: {str(e)}')
        else:
            messagebox.showerror('Erro', 'Dados não encontrados para o CNPJ selecionado')
    
    def gerar_pdfs_empresas_selecionadas():
        """Gera PDFs para todas as empresas selecionadas do contador"""
        cnpj_contador = combo_contador_empresas.get().strip()
        
        if not cnpj_contador:
            messagebox.showerror('Erro', 'Selecione um contador primeiro')
            return
        
        # Verificar quais empresas estão selecionadas
        empresas_selecionadas = []
        for cnpj_empresa, var in empresas_vars.items():
            if var.get():  # Se checkbox está marcado
                empresas_selecionadas.append(cnpj_empresa)
        
        if not empresas_selecionadas:
            messagebox.showerror('Erro', 'Selecione pelo menos uma empresa')
            return
        
        # Buscar dados do contador
        dados_contador_raw = buscar_contador_por_cnpj_ou_nome(cnpj_contador)
        if not dados_contador_raw:
            messagebox.showerror('Erro', 'Dados do contador não encontrados')
            return
        
        dados_contador = {
            'cnpj': dados_contador_raw[0],
            'nome': dados_contador_raw[1],
            'municipio': dados_contador_raw[2],
            'socio': dados_contador_raw[3],
            'contato': dados_contador_raw[4],
            'tipo_pessoa': dados_contador_raw[5],
            'tipo_telefone': dados_contador_raw[6],
            'empresas_representadas': dados_contador_raw[7],
            'empresa_associada_1': dados_contador_raw[8],
            'empresa_associada_2': dados_contador_raw[9],
            'empresa_associada_3': dados_contador_raw[10]
        }
        
        # Gerar PDF para cada empresa selecionada
        arquivos_gerados = []
        erros = []
        
        for cnpj_empresa in empresas_selecionadas:
            try:
                # Buscar dados da empresa no REPIS
                dados_repis_raw = buscar_repis_por_cnpj(cnpj_empresa)
                
                if not dados_repis_raw:
                    # Se não encontrou no REPIS, buscar dados da empresa na tabela empresas
                    dados_empresa_raw = buscar_empresa_por_cnpj(cnpj_empresa)
                    if dados_empresa_raw:
                        # Criar dados REPIS baseados nos dados da empresa
                        dados_repis_raw = [
                            dados_empresa_raw[0],  # cnpj
                            dados_empresa_raw[1],  # razao_social
                            dados_empresa_raw[2],  # nome_fantasia
                            dados_empresa_raw[3],  # endereco
                            dados_empresa_raw[4],  # complemento
                            dados_empresa_raw[5],  # cep
                            dados_empresa_raw[6],  # email
                            dados_empresa_raw[7],  # bairro
                            dados_empresa_raw[8],  # uf
                            dados_empresa_raw[9],  # municipio
                            dados_empresa_raw[12], # data_abertura
                            dados_empresa_raw[14], # responsavel como nome_solicitante
                            "Sócio",               # solicitante_tipo padrão
                            dados_empresa_raw[10], # telefone
                            dados_empresa_raw[16], # email_responsavel como email_solicitante
                            "",                    # cpf (vazio)
                            "",                    # rg (vazio)
                            dados_contador['nome'] if dados_contador else "", # contador
                            dados_contador['contato'] if dados_contador else "", # telefone_contador
                            ""                     # email_contador (vazio)
                        ]
                
                if dados_repis_raw:
                    dados_repis = {
                        'cnpj': dados_repis_raw[0],
                        'razao_social': dados_repis_raw[1],
                        'nome_fantasia': dados_repis_raw[2],
                        'endereco': dados_repis_raw[3],
                        'complemento': dados_repis_raw[4],
                        'cep': dados_repis_raw[5],
                        'email': dados_repis_raw[6],
                        'bairro': dados_repis_raw[7],
                        'uf': dados_repis_raw[8],
                        'municipio': dados_repis_raw[9],
                        'data_abertura': dados_repis_raw[10],
                        'nome_solicitante': dados_repis_raw[11],
                        'solicitante_tipo': dados_repis_raw[12],
                        'telefone': dados_repis_raw[13],
                        'email_solicitante': dados_repis_raw[14],
                        'cpf': dados_repis_raw[15],
                        'rg': dados_repis_raw[16],
                        'contador': dados_repis_raw[17],
                        'telefone_contador': dados_repis_raw[18],
                        'email_contador': dados_repis_raw[19]
                    }
                    
                    # Gerar PDF
                    from pdf_filler import processar_preenchimento_pdf_novo
                    arquivo_gerado = processar_preenchimento_pdf_novo(dados_repis, dados_contador)
                    if arquivo_gerado:
                        arquivos_gerados.append(arquivo_gerado)
                else:
                    erros.append(f'Dados REPIS não encontrados para CNPJ: {cnpj_empresa}')
                    
            except Exception as e:
                erros.append(f'Erro ao gerar PDF para {cnpj_empresa}: {str(e)}')
        
        # Mostrar resultado
        if arquivos_gerados:
            resultado = f'PDFs gerados com sucesso ({len(arquivos_gerados)}):\\n'
            for arquivo in arquivos_gerados:
                resultado += f'- {arquivo}\\n'
            
            if erros:
                resultado += f'\\nErros encontrados ({len(erros)}):\\n'
                for erro in erros:
                    resultado += f'- {erro}\\n'
            
            messagebox.showinfo('Resultado', resultado)
        else:
            messagebox.showerror('Erro', f'Nenhum PDF foi gerado.\\nErros:\\n' + '\\n'.join(erros))
    
    # Botões
    button_frame = Frame(scrollable_frame, bg=co1)
    button_frame.pack(fill=X, padx=10, pady=20)
    
    # Botões para opção 1 (REPIS individual)
    Label(button_frame, text="Opção 1 - REPIS Individual:", font=('Segoe UI', 11, 'bold'), bg=co1, fg=co0).pack(anchor=W, pady=(0,5))
    
    botoes_opcao1 = Frame(button_frame, bg=co1)
    botoes_opcao1.pack(fill=X, pady=5)
    
    btn_preview = criar_botao_moderno(botoes_opcao1, "Carregar Preview", carregar_preview, co2, 15)
    btn_preview.pack(side=LEFT, padx=5)
    
    btn_gerar = criar_botao_moderno(botoes_opcao1, "Gerar PDF Preenchido", gerar_pdf_preenchido, co3, 20)
    btn_gerar.pack(side=LEFT, padx=5)
    
    # Botões para opção 2 (Contador e empresas)
    Label(button_frame, text="Opção 2 - Contador e Empresas:", font=('Segoe UI', 11, 'bold'), bg=co1, fg=co0).pack(anchor=W, pady=(20,5))
    
    botoes_opcao2 = Frame(button_frame, bg=co1)
    botoes_opcao2.pack(fill=X, pady=5)
    
    btn_gerar_multiplos = criar_botao_moderno(botoes_opcao2, "Gerar PDFs das Empresas Selecionadas", gerar_pdfs_empresas_selecionadas, co9, 30)
    btn_gerar_multiplos.pack(side=LEFT, padx=5)

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
    
    section_title = Label(title_frame, text="Opcoes de Exportacao", 
                         font=('Segoe UI', 16, 'bold'), bg=co7, fg=co1)
    section_title.pack(pady=12)
    
    # Frame de opcoes
    options_frame = Frame(main_container, bg=co1)
    options_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)
    
    # Selecao de tabela
    Label(options_frame, text="Selecione a tabela:", font=('Segoe UI', 12, 'bold'), bg=co1, fg=co0).pack(pady=10)
    combo_tabela = ttk.Combobox(options_frame, width=20, values=["REPIS", "Contadores", "Empresas"], font=('Segoe UI', 12))
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
    
    # Informacoes sobre exportacao
    info_frame = Frame(options_frame, bg=co5, relief="solid", bd=1)
    info_frame.pack(fill=X, pady=20)
    
    Label(info_frame, text="Selecione a tabela para ser exportada", 
          font=('Segoe UI', 12, 'bold'), bg=co5, fg=co0).pack(pady=10)
    
    Label(info_frame, text="Escolha o formato desejado para exportar os dados cadastrados.", 
          font=('Segoe UI', 10), bg=co5, fg=co0, justify=CENTER).pack(pady=10)

#---- EMPRESAS com design moderno
def empresas():
    # Limpar frames
    for widget in frame_content.winfo_children():
        widget.destroy()
    for widget in frame_data_display.winfo_children():
        widget.destroy()
    
    aba_ativa.set("empresas")
    atualizar_navegacao()
    
    # Container principal com scroll
    main_container = Frame(frame_content, bg=co1, relief="solid", bd=1)
    main_container.pack(fill=BOTH, expand=True, padx=10, pady=10)
    
    # Canvas para scroll
    canvas = Canvas(main_container, bg=co1)
    scrollbar = Scrollbar(main_container, orient="vertical", command=canvas.yview)
    scrollable_frame = Frame(canvas, bg=co1)
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    # Titulo da secao
    title_frame = Frame(scrollable_frame, bg=co8, height=50)
    title_frame.pack(fill=X, padx=5, pady=5)
    title_frame.pack_propagate(False)
    
    section_title = Label(title_frame, text="Cadastro de Empresas", 
                         font=('Segoe UI', 16, 'bold'), bg=co8, fg=co1)
    section_title.pack(pady=12)
    
    # Frame de pesquisa estilizado
    search_frame = LabelFrame(scrollable_frame, text="Pesquisa por CNPJ", 
                             font=('Segoe UI', 12, 'bold'), bg=co1, fg=co0,
                             relief="solid", bd=1)
    search_frame.pack(fill=X, padx=10, pady=5)
    
    search_inner = Frame(search_frame, bg=co1)
    search_inner.pack(fill=X, padx=10, pady=10)
    
    Label(search_inner, text="CNPJ:", font=('Segoe UI', 10, 'bold'), bg=co1, fg=co0).grid(row=0, column=0, sticky=W, padx=5)
    e_pesquisa_emp = Entry(search_inner, width=25, font=('Segoe UI', 10), relief='solid', bd=2)
    e_pesquisa_emp.grid(row=0, column=1, padx=10, pady=5)
    
    def pesquisar_empresa():
        cnpj = e_pesquisa_emp.get()
        if cnpj:
            resultado = buscar_empresa_por_cnpj(cnpj)
            if resultado:
                # Preencher todos os campos
                e_cnpj.delete(0, END)
                e_cnpj.insert(0, resultado[0])
                e_razao_social.delete(0, END)
                e_razao_social.insert(0, resultado[1] if resultado[1] else "")
                e_nome_fantasia.delete(0, END)
                e_nome_fantasia.insert(0, resultado[2] if resultado[2] else "")
                e_endereco.delete(0, END)
                e_endereco.insert(0, resultado[3] if resultado[3] else "")
                e_complemento.delete(0, END)
                e_complemento.insert(0, resultado[4] if resultado[4] else "")
                e_cep.delete(0, END)
                e_cep.insert(0, resultado[5] if resultado[5] else "")
                e_email.delete(0, END)
                e_email.insert(0, resultado[6] if resultado[6] else "")
                e_bairro.delete(0, END)
                e_bairro.insert(0, resultado[7] if resultado[7] else "")
                combo_uf.set(resultado[8] if resultado[8] else "")
                e_municipio.delete(0, END)
                e_municipio.insert(0, resultado[9] if resultado[9] else "")
                e_telefone.delete(0, END)
                e_telefone.insert(0, resultado[10] if resultado[10] else "")
                e_atividade_principal.delete(0, END)
                e_atividade_principal.insert(0, resultado[11] if resultado[11] else "")
                e_data_abertura.delete(0, END)
                e_data_abertura.insert(0, resultado[12] if resultado[12] else "")
                combo_situacao.set(resultado[13] if resultado[13] else "")
                e_responsavel.delete(0, END)
                e_responsavel.insert(0, resultado[14] if resultado[14] else "")
                e_telefone_responsavel.delete(0, END)
                e_telefone_responsavel.insert(0, resultado[15] if resultado[15] else "")
                e_email_responsavel.delete(0, END)
                e_email_responsavel.insert(0, resultado[16] if resultado[16] else "")
                
                # Buscar contador associado à empresa
                contadores_associados = buscar_contadores_por_empresa(resultado[0])
                if contadores_associados:
                    contador_info = f"{contadores_associados[0][0]} - {contadores_associados[0][1]}"
                    combo_contador.set(contador_info)
                else:
                    combo_contador.set("")
                
                messagebox.showinfo('Sucesso', 'Dados encontrados!')
            else:
                messagebox.showwarning('Aviso', 'CNPJ nao encontrado!')
        else:
            messagebox.showerror('Erro', 'Digite um CNPJ para pesquisar')

    search_btn = criar_botao_moderno(search_inner, 'Pesquisar', pesquisar_empresa, co8)
    search_btn.grid(row=0, column=2, padx=10)
    
    # Frame do formulario com layout em grid moderno
    form_frame = LabelFrame(scrollable_frame, text="Dados da Empresa", 
                           font=('Segoe UI', 12, 'bold'), bg=co1, fg=co0,
                           relief="solid", bd=1)
    form_frame.pack(fill=BOTH, expand=True, padx=10, pady=5)
    
    form_inner = Frame(form_frame, bg=co1)
    form_inner.pack(fill=BOTH, expand=True, padx=15, pady=15)
    
    # Configurar grid
    form_inner.columnconfigure(1, weight=1)
    form_inner.columnconfigure(3, weight=1)
    
    # Campos do formulario com estilo moderno
    row = 0
    
    # Linha 1: CNPJ e Razão Social
    Label(form_inner, text="CNPJ *", font=('Segoe UI', 10, 'bold'), bg=co1, fg=co0).grid(row=row, column=0, sticky=W, pady=5)
    e_cnpj = Entry(form_inner, width=30, font=('Segoe UI', 10), relief='solid', bd=2)
    e_cnpj.grid(row=row, column=1, sticky=EW, padx=10, pady=5)

    Label(form_inner, text="Razão Social *", font=('Segoe UI', 10, 'bold'), bg=co1, fg=co0).grid(row=row, column=2, sticky=W, pady=5)
    e_razao_social = Entry(form_inner, width=30, font=('Segoe UI', 10), relief='solid', bd=2)
    e_razao_social.grid(row=row, column=3, sticky=EW, padx=10, pady=5)
    row += 1

    # Linha 2: Nome Fantasia e E-mail
    Label(form_inner, text="Nome Fantasia", font=('Segoe UI', 10, 'bold'), bg=co1, fg=co0).grid(row=row, column=0, sticky=W, pady=5)
    e_nome_fantasia = Entry(form_inner, width=30, font=('Segoe UI', 10), relief='solid', bd=2)
    e_nome_fantasia.grid(row=row, column=1, sticky=EW, padx=10, pady=5)

    Label(form_inner, text="E-mail", font=('Segoe UI', 10, 'bold'), bg=co1, fg=co0).grid(row=row, column=2, sticky=W, pady=5)
    e_email = Entry(form_inner, width=30, font=('Segoe UI', 10), relief='solid', bd=2)
    e_email.grid(row=row, column=3, sticky=EW, padx=10, pady=5)
    row += 1

    # Linha 3: Endereço
    Label(form_inner, text="Endereço", font=('Segoe UI', 10, 'bold'), bg=co1, fg=co0).grid(row=row, column=0, sticky=W, pady=5)
    e_endereco = Entry(form_inner, width=60, font=('Segoe UI', 10), relief='solid', bd=2)
    e_endereco.grid(row=row, column=1, columnspan=3, sticky=EW, padx=10, pady=5)
    row += 1

    # Linha 4: Complemento e CEP
    Label(form_inner, text="Complemento", font=('Segoe UI', 10, 'bold'), bg=co1, fg=co0).grid(row=row, column=0, sticky=W, pady=5)
    e_complemento = Entry(form_inner, width=30, font=('Segoe UI', 10), relief='solid', bd=2)
    e_complemento.grid(row=row, column=1, sticky=EW, padx=10, pady=5)

    Label(form_inner, text="CEP", font=('Segoe UI', 10, 'bold'), bg=co1, fg=co0).grid(row=row, column=2, sticky=W, pady=5)
    e_cep = Entry(form_inner, width=30, font=('Segoe UI', 10), relief='solid', bd=2)
    e_cep.grid(row=row, column=3, sticky=EW, padx=10, pady=5)
    row += 1

    # Linha 5: Bairro e UF
    Label(form_inner, text="Bairro", font=('Segoe UI', 10, 'bold'), bg=co1, fg=co0).grid(row=row, column=0, sticky=W, pady=5)
    e_bairro = Entry(form_inner, width=30, font=('Segoe UI', 10), relief='solid', bd=2)
    e_bairro.grid(row=row, column=1, sticky=EW, padx=10, pady=5)

    Label(form_inner, text="UF", font=('Segoe UI', 10, 'bold'), bg=co1, fg=co0).grid(row=row, column=2, sticky=W, pady=5)
    combo_uf = ttk.Combobox(form_inner, width=15, values=["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"], font=('Segoe UI', 10))
    combo_uf.grid(row=row, column=3, sticky=W, padx=10, pady=5)
    row += 1

    # Linha 6: Município e Telefone
    Label(form_inner, text="Município", font=('Segoe UI', 10, 'bold'), bg=co1, fg=co0).grid(row=row, column=0, sticky=W, pady=5)
    e_municipio = Entry(form_inner, width=30, font=('Segoe UI', 10), relief='solid', bd=2)
    e_municipio.grid(row=row, column=1, sticky=EW, padx=10, pady=5)

    Label(form_inner, text="Telefone", font=('Segoe UI', 10, 'bold'), bg=co1, fg=co0).grid(row=row, column=2, sticky=W, pady=5)
    e_telefone = Entry(form_inner, width=30, font=('Segoe UI', 10), relief='solid', bd=2)
    e_telefone.grid(row=row, column=3, sticky=EW, padx=10, pady=5)
    row += 1

    # Linha 7: Atividade Principal e Data de Abertura
    Label(form_inner, text="Atividade Principal", font=('Segoe UI', 10, 'bold'), bg=co1, fg=co0).grid(row=row, column=0, sticky=W, pady=5)
    e_atividade_principal = Entry(form_inner, width=30, font=('Segoe UI', 10), relief='solid', bd=2)
    e_atividade_principal.grid(row=row, column=1, sticky=EW, padx=10, pady=5)

    Label(form_inner, text="Data de Abertura", font=('Segoe UI', 10, 'bold'), bg=co1, fg=co0).grid(row=row, column=2, sticky=W, pady=5)
    e_data_abertura = Entry(form_inner, width=30, font=('Segoe UI', 10), relief='solid', bd=2)
    e_data_abertura.grid(row=row, column=3, sticky=EW, padx=10, pady=5)
    row += 1

    # Linha 8: Situação e Contador
    Label(form_inner, text="Situação", font=('Segoe UI', 10, 'bold'), bg=co1, fg=co0).grid(row=row, column=0, sticky=W, pady=5)
    combo_situacao = ttk.Combobox(form_inner, width=15, values=["Ativa", "Inativa", "Suspensa", "Baixada"], font=('Segoe UI', 10))
    combo_situacao.grid(row=row, column=1, sticky=W, padx=10, pady=5)
    
    # Campo para selecionar contador
    Label(form_inner, text="Contador", font=('Segoe UI', 10, 'bold'), bg=co1, fg=co0).grid(row=row, column=2, sticky=W, pady=5)
    
    # Buscar todos os contadores para popular o combobox
    dados_contadores = ver_dados_contadores()
    contadores_opcoes = [f"{item[0]} - {item[1]}" for item in dados_contadores]  # CNPJ - Nome
    
    combo_contador = ttk.Combobox(form_inner, width=30, values=contadores_opcoes, font=('Segoe UI', 10))
    combo_contador.grid(row=row, column=3, sticky=EW, padx=10, pady=5)
    row += 1

    # Separador
    separator = Frame(form_inner, bg=co6, height=2)
    separator.grid(row=row, column=0, columnspan=4, sticky=EW, pady=10)
    row += 1

    # Seção do Responsável
    Label(form_inner, text="DADOS DO RESPONSÁVEL", font=('Segoe UI', 12, 'bold'), bg=co1, fg=co2).grid(row=row, column=0, columnspan=4, pady=10)
    row += 1

    # Linha 9: Responsável e Telefone do Responsável
    Label(form_inner, text="Responsável", font=('Segoe UI', 10, 'bold'), bg=co1, fg=co0).grid(row=row, column=0, sticky=W, pady=5)
    e_responsavel = Entry(form_inner, width=30, font=('Segoe UI', 10), relief='solid', bd=2)
    e_responsavel.grid(row=row, column=1, sticky=EW, padx=10, pady=5)

    Label(form_inner, text="Telefone do Responsável", font=('Segoe UI', 10, 'bold'), bg=co1, fg=co0).grid(row=row, column=2, sticky=W, pady=5)
    e_telefone_responsavel = Entry(form_inner, width=30, font=('Segoe UI', 10), relief='solid', bd=2)
    e_telefone_responsavel.grid(row=row, column=3, sticky=EW, padx=10, pady=5)
    row += 1

    # Linha 10: Email do Responsável
    Label(form_inner, text="Email do Responsável", font=('Segoe UI', 10, 'bold'), bg=co1, fg=co0).grid(row=row, column=0, sticky=W, pady=5)
    e_email_responsavel = Entry(form_inner, width=30, font=('Segoe UI', 10), relief='solid', bd=2)
    e_email_responsavel.grid(row=row, column=1, sticky=EW, padx=10, pady=5)
    row += 1
    
    # Botoes com design moderno
    button_frame = Frame(form_inner, bg=co1)
    button_frame.grid(row=row, column=0, columnspan=4, pady=20)
    
    # Tabela dados Empresas
    table_frame = Frame(frame_data_display, bg=co1, relief="solid", bd=1)
    table_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)
    
    table_title = Frame(table_frame, bg=co8, height=40)
    table_title.pack(fill=X)
    table_title.pack_propagate(False)
    
    Label(table_title, text="Empresas Cadastradas", 
          font=('Segoe UI', 14, 'bold'), bg=co8, fg=co1).pack(pady=10)

    def mostrar_dados_empresas():
        # Limpar tabela existente
        for widget in table_frame.winfo_children():
            if isinstance(widget, ttk.Treeview):
                widget.destroy()
        
        # Cabeçalhos da tabela com todos os campos importantes
        list_header = ['CNPJ', 'Razão Social', 'Nome Fantasia', 'Município', 'Telefone', 'Atividade Principal', 'Situação', 'Responsável']
        df_list = ver_dados_empresas()

        global tree_dados_empresas
        
        tree_frame = Frame(table_frame, bg=co1)
        tree_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        tree_dados_empresas = ttk.Treeview(tree_frame, selectmode="extended", columns=list_header, show="headings", height=10)
        
        # Scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree_dados_empresas.yview)
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree_dados_empresas.xview)
        tree_dados_empresas.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        tree_dados_empresas.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')

        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        # Configurar colunas com larguras otimizadas
        widths = [120, 200, 150, 120, 120, 180, 100, 150]
        for i, col in enumerate(list_header):
            tree_dados_empresas.heading(col, text=col, anchor=W)
            tree_dados_empresas.column(col, width=widths[i], anchor=W)

        # Inserir dados com cores alternadas (mostrar apenas campos principais)
        for i, item in enumerate(df_list):
            # Exibir apenas os campos principais na tabela
            item_display = [
                item[0],  # CNPJ
                item[1],  # Razão Social
                item[2] if item[2] else "N/A",  # Nome Fantasia
                item[9] if item[9] else "N/A",  # Município
                item[10] if item[10] else "N/A",  # Telefone
                item[11] if item[11] else "N/A",  # Atividade Principal
                item[13] if item[13] else "N/A",  # Situação
                item[14] if item[14] else "N/A"   # Responsável
            ]
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            tree_dados_empresas.insert('', 'end', values=item_display, tags=(tag,))
        
        # Configurar tags para cores alternadas
        tree_dados_empresas.tag_configure('evenrow', background=co5)
        tree_dados_empresas.tag_configure('oddrow', background=co1)
        
        # Adicionar evento de duplo clique para carregar dados no formulário
        def on_item_double_click(event):
            try:
                selected_item = tree_dados_empresas.selection()[0]
                cnpj_selecionado = tree_dados_empresas.item(selected_item, 'values')[0]
                
                # Buscar dados completos da empresa
                resultado = buscar_empresa_por_cnpj(cnpj_selecionado)
                if resultado:
                    # Carregar dados nos campos do formulário
                    e_cnpj.delete(0, END)
                    e_cnpj.insert(0, resultado[0])
                    e_razao_social.delete(0, END)
                    e_razao_social.insert(0, resultado[1] if resultado[1] else "")
                    e_nome_fantasia.delete(0, END)
                    e_nome_fantasia.insert(0, resultado[2] if resultado[2] else "")
                    e_endereco.delete(0, END)
                    e_endereco.insert(0, resultado[3] if resultado[3] else "")
                    e_complemento.delete(0, END)
                    e_complemento.insert(0, resultado[4] if resultado[4] else "")
                    e_cep.delete(0, END)
                    e_cep.insert(0, resultado[5] if resultado[5] else "")
                    e_email.delete(0, END)
                    e_email.insert(0, resultado[6] if resultado[6] else "")
                    e_bairro.delete(0, END)
                    e_bairro.insert(0, resultado[7] if resultado[7] else "")
                    combo_uf.set(resultado[8] if resultado[8] else "")
                    e_municipio.delete(0, END)
                    e_municipio.insert(0, resultado[9] if resultado[9] else "")
                    e_telefone.delete(0, END)
                    e_telefone.insert(0, resultado[10] if resultado[10] else "")
                    e_atividade_principal.delete(0, END)
                    e_atividade_principal.insert(0, resultado[11] if resultado[11] else "")
                    e_data_abertura.delete(0, END)
                    e_data_abertura.insert(0, resultado[12] if resultado[12] else "")
                    combo_situacao.set(resultado[13] if resultado[13] else "")
                    e_responsavel.delete(0, END)
                    e_responsavel.insert(0, resultado[14] if resultado[14] else "")
                    e_telefone_responsavel.delete(0, END)
                    e_telefone_responsavel.insert(0, resultado[15] if resultado[15] else "")
                    e_email_responsavel.delete(0, END)
                    e_email_responsavel.insert(0, resultado[16] if resultado[16] else "")
                    
                    # Buscar contador associado à empresa
                    contadores_associados = buscar_contadores_por_empresa(resultado[0])
                    if contadores_associados:
                        contador_info = f"{contadores_associados[0][0]} - {contadores_associados[0][1]}"
                        combo_contador.set(contador_info)
                    else:
                        combo_contador.set("")
                
            except IndexError:
                pass
        
        tree_dados_empresas.bind('<Double-1>', on_item_double_click)

    # Funcoes CRUD
    def novo_cadastro_empresa():
        cnpj = e_cnpj.get()
        razao_social = e_razao_social.get()
        nome_fantasia = e_nome_fantasia.get()
        endereco = e_endereco.get()
        complemento = e_complemento.get()
        cep = e_cep.get()
        email = e_email.get()
        bairro = e_bairro.get()
        uf = combo_uf.get()
        municipio = e_municipio.get()
        telefone = e_telefone.get()
        atividade_principal = e_atividade_principal.get()
        data_abertura = e_data_abertura.get()
        situacao = combo_situacao.get()
        responsavel = e_responsavel.get()
        telefone_responsavel = e_telefone_responsavel.get()
        email_responsavel = e_email_responsavel.get()
        
        lista = [cnpj, razao_social, nome_fantasia, endereco, complemento, cep, email, bairro, uf, municipio, telefone, atividade_principal, data_abertura, situacao, responsavel, telefone_responsavel, email_responsavel]

        # Verificar campos obrigatórios
        campos_obrigatorios = [cnpj, razao_social]
        if any(campo == "" for campo in campos_obrigatorios):
            messagebox.showerror('Erro', 'Preencha todos os campos obrigatórios (*)')
            return
            
        try:
            criar_empresa(lista)
            
            # Associar empresa ao contador, se selecionado
            contador_selecionado = combo_contador.get()
            if contador_selecionado:
                cnpj_contador = contador_selecionado.split(" - ")[0]  # Extrair CNPJ do contador
                associar_contador_empresa(cnpj_contador, cnpj, 'representacao')
            
            messagebox.showinfo('Sucesso', 'Os dados foram inseridos com sucesso')
            
            # Limpar campos
            for entry in [e_cnpj, e_razao_social, e_nome_fantasia, e_endereco, e_complemento, e_cep, e_email, e_bairro, e_municipio, e_telefone, e_atividade_principal, e_data_abertura, e_responsavel, e_telefone_responsavel, e_email_responsavel]:
                entry.delete(0, END)
            combo_uf.set("")
            combo_situacao.set("")
            combo_contador.set("")
            
            mostrar_dados_empresas()
        except sqlite3.IntegrityError:
            messagebox.showerror('Erro', 'CNPJ ja cadastrado!')

    def atualizar_empresa_func():
        try:
            selected_item = tree_dados_empresas.selection()[0]
            cnpj_selecionado = tree_dados_empresas.item(selected_item, 'values')[0]
            
            # Coletar todos os dados
            dados = {
                'razao_social': e_razao_social.get(),
                'nome_fantasia': e_nome_fantasia.get(),
                'endereco': e_endereco.get(),
                'complemento': e_complemento.get(),
                'cep': e_cep.get(),
                'email': e_email.get(),
                'bairro': e_bairro.get(),
                'uf': combo_uf.get(),
                'municipio': e_municipio.get(),
                'telefone': e_telefone.get(),
                'atividade_principal': e_atividade_principal.get(),
                'data_abertura': e_data_abertura.get(),
                'situacao': combo_situacao.get(),
                'responsavel': e_responsavel.get(),
                'telefone_responsavel': e_telefone_responsavel.get(),
                'email_responsavel': e_email_responsavel.get()
            }
            
            # Verificar campos obrigatórios
            campos_obrigatorios = ['razao_social']
            if any(dados[campo] == "" for campo in campos_obrigatorios):
                messagebox.showerror('Erro', 'Preencha todos os campos obrigatórios (*)')
                return
                
            atualizar_empresa(cnpj_selecionado, **dados)
            
            # Atualizar associação com contador
            contador_selecionado = combo_contador.get()
            
            # Primeiro, desassociar todos os contadores existentes
            contadores_existentes = buscar_contadores_por_empresa(cnpj_selecionado)
            for contador in contadores_existentes:
                desassociar_contador_empresa(contador[0], cnpj_selecionado)
            
            # Associar ao novo contador, se selecionado
            if contador_selecionado:
                cnpj_contador = contador_selecionado.split(" - ")[0]  # Extrair CNPJ do contador
                associar_contador_empresa(cnpj_contador, cnpj_selecionado, 'representacao')
            
            messagebox.showinfo('Sucesso', 'Dados atualizados com sucesso')
            mostrar_dados_empresas()
            
        except IndexError:
            messagebox.showerror('Erro', 'Selecione um item na tabela')

    def deletar_empresa_func():
        try:
            selected_item = tree_dados_empresas.selection()[0]
            cnpj_selecionado = tree_dados_empresas.item(selected_item, 'values')[0]
            
            resposta = messagebox.askyesno('Confirmacao', f'Deseja realmente excluir o registro do CNPJ {cnpj_selecionado}?')
            if resposta:
                excluir_empresa(cnpj_selecionado)
                messagebox.showinfo('Sucesso', 'Registro excluido com sucesso')
                mostrar_dados_empresas()
                
        except IndexError:
            messagebox.showerror('Erro', 'Selecione um item na tabela')

    # Criar botoes
    btn_salvar = criar_botao_moderno(button_frame, "SALVAR", novo_cadastro_empresa, co3)
    btn_salvar.pack(side=LEFT, padx=5)
    
    btn_atualizar = criar_botao_moderno(button_frame, "ATUALIZAR", atualizar_empresa_func, co2)
    btn_atualizar.pack(side=LEFT, padx=5)
    
    btn_deletar = criar_botao_moderno(button_frame, "DELETAR", deletar_empresa_func, co4)
    btn_deletar.pack(side=LEFT, padx=5)

    mostrar_dados_empresas()

#---- CONTROLE
def control(i):
    if i == 'repis':
        repis()
    elif i == 'contador':
        contador()
    elif i == 'empresas':
        empresas()
    elif i == 'preenchimento':
        preenchimento_pdf()
    elif i == 'salvar':
        exportar()

# Inicializar com REPIS
repis()

janela.mainloop()


