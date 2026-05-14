import sqlite3

conexao = sqlite3.connect("votacao.db")
cursor = conexao.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS votos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    candidato TEXT NOT NULL
)
""")

def registrar_voto(candidato):
    cursor.execute(
        "INSERT INTO votos (candidato) VALUES (?)",
        (candidato,)
    )

    conexao.commit()

registrar_voto("Candidato 1")
registrar_voto("Candidato 2")
registrar_voto("Candidato 1")

print("Votos registrados com sucesso!")

conexao.close()