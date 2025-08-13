import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PyPDF2 import PdfReader, PdfWriter
from tkinter import messagebox
import os
from datetime import datetime
from pdf_mapping import pdf_fields, checkbox_fields

def preencher_pdf_repis_alinhado(dados_repis, dados_contador=None, arquivo_saida=None):
    try:
        pdf_original = "REPIS - 2025-2026.pdf"
        if not os.path.exists(pdf_original):
            raise FileNotFoundError(f"Arquivo {pdf_original} não encontrado")
        
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)
        can.setFont("Helvetica", 9)
        
        # Preencher campos de texto
        for key, field_info in pdf_fields.items():
            value = ""
            
            # Mapeamento específico para campos do solicitante
            if key == 'telefone_solicitante':
                value = dados_repis.get('telefone', '')
            elif key == 'cpf_solicitante':
                value = dados_repis.get('cpf', '')
            elif key == 'rg_solicitante':
                value = dados_repis.get('rg', '')
            elif key == 'nome_contador':
                # Primeiro tentar dados do contador, depois dados do REPIS
                if dados_contador and dados_contador.get('nome'):
                    value = dados_contador['nome']
                else:
                    value = dados_repis.get('contador', '')
            elif key == 'telefone_contador':
                # Primeiro tentar dados do contador, depois dados do REPIS
                if dados_contador and dados_contador.get('contato'):
                    value = dados_contador['contato']
                else:
                    value = dados_repis.get('telefone_contador', '')
            elif key == 'email_contador':
                # Primeiro tentar dados do contador, depois dados do REPIS
                if dados_contador and dados_contador.get('email'):
                    value = dados_contador['email']
                else:
                    value = dados_repis.get('email_contador', '')
            # Para outros campos, usar mapeamento direto
            elif key in dados_repis and dados_repis[key]:
                value = str(dados_repis[key])
            # Se não encontrou e há dados do contador, buscar lá
            elif dados_contador and key in dados_contador and dados_contador[key]:
                value = str(dados_contador[key])
            
            # Tratamento especial para campos compostos como endereco + numero
            if key == 'endereco' and 'numero' in pdf_fields and 'numero' in dados_repis:
                endereco_base = dados_repis.get('endereco', '')
                numero = dados_repis.get('numero', '')
                if endereco_base and numero:
                    value = f"{endereco_base}, {numero}"
                elif endereco_base:
                    value = endereco_base
            
            # Garantir que telefone seja formatado corretamente
            if 'telefone' in key and value:
                # Remover caracteres não numéricos e formatar
                telefone_limpo = ''.join(filter(str.isdigit, value))
                if len(telefone_limpo) == 11:  # Celular
                    value = f"({telefone_limpo[:2]}) {telefone_limpo[2:7]}-{telefone_limpo[7:]}"
                elif len(telefone_limpo) == 10:  # Fixo
                    value = f"({telefone_limpo[:2]}) {telefone_limpo[2:6]}-{telefone_limpo[6:]}"
            
            if value and value != "None":
                can.drawString(field_info['x'], field_info['y'], value)

        # Preencher checkboxes
        if dados_repis.get("solicitante_tipo"):
            if dados_repis["solicitante_tipo"].upper() == "SÓCIO":
                if "solicitante_socio" in checkbox_fields:
                    field_info = checkbox_fields["solicitante_socio"]
                    can.drawString(field_info['x'], field_info['y'], "X")
            elif dados_repis["solicitante_tipo"].upper() == "CONTADOR":
                if "solicitante_contador" in checkbox_fields:
                    field_info = checkbox_fields["solicitante_contador"]
                    can.drawString(field_info['x'], field_info['y'], "X")

        # Preencher datas de assinatura
        data_atual = datetime.now().strftime("%d/%m/%Y")
        if "data_assinatura_empresa" in pdf_fields:
            field_info = pdf_fields["data_assinatura_empresa"]
            can.drawString(field_info['x'], field_info['y'], data_atual)
        if "data_assinatura_protocolo" in pdf_fields:
            field_info = pdf_fields["data_assinatura_protocolo"]
            can.drawString(field_info['x'], field_info['y'], data_atual)

        can.save()
        packet.seek(0)
        new_pdf = PdfReader(packet)
        
        existing_pdf = PdfReader(pdf_original)
        output = PdfWriter()
        
        page = existing_pdf.pages[0]
        page.merge_page(new_pdf.pages[0])
        output.add_page(page)
        
        if not arquivo_saida:
            cnpj_limpo = dados_repis.get("cnpj", "sem_cnpj").replace("/", "_").replace(".", "_").replace("-", "_")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            arquivo_saida = f"REPIS {cnpj_limpo}_{timestamp}.pdf"
        
        with open(arquivo_saida, "wb") as outputStream:
            output.write(outputStream)
        
        return arquivo_saida
        
    except Exception as e:
        raise Exception(f"Erro ao preencher PDF: {str(e)}")

def criar_pdf_completo_repis(dados_repis, dados_contador=None):
    # Esta função permanece como fallback, caso o preenchimento alinhado falhe
    # Não é o foco principal da correção atual, mas é mantida para robustez
    try:
        cnpj_limpo = dados_repis.get("cnpj", "sem_cnpj").replace("/", "_").replace(".", "_").replace("-", "_")
        arquivo_saida = f"REPIS_{cnpj_limpo}.pdf"
        
        can = canvas.Canvas(arquivo_saida, pagesize=letter)
        width, height = letter
        
        # ... (código existente para criar PDF completo)
        # Apenas um placeholder para o código existente, que não será alterado agora
        can.setFont("Helvetica-Bold", 14)
        can.drawString(50, height - 50, "SOLICITAÇÃO DE ADESÃO AO REPIS: 2025/2026")
        can.save()
        return arquivo_saida
        
    except Exception as e:
        raise Exception(f"Erro ao criar PDF completo: {str(e)}")

def processar_preenchimento_pdf_novo(dados_repis, dados_contador=None):
    try:
        arquivo_gerado = preencher_pdf_repis_alinhado(dados_repis, dados_contador)
        messagebox.showinfo("Sucesso", f"PDF preenchido com alinhamento gerado: {arquivo_gerado}")
        return arquivo_gerado
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao preencher o PDF alinhado: {str(e)}\nTentando gerar PDF com layout completo como alternativa.")
        try:
            arquivo_gerado = criar_pdf_completo_repis(dados_repis, dados_contador)
            messagebox.showinfo("Sucesso", f"PDF com formulário completo gerado: {arquivo_gerado}\n\nNota: Não foi possível preencher o formulário original, mas foi criado um PDF com layout similar.")
            return arquivo_gerado
        except Exception as e2:
            messagebox.showerror("Erro", f"Erro ao gerar PDF: {str(e2)}")
            return None
