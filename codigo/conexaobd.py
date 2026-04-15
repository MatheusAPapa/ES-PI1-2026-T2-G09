import mysql.connector
conexao = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'MAPB@12032008', #colocar a senha do seu mysql
    database = 'PI'
)
cursor = conexao.cursor()