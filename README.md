&#x20; \[]

# 🚀 Página de Cadastro

Bem-vindo à **Página de Cadastro**! Esta aplicação desktop em Python permite gerenciar contadores, empresas e gerar relatórios em PDF.

## ✨ Funcionalidades

* ✅ Cadastro, edição e exclusão de contadores
* ✅ Cadastro, edição e exclusão de empresas
* 🔗 Vinculação entre contadores e empresas
* 📄 Geração de PDF preenchidos
* 🖥️ Interface com abas usando `tkinter`

## 🛠️ Tecnologias

* 🐍 Python 3.12
* 🎨 `tkinter` (`ttk`, `scrolledtext`, `messagebox`)
* 📦 SQLite (`*.db`)
* 🖼️ PIL (Pillow)
* 📑 ReportLab

## 📂 Estrutura

```
Pagina-de-cadastro/
├─ main.py             # Inicializa GUI
├─ view.py             # Classes e funções da interface
├─ pdf_mapping.py      # Lógica de geração de PDF
├─ logo.png            # Logo da aplicação
├─ *.db                # Bancos SQLite
└─ build_exe.bat       # Script de build (Windows)
```

## ⚙️ Requisitos

* Python >= 3.8
* Dependências:

  ```bash
  pip install -r requirements.txt
  ```

## ▶️ Uso

```bash
python main.py
```

## 📦 Build do Executável

Windows:

```bat
build_exe.bat
```

> Certifique-se de ter o PyInstaller:
>
> ```bash
> pip install pyinstaller
> ```

## 🎨 Customizações

* 🎯 **Banco de Dados**: Edite/adicione `.db` e atualize `main.spec` ou script de build.
* 📑 **PDF**: Ajuste `pdf_mapping.py`.
* 🖌️ **GUI**: Modifique estilos em `view.py`.

## 📝 Licença

Este projeto é licenciado sob MIT. Veja `LICENSE`.

---

*Desenvolvido por Arthur Pedro 🌟*
