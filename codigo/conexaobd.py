import mysql.connector
conexao = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'Kellgu123@', #colocar a senha do seu mysql
    database = 'PI'
)
cursor = conexao.cursor()