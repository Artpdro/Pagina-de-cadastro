import sqlite3

con = sqlite3.connect('cadastro_contadores.db')

def deletar_contador(id):
    with con:
        cur = con.cursor()
        query = "DELETE FROM contadores WHERE id=?"
        cur.execute(query, (id))
        print("Contador deletado com sucesso!")

deletar_contador([2])


