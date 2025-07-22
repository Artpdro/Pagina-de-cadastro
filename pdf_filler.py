"""
Módulo para preenchimento automático do PDF REPIS com coordenadas ajustadas
"""

import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PyPDF2 import PdfReader, PdfWriter
from tkinter import messagebox
import os

def preencher_pdf_repis_alinhado(dados_repis, dados_contador=None, arquivo_saida=None):
    """
    Preenche o PDF REPIS com os dados fornecidos usando coordenadas alinhadas conforme a imagem
    """
    try:
        # Verificar se o arquivo PDF original existe
        pdf_original = "REPIS-2025-2026.pdf"
        if not os.path.exists(pdf_original):
            raise FileNotFoundError(f"Arquivo {pdf_original} não encontrado")
        
        # Criar um novo PDF com os dados preenchidos
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)
        
        # Configurar fonte menor para melhor alinhamento
        can.setFont("Helvetica", 9)
        
        # Coordenadas ajustadas baseadas na análise da imagem fornecida
        # A imagem mostra um formulário com campos específicos que precisam ser alinhados
        
        # CNPJ (campo no topo do formulário)
        if dados_repis.get('cnpj'):
            can.drawString(245, 735, dados_repis.get('cnpj', ''))
        
        # Razão Social
        if dados_repis.get('razao_social'):
            can.drawString(100, 710, dados_repis.get('razao_social', ''))
        
        # Nome Fantasia
        if dados_repis.get('nome_fantasia'):
            can.drawString(100, 685, dados_repis.get('nome_fantasia', ''))
        
        # Endereço
        if dados_repis.get('endereco'):
            can.drawString(100, 660, dados_repis.get('endereco', ''))
        
        # Número (parte do endereço)
        # can.drawString(350, 660, "S/N")  # Valor padrão se não tiver número
        
        # Complemento
        if dados_repis.get('complemento'):
            can.drawString(450, 660, dados_repis.get('complemento', ''))
        
        # CEP
        if dados_repis.get('cep'):
            can.drawString(100, 635, dados_repis.get('cep', ''))
        
        # Email
        if dados_repis.get('email'):
            can.drawString(250, 635, dados_repis.get('email', ''))
        
        # Bairro
        if dados_repis.get('bairro'):
            can.drawString(100, 610, dados_repis.get('bairro', ''))
        
        # UF
        if dados_repis.get('uf'):
            can.drawString(250, 610, dados_repis.get('uf', ''))
        
        # Município
        if dados_repis.get('municipio'):
            can.drawString(350, 610, dados_repis.get('municipio', ''))
        
        # Data de abertura
        if dados_repis.get('data_abertura'):
            can.drawString(100, 585, dados_repis.get('data_abertura', ''))
        
        # Número de empregados (campo específico do formulário)
        can.drawString(350, 585, "0")  # Valor padrão
        
        # Nome do solicitante
        if dados_repis.get('nome_solicitante'):
            can.drawString(100, 545, dados_repis.get('nome_solicitante', ''))
        
        # Marcar checkbox SÓCIO ou CONTADOR
        if dados_repis.get('solicitante_tipo'):
            if dados_repis.get('solicitante_tipo').upper() == 'SÓCIO':
                can.drawString(295, 520, 'X')  # Checkbox SÓCIO
            elif dados_repis.get('solicitante_tipo').upper() == 'CONTADOR':
                can.drawString(365, 520, 'X')  # Checkbox CONTADOR
        
        # Telefone do solicitante
        if dados_repis.get('telefone'):
            can.drawString(100, 495, dados_repis.get('telefone', ''))
        
        # Email do solicitante
        if dados_repis.get('email_solicitante'):
            can.drawString(200, 495, dados_repis.get('email_solicitante', ''))
        
        # CPF
        if dados_repis.get('cpf'):
            can.drawString(350, 495, dados_repis.get('cpf', ''))
        
        # RG
        if dados_repis.get('rg'):
            can.drawString(450, 495, dados_repis.get('rg', ''))
        
        # Dados do contador
        if dados_contador:
            # Nome do contador
            if dados_contador.get('nome'):
                can.drawString(100, 470, dados_contador.get('nome', ''))
            
            # Telefone do contador
            if dados_contador.get('contato'):
                can.drawString(200, 470, dados_contador.get('contato', ''))
            
            # Email do contador
            if dados_contador.get('email_contador'):
                can.drawString(350, 470, dados_contador.get('email_contador', ''))
        elif dados_repis.get('contador'):
            # Usar dados do contador do REPIS
            can.drawString(100, 470, dados_repis.get('contador', ''))
            if dados_repis.get('telefone_contador'):
                can.drawString(200, 470, dados_repis.get('telefone_contador', ''))
            if dados_repis.get('email_contador'):
                can.drawString(350, 470, dados_repis.get('email_contador', ''))
        
        # Protocolo - Data atual
        from datetime import datetime
        data_atual = datetime.now().strftime("%d/%m/%Y")
        can.drawString(350, 150, data_atual)
        
        # Data de assinatura
        can.drawString(100, 100, data_atual)
        
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
            arquivo_saida = f"REPIS_preenchido_alinhado_{cnpj_limpo}.pdf"
        
        # Salvar o PDF preenchido
        with open(arquivo_saida, "wb") as outputStream:
            output.write(outputStream)
        
        return arquivo_saida
        
    except Exception as e:
        raise Exception(f'Erro ao preencher PDF: {str(e)}')

