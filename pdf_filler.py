"""
Módulo para preenchimento automático do PDF REPIS
"""

import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PyPDF2 import PdfReader, PdfWriter
from tkinter import messagebox
import os

def preencher_pdf_repis_melhorado(dados_repis, dados_contador=None, arquivo_saida=None):
    """
    Preenche o PDF REPIS com os dados fornecidos de forma mais precisa
    """
    try:
        # Verificar se o arquivo PDF original existe
        pdf_original = "REPIS-2025-2026.pdf"
        if not os.path.exists(pdf_original):
            raise FileNotFoundError(f"Arquivo {pdf_original} não encontrado")
        
        # Criar um novo PDF com os dados preenchidos
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)
        
        # Configurar fonte
        can.setFont("Helvetica", 10)
        
        # Posições aproximadas dos campos no PDF (ajustadas para o formulário REPIS)
        # Estas coordenadas podem precisar de ajuste fino baseado no PDF real
        
        # CNPJ (campo principal)
        if dados_repis.get('cnpj'):
            can.drawString(150, 680, dados_repis.get('cnpj', ''))
        
        # Número de empregados (campo vazio no formulário)
        # can.drawString(400, 680, "0")  # Valor padrão
        
        # Nome do solicitante
        if dados_repis.get('nome_solicitante'):
            can.drawString(150, 620, dados_repis.get('nome_solicitante', ''))
        
        # Marcar se é SÓCIO ou CONTADOR
        if dados_repis.get('solicitante_tipo'):
            if dados_repis.get('solicitante_tipo').upper() == 'SÓCIO':
                can.drawString(150, 590, 'X')  # Marcar SÓCIO
            elif dados_repis.get('solicitante_tipo').upper() == 'CONTADOR':
                can.drawString(250, 590, 'X')  # Marcar CONTADOR
        
        # CPF
        if dados_repis.get('cpf'):
            can.drawString(100, 560, dados_repis.get('cpf', ''))
        
        # RG
        if dados_repis.get('rg'):
            can.drawString(250, 560, dados_repis.get('rg', ''))
        
        # Telefone
        if dados_repis.get('telefone'):
            can.drawString(400, 560, dados_repis.get('telefone', ''))
        
        # Email do solicitante
        if dados_repis.get('email_solicitante'):
            can.drawString(100, 530, dados_repis.get('email_solicitante', ''))
        
        # Dados do contador (se aplicável)
        if dados_contador:
            # Nome do contador
            if dados_contador.get('nome'):
                can.drawString(100, 500, dados_contador.get('nome', ''))
            
            # Telefone do contador
            if dados_contador.get('contato'):
                can.drawString(250, 500, dados_contador.get('contato', ''))
            
            # Email do contador
            if dados_contador.get('email_contador'):
                can.drawString(400, 500, dados_contador.get('email_contador', ''))
        elif dados_repis.get('contador'):
            # Usar dados do contador do REPIS
            can.drawString(100, 500, dados_repis.get('contador', ''))
            if dados_repis.get('telefone_contador'):
                can.drawString(250, 500, dados_repis.get('telefone_contador', ''))
            if dados_repis.get('email_contador'):
                can.drawString(400, 500, dados_repis.get('email_contador', ''))
        
        # Data atual (protocolo)
        from datetime import datetime
        data_atual = datetime.now().strftime("%d/%m/%Y")
        can.drawString(100, 200, data_atual)
        
        can.save()
        
        # Mover para o início do StringIO buffer
        packet.seek(0)
        new_pdf = PdfReader(packet)
        
        # Ler o PDF original
        existing_pdf = PdfReader(pdf_original)
        output = PdfWriter()
        
        # Adicionar a página preenchida
        page = existing_pdf.pages[0]
        page.merge_page(new_pdf.pages[0])
        output.add_page(page)
        
        # Definir nome do arquivo de saída
        if not arquivo_saida:
            cnpj_limpo = dados_repis.get('cnpj', 'sem_cnpj').replace('/', '_').replace('.', '_').replace('-', '_')
            arquivo_saida = f"REPIS_preenchido_{cnpj_limpo}.pdf"
        
        # Salvar o PDF preenchido
        with open(arquivo_saida, "wb") as outputStream:
            output.write(outputStream)
        
        return arquivo_saida
        
    except Exception as e:
        raise Exception(f'Erro ao preencher PDF: {str(e)}')

def criar_pdf_simples_repis(dados_repis, dados_contador=None):
    """
    Cria um PDF simples com os dados do REPIS quando o preenchimento do formulário falha
    """
    try:
        cnpj_limpo = dados_repis.get('cnpj', 'sem_cnpj').replace('/', '_').replace('.', '_').replace('-', '_')
        arquivo_saida = f"REPIS_dados_{cnpj_limpo}.pdf"
        
        can = canvas.Canvas(arquivo_saida, pagesize=letter)
        width, height = letter
        
        # Título
        can.setFont("Helvetica-Bold", 16)
        can.drawString(50, height - 50, "SOLICITAÇÃO DE ADESÃO AO REPIS: 2025/2026")
        
        # Dados da empresa
        can.setFont("Helvetica-Bold", 12)
        can.drawString(50, height - 100, "DADOS DA EMPRESA:")
        
        can.setFont("Helvetica", 10)
        y_pos = height - 120
        
        campos_empresa = [
            ("CNPJ:", dados_repis.get('cnpj', '')),
            ("Razão Social:", dados_repis.get('razao_social', '')),
            ("Nome Fantasia:", dados_repis.get('nome_fantasia', '')),
            ("Endereço:", dados_repis.get('endereco', '')),
            ("Complemento:", dados_repis.get('complemento', '')),
            ("CEP:", dados_repis.get('cep', '')),
            ("Bairro:", dados_repis.get('bairro', '')),
            ("Município:", dados_repis.get('municipio', '')),
            ("UF:", dados_repis.get('uf', '')),
            ("E-mail:", dados_repis.get('email', '')),
            ("Data de Abertura:", dados_repis.get('data_abertura', ''))
        ]
        
        for campo, valor in campos_empresa:
            can.drawString(50, y_pos, f"{campo} {valor}")
            y_pos -= 20
        
        # Dados do solicitante
        y_pos -= 20
        can.setFont("Helvetica-Bold", 12)
        can.drawString(50, y_pos, "DADOS DO SOLICITANTE:")
        y_pos -= 20
        
        can.setFont("Helvetica", 10)
        campos_solicitante = [
            ("Nome do Solicitante:", dados_repis.get('nome_solicitante', '')),
            ("Tipo de Solicitante:", dados_repis.get('solicitante_tipo', '')),
            ("CPF:", dados_repis.get('cpf', '')),
            ("RG:", dados_repis.get('rg', '')),
            ("Telefone:", dados_repis.get('telefone', '')),
            ("E-mail:", dados_repis.get('email_solicitante', ''))
        ]
        
        for campo, valor in campos_solicitante:
            can.drawString(50, y_pos, f"{campo} {valor}")
            y_pos -= 20
        
        # Dados do contador
        if dados_repis.get('contador') or dados_contador:
            y_pos -= 20
            can.setFont("Helvetica-Bold", 12)
            can.drawString(50, y_pos, "DADOS DO CONTADOR:")
            y_pos -= 20
            
            can.setFont("Helvetica", 10)
            if dados_contador:
                campos_contador = [
                    ("Nome:", dados_contador.get('nome', '')),
                    ("Telefone:", dados_contador.get('contato', '')),
                    ("E-mail:", dados_contador.get('email_contador', ''))
                ]
            else:
                campos_contador = [
                    ("Nome:", dados_repis.get('contador', '')),
                    ("Telefone:", dados_repis.get('telefone_contador', '')),
                    ("E-mail:", dados_repis.get('email_contador', ''))
                ]
            
            for campo, valor in campos_contador:
                can.drawString(50, y_pos, f"{campo} {valor}")
                y_pos -= 20
        
        # Data de geração
        from datetime import datetime
        data_atual = datetime.now().strftime("%d/%m/%Y às %H:%M")
        can.drawString(50, 50, f"Documento gerado em: {data_atual}")
        
        can.save()
        return arquivo_saida
        
    except Exception as e:
        raise Exception(f'Erro ao criar PDF simples: {str(e)}')

def processar_preenchimento_pdf(dados_repis, dados_contador=None):
    """
    Função principal para processar o preenchimento do PDF
    Tenta primeiro preencher o formulário original, se falhar, cria um PDF simples
    """
    try:
        # Tentar preencher o formulário original
        arquivo_gerado = preencher_pdf_repis_melhorado(dados_repis, dados_contador)
        messagebox.showinfo('Sucesso', f'PDF preenchido gerado: {arquivo_gerado}')
        return arquivo_gerado
    except Exception as e:
        try:
            # Se falhar, criar um PDF simples com os dados
            arquivo_gerado = criar_pdf_simples_repis(dados_repis, dados_contador)
            messagebox.showinfo('Sucesso', f'PDF com dados gerado: {arquivo_gerado}\n\nNota: Não foi possível preencher o formulário original, mas foi criado um PDF com todos os dados.')
            return arquivo_gerado
        except Exception as e2:
            messagebox.showerror('Erro', f'Erro ao gerar PDF: {str(e2)}')
            return None

