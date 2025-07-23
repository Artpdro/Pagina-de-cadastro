'''
Este arquivo contém o mapeamento dos campos do PDF REPIS-2025-2026.pdf para preenchimento.
As coordenadas (x, y) representam o canto inferior esquerdo do campo de texto.
As dimensões (width, height) representam a largura e altura do campo de texto.

As coordenadas foram estimadas visualmente e podem precisar de ajustes finos.
'''

pdf_fields = {
    'razao_social': {'x': 100, 'y': 690, 'width': 250, 'height': 15},
    'cnpj': {'x': 400, 'y': 690, 'width': 150, 'height': 15},
    'nome_fantasia': {'x': 100, 'y': 650, 'width': 250, 'height': 15},
    'endereco': {'x': 100, 'y': 610, 'width': 250, 'height': 15},
    'numero': {'x': 400, 'y': 610, 'width': 50, 'height': 15},
    'complemento': {'x': 500, 'y': 610, 'width': 100, 'height': 15},
    'cep': {'x': 100, 'y': 570, 'width': 100, 'height': 15},
    'email': {'x': 250, 'y': 570, 'width': 200, 'height': 15},
    'bairro': {'x': 100, 'y': 530, 'width': 150, 'height': 15},
    'uf': {'x': 300, 'y': 530, 'width': 50, 'height': 15},
    'municipio': {'x': 400, 'y': 530, 'width': 150, 'height': 15},
    'data_abertura': {'x': 100, 'y': 490, 'width': 100, 'height': 15},
    'num_empregados': {'x': 400, 'y': 490, 'width': 50, 'height': 15},

    'nome_solicitante': {'x': 100, 'y': 410, 'width': 250, 'height': 15},
    'telefone_solicitante': {'x': 100, 'y': 370, 'width': 150, 'height': 15},
    'email_solicitante': {'x': 300, 'y': 370, 'width': 200, 'height': 15},
    'cpf_solicitante': {'x': 500, 'y': 370, 'width': 100, 'height': 15},
    'rg_solicitante': {'x': 650, 'y': 370, 'width': 100, 'height': 15},

    'nome_contador': {'x': 100, 'y': 300, 'width': 250, 'height': 15},
    'telefone_contador': {'x': 400, 'y': 300, 'width': 150, 'height': 15},
    'email_contador': {'x': 600, 'y': 300, 'width': 200, 'height': 15},

    'data_assinatura_empresa': {'x': 550, 'y': 220, 'width': 100, 'height': 15},
    'data_assinatura_protocolo': {'x': 750, 'y': 220, 'width': 100, 'height': 15},
}

checkbox_fields = {
    'solicitante_socio': {'x': 500, 'y': 420, 'width': 10, 'height': 10},
    'solicitante_contador': {'x': 600, 'y': 420, 'width': 10, 'height': 10},
}