def criar_pdf_completo_repis(dados_repis, dados_contador=None):
    """
    Cria um PDF completo com layout similar ao formulário original
    """
    try:
        cnpj_limpo = dados_repis.get('cnpj', 'sem_cnpj').replace('/', '_').replace('.', '_').replace('-', '_')
        arquivo_saida = f"REPIS_formulario_completo_{cnpj_limpo}.pdf"
        
        can = canvas.Canvas(arquivo_saida, pagesize=letter)
        width, height = letter
        
        # Cabeçalho
        can.setFont("Helvetica-Bold", 14)
        can.drawString(50, height - 50, "SOLICITAÇÃO DE ADESÃO AO REPIS: 2025/2026")
        
        # Linha horizontal
        can.line(50, height - 70, width - 50, height - 70)
        
        # Seção de dados da empresa
        y_pos = height - 100
        can.setFont("Helvetica-Bold", 11)
        can.drawString(50, y_pos, "DADOS DA EMPRESA")
        
        y_pos -= 25
        can.setFont("Helvetica", 10)
        
        # CNPJ
        can.drawString(50, y_pos, "CNPJ:")
        can.drawString(100, y_pos, dados_repis.get('cnpj', ''))
        y_pos -= 20
        
        # Razão Social
        can.drawString(50, y_pos, "Razão Social:")
        can.drawString(130, y_pos, dados_repis.get('razao_social', ''))
        y_pos -= 20
        
        # Nome Fantasia
        can.drawString(50, y_pos, "Nome Fantasia:")
        can.drawString(140, y_pos, dados_repis.get('nome_fantasia', ''))
        y_pos -= 20
        
        # Endereço
        can.drawString(50, y_pos, "Endereço:")
        can.drawString(110, y_pos, dados_repis.get('endereco', ''))
        y_pos -= 20
        
        # Complemento, CEP
        can.drawString(50, y_pos, "Complemento:")
        can.drawString(130, y_pos, dados_repis.get('complemento', ''))
        can.drawString(300, y_pos, "CEP:")
        can.drawString(330, y_pos, dados_repis.get('cep', ''))
        y_pos -= 20
        
        # Bairro, UF, Município
        can.drawString(50, y_pos, "Bairro:")
        can.drawString(90, y_pos, dados_repis.get('bairro', ''))
        can.drawString(250, y_pos, "UF:")
        can.drawString(270, y_pos, dados_repis.get('uf', ''))
        can.drawString(320, y_pos, "Município:")
        can.drawString(380, y_pos, dados_repis.get('municipio', ''))
        y_pos -= 20
        
        # Email, Data de abertura
        can.drawString(50, y_pos, "E-mail:")
        can.drawString(90, y_pos, dados_repis.get('email', ''))
        can.drawString(300, y_pos, "Data de Abertura:")
        can.drawString(400, y_pos, dados_repis.get('data_abertura', ''))
        y_pos -= 30
        
        # Seção do solicitante
        can.setFont("Helvetica-Bold", 11)
        can.drawString(50, y_pos, "DADOS DO SOLICITANTE")
        y_pos -= 25
        
        can.setFont("Helvetica", 10)
        
        # Nome do solicitante
        can.drawString(50, y_pos, "Nome do Solicitante:")
        can.drawString(170, y_pos, dados_repis.get('nome_solicitante', ''))
        y_pos -= 20
        
        # Tipo de solicitante
        can.drawString(50, y_pos, "Solicitante é:")
        tipo_solicitante = dados_repis.get('solicitante_tipo', '')
        if tipo_solicitante.upper() == 'SÓCIO':
            can.drawString(130, y_pos, "☑ SÓCIO    ☐ CONTADOR")
        elif tipo_solicitante.upper() == 'CONTADOR':
            can.drawString(130, y_pos, "☐ SÓCIO    ☑ CONTADOR")
        else:
            can.drawString(130, y_pos, "☐ SÓCIO    ☐ CONTADOR")
        y_pos -= 20
        
        # Telefone, Email
        can.drawString(50, y_pos, "Telefone:")
        can.drawString(100, y_pos, dados_repis.get('telefone', ''))
        can.drawString(250, y_pos, "E-mail:")
        can.drawString(290, y_pos, dados_repis.get('email_solicitante', ''))
        y_pos -= 20
        
        # CPF, RG
        can.drawString(50, y_pos, "CPF:")
        can.drawString(80, y_pos, dados_repis.get('cpf', ''))
        can.drawString(250, y_pos, "RG:")
        can.drawString(270, y_pos, dados_repis.get('rg', ''))
        y_pos -= 30
        
        # Seção do contador
        can.setFont("Helvetica-Bold", 11)
        can.drawString(50, y_pos, "DADOS DO CONTADOR")
        y_pos -= 25
        
        can.setFont("Helvetica", 10)
        
        if dados_contador:
            # Nome do contador
            can.drawString(50, y_pos, "Contador:")
            can.drawString(110, y_pos, dados_contador.get('nome', ''))
            y_pos -= 20
            
            # Telefone do contador
            can.drawString(50, y_pos, "Telefone:")
            can.drawString(100, y_pos, dados_contador.get('contato', ''))
            
            # Email do contador
            can.drawString(250, y_pos, "E-mail:")
            can.drawString(290, y_pos, dados_contador.get('email_contador', ''))
        else:
            # Usar dados do contador do REPIS
            can.drawString(50, y_pos, "Contador:")
            can.drawString(110, y_pos, dados_repis.get('contador', ''))
            y_pos -= 20
            
            can.drawString(50, y_pos, "Telefone:")
            can.drawString(100, y_pos, dados_repis.get('telefone_contador', ''))
            
            can.drawString(250, y_pos, "E-mail:")
            can.drawString(290, y_pos, dados_repis.get('email_contador', ''))
        
        y_pos -= 40
        
        # Protocolo
        from datetime import datetime
        data_atual = datetime.now().strftime("%d/%m/%Y")
        can.drawString(50, y_pos, f"Protocolo: ________________    Data: {data_atual}")
        y_pos -= 30
        
        # Assinatura
        can.drawString(50, y_pos, f"Data: {data_atual}")
        can.drawString(300, y_pos, "Assinatura: _________________________")
        
        can.save()
        return arquivo_saida
        
    except Exception as e:
        raise Exception(f'Erro ao criar PDF completo: {str(e)}')

def processar_preenchimento_pdf_novo(dados_repis, dados_contador=None):
    """
    Função principal para processar o preenchimento do PDF com coordenadas alinhadas
    """
    try:
        # Tentar preencher o formulário original com coordenadas alinhadas
        arquivo_gerado = preencher_pdf_repis_alinhado(dados_repis, dados_contador)
        messagebox.showinfo('Sucesso', f'PDF preenchido com alinhamento gerado: {arquivo_gerado}')
        return arquivo_gerado
    except Exception as e:
        try:
            # Se falhar, criar um PDF completo com layout similar
            arquivo_gerado = criar_pdf_completo_repis(dados_repis, dados_contador)
            messagebox.showinfo('Sucesso', f'PDF com formulário completo gerado: {arquivo_gerado}\n\nNota: Não foi possível preencher o formulário original, mas foi criado um PDF com layout similar.')
            return arquivo_gerado
        except Exception as e2:
            messagebox.showerror('Erro', f'Erro ao gerar PDF: {str(e2)}')
            return None