from datetime import datetime
import random
import conexaobd

def registrar_log(mensagem):
    #regista a hora que ocorrerá o log
    data_hora = datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
    
    #tenta registra o log no arquivo txt, caso não de mostrará uma mensagem de erro
    try:
        with open("codigo/logs_ocorrencia.txt", "a", encoding="utf-8") as arq:
            arq.write(f"{data_hora} -> {mensagem}\n")
    except:
        print("não foi possível salvar o log")

def exibir_logs ():
    #Faz a leitura dos logs no arquivo txt e depois printa, caso não exista o arquivo será mostrado uma mensagem de erro
    try:
        with open("codigo/logs_ocorrencia.txt", "r", encoding="utf-8") as arq:
            conteudo = arq.read()
            print(conteudo)
    except FileNotFoundError:
        print('Arquivo não encontrado')

def gerar_protocolo_votacao (candidato):
    alfabeto = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M','N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    letras_aleatorias = ''.join(random.choices(alfabeto, k=2))
    numeros_aleatorios = random.randint(10000, 99999)

    protocolo = 'V' + letras_aleatorias + '26' + str(candidato) + str(numeros_aleatorios)
    return protocolo

def abrir_sistema_votacao (cpf_abrindo, titulo_abrindo, chave_acesso_abrindo ):
    #pega os dados do eleitor no banco de dados
    sql = ('SELECT cpf, numero_titulo, mesario, chave_acesso FROM eleitores WHERE cpf=%s')
    values = (cpf)
    conexaobd.cursor.execute(sql, values)
    cpf, numero_titulo, mesario, chave_acesso = conexaobd.cursor.fetchone()

    #compara os dados do banco de dados com os dados informados pelos eleitores
    if mesario != True:
        print('Você não tem permissão para abrir o sistema de votação!')
    elif cpf_abrindo != cpf[0:4]:
        print('Valídação dos dados falhou, pois o cpf está errado, não será possível fazer a abertura da votação! ')
    elif titulo_abrindo != numero_titulo:
        print('Valídação dos dados falhou, pois o título de eleitor está errado, não será possível fazer a abertura da votação! ')
    elif chave_acesso_abrindo != chave_acesso:
        print('Valídação dos dados falhou, pois a chave de acesso está errada, não será possível fazer a abertura da votação! ')
        
    #fazendo a zerázima
    conexaobd.cursor.execute('DELETE * FROM votos')
    conexaobd.conexao.commit()
    conexaobd.cursor.execute('''
    SELECT c.nome, c.numero, COUNT(v.voto) AS total_votos
    FROM candidatos AS c
    LEFT JOIN votos AS v ON c.numero = v.voto
    GROUP BY c.numero, c.nome
    ''')

    print("\n================= ZERÁZIMA ===================")
    for (nome, numero, total_votos) in conexaobd.cursor.fetchall():
        print(f'Número: {numero} - Nome: {nome} - Total de votos: {total_votos}')
    print("================================================\n")
