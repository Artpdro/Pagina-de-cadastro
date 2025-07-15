import sqlite3 

try:
    con = sqlite3.connect('cadastro_contadores.db')
    print("Conexão com o banco de dados feita com sucesso!")
except sqlite3.Error as e:
    print("Erro ao conectar ao banco de dados!", e)

# tabela de contadores
try:
    with con:
        cur = con.cursor()
        cur.execute(""" CREATE TABLE IF NOT EXISTS contadores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            empresa TEXT
        )""")


        print("Tabela contadores criada com sucesso!")


except sqlite3.Error as e:
    print("Erro ao criar tabela de contadores", e)

try:
    con = sqlite3.connect('cadastro_contadores.db')
    print("Conexão com o banco de dados feita com sucesso!")
except sqlite3.Error as e:
    print("Erro ao conectar ao banco de dados!", e)

# adicionar contador
def adicionar_contador(i):
    with con:
        cur = con.cursor()
        query = "INSERT INTO contadores (id, nome, empresa, cidade) VALUES (?,?,?,?)"
        cur.execute(query,)

# adicionar_contador(['abreu', 'thiago', 'bacanas'])

# ver tudo

def ver_contadores(): 
    lista = []
    with con:
        cur = con.cursor()
        cur.execute('SELECT * FROM contadores')
        linha = cur.fetchall()

        for i in linha:
            lista.append(i)
    return lista

# print(ver_contadores())

con = sqlite3.connect('cadastro_contadores.db')

# atualizar contadores

def atualizar_contador(id, nome, empresa, cidade):
    with con:
        cur = con.cursor()
        query = "UPDATE contadores SET nome = ?, empresa = ? cidade = ? WHERE id = ?"
        cur.execute(query, (nome, empresa, cidade, id))
        print("Contador atualizado com sucesso!")

l = ['Gisele', 'sindnorte']

atualizar_contador(1, 'Gisele', 'Sindnorte')

# deletar contadores

def deletar_contador(id):
    with con:
        cur = con.cursor()
        query = "DELETE FROM contadores WHERE id=?"
        cur.execute(query, (id))
        print("Contador deletado com sucesso!")

deletar_contador([2])

# ------------------------------

