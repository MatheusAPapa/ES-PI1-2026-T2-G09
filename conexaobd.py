import mysql.connector
conexao = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'sua_senha', #colocar a senha do seu mysql
    database = 'PI'
)
cursor = conexao.cursor()