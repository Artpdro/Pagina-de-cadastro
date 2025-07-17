import sqlite3

# Conecta ao banco (ou cria, se não existir)
conn = sqlite3.connect('contadores.db')
cursor = conn.cursor()

# Garante que a tabela exista
cursor.execute("""
CREATE TABLE IF NOT EXISTS contadores (
    cnpj          TEXT PRIMARY KEY,
    razao_social  TEXT NOT NULL,
    nome_fantasia TEXT NOT NULL,
    municipio     TEXT NOT NULL,
    contador      TEXT NOT NULL,
    tel_contador  TEXT NOT NULL
)
""")
conn.commit()

def criar_contador(dados):
    """
    Insere um novo registro de contador.
    Aceita uma lista com os dados: [cnpj, razao_social, nome_fantasia, municipio, contador, tel_contador]
    """
    cnpj, razao_social, nome_fantasia, municipio, contador, tel_contador = dados
    cursor.execute("""
        INSERT INTO contadores
          (cnpj, razao_social, nome_fantasia, municipio, contador, tel_contador)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (cnpj, razao_social, nome_fantasia, municipio, contador, tel_contador))
    conn.commit()

def excluir_contador(cnpj):
    """
    Exclui o registro de contador com o CNPJ informado.
    """
    cursor.execute(
        "DELETE FROM contadores WHERE cnpj = ?",
        (cnpj,)
    )
    conn.commit()

def atualizar_contador(cnpj, *, razao_social=None, nome_fantasia=None,
                      municipio=None, contador=None, tel_contador=None):
    """
    Atualiza apenas os campos não-None para o contador identificado pelo CNPJ.
    Exemplo:
      atualizar_contador("00.000.000/0001-00", razao_social="Nova Razão")
    """
    campos = []
    valores = []

    if razao_social is not None:
        campos.append("razao_social = ?")
        valores.append(razao_social)
    if nome_fantasia is not None:
        campos.append("nome_fantasia = ?")
        valores.append(nome_fantasia)
    if municipio is not None:
        campos.append("municipio = ?")
        valores.append(municipio)
    if contador is not None:
        campos.append("contador = ?")
        valores.append(contador)
    if tel_contador is not None:
        campos.append("tel_contador = ?")
        valores.append(tel_contador)

    if not campos:
        # nada a atualizar
        return

    valores.append(cnpj)  # condição WHERE
    sql = f"UPDATE contadores SET {', '.join(campos)} WHERE cnpj = ?"
    cursor.execute(sql, valores)
    conn.commit()


def buscar_todos_contadores():
    """
    Retorna todos os registros de contadores do banco de dados.
    """
    cursor.execute("SELECT * FROM contadores")
    return cursor.fetchall()

def ver_dados():
    lista = []
    with conn:
        cur =conn.cursor()
        cur.execute('SELECT * FROM contadores')
        linha = cur.fetchall()

        for i in linha:
            lista.append(i)
    return lista

print()
