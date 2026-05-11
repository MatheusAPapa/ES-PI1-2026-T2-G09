import sqlite3

conexao = sqlite3.connect("votacao.db")
cursor = conexao.cursor()

cursor.execute("""
SELECT candidato, COUNT(*) 
FROM votos
GROUP BY candidato
""")

resultados = cursor.fetchall()

print("Resultado da votação:")

for candidato, votos in resultados:
    print(candidato, "-", votos, "votos")

conexao.close()
