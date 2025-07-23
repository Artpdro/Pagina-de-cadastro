'''
Este arquivo contém o mapeamento corrigido dos campos do PDF REPIS-2025-2026.pdf para preenchimento.
As coordenadas (x, y) representam o canto inferior esquerdo do campo de texto.
As coordenadas foram ajustadas baseadas na análise dos PDFs de exemplo fornecidos.

Sistema de coordenadas do PDF:
- Origem (0,0) no canto inferior esquerdo
- X aumenta para a direita
- Y aumenta para cima
- Tamanho da página: aproximadamente 612x792 pontos (Letter)
'''

# Coordenadas corrigidas baseadas na análise visual dos PDFs
pdf_fields = {
    # Primeira linha - Razão Social e CNPJ
    'razao_social': {'x': 70, 'y': 670, 'width': 400, 'height': 15},
    'cnpj': {'x': 350, 'y': 670, 'width': 150, 'height': 15},
    
    # Segunda linha - Nome Fantasia
    'nome_fantasia': {'x': 70, 'y': 635, 'width': 680, 'height': 15},
    
    # Terceira linha - Endereço, Número e Complemento
    'endereco': {'x': 70, 'y': 597, 'width': 400, 'height': 15},
    'numero': {'x': 350, 'y': 597, 'width': 80, 'height': 15},
    'complemento': {'x': 460, 'y': 597, 'width': 150, 'height': 15},
    
    # Quarta linha - CEP e Email
    'cep': {'x': 70, 'y': 563, 'width': 120, 'height': 15},
    'email': {'x': 350, 'y': 563, 'width': 200, 'height': 15},
    
    # Quinta linha - Bairro, UF e Município
    'bairro': {'x': 70, 'y': 529, 'width': 350, 'height': 15},
    'uf': {'x': 350, 'y': 529, 'width': 50, 'height': 15},
    'municipio': {'x': 460, 'y': 529, 'width': 150, 'height': 15},
    
    # Sexta linha - Data de abertura e Número de empregados
    'data_abertura': {'x': 70, 'y': 488, 'width': 120, 'height': 15},
    'num_empregados': {'x': 350, 'y': 488, 'width': 80, 'height': 15},
    
    # Seção do solicitante
    'nome_solicitante': {'x': 70, 'y': 433, 'width': 400, 'height': 15},
    
    # Linha do solicitante - Telefone, Email, CPF, RG
    'telefone_solicitante': {'x': 70, 'y': 392, 'width': 150, 'height': 15},
    'email_solicitante': {'x': 200, 'y': 392, 'width': 200, 'height': 15},
    'cpf_solicitante': {'x': 350, 'y': 392, 'width': 120, 'height': 15},
    'rg_solicitante': {'x': 460, 'y': 392, 'width': 120, 'height': 15},
    
    # Seção do contador
    'nome_contador': {'x': 70, 'y': 340, 'width': 200, 'height': 15},
    'telefone_contador': {'x': 200, 'y': 340, 'width': 150, 'height': 15},
    'email_contador': {'x': 350, 'y': 340, 'width': 200, 'height': 15},
}

# Coordenadas dos checkboxes
checkbox_fields = {
    'solicitante_socio': {'x': 370, 'y': 433, 'width': 10, 'height': 10},
    'solicitante_contador': {'x': 455, 'y': 433, 'width': 10, 'height': 10},
}

# Mapeamento de campos do sistema para campos do PDF
field_mapping = {
    'cnpj': 'cnpj',
    'razao_social': 'razao_social',
    'nome_fantasia': 'nome_fantasia',
    'endereco': 'endereco',
    'numero': 'numero',
    'complemento': 'complemento',
    'cep': 'cep',
    'email': 'email',
    'bairro': 'bairro',
    'uf': 'uf',
    'municipio': 'municipio',
    'data_abertura': 'data_abertura',
    'nome_solicitante': 'nome_solicitante',
    'telefone': 'telefone_solicitante',
    'email_solicitante': 'email_solicitante',
    'cpf': 'cpf_solicitante',
    'rg': 'rg_solicitante',
    'contador': 'nome_contador',
    'telefone_contador': 'telefone_contador',
    'email_contador': 'email_contador',
}
