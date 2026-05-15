from datetime import datetime
import random
import conexaobd
import verificacoes
import os

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

def verificar_eleitor(titulo_eleitor, cpf_eleitor):
    # a função verifica se o eleitor está no banco de dados e se ele já votou
    sql = 'SELECT cpf, numero_titulo, status_de_voto FROM eleitores WHERE cpf=%s AND numero_titulo=%s'
    values = [cpf_eleitor, titulo_eleitor]
    conexaobd.cursor.execute(sql, values)
    
    resultado = conexaobd.cursor.fetchone()
    
    # verifica se o eleitor está cadastrado
    if resultado is None:
        print('Eleitor não encontrado!\n')
        return False
    #verificando se o eleitor já votou
    ja_votou = resultado[2]
    if ja_votou == True:
        print('Não é possível votar duas vezes!\n')
        return False
    return True

def abrir_sistema_votacao (titulo_abrindo, cpf_abrindo, chave_acesso_abrindo):
    os.system('cls')
    #pega os dados do eleitor no banco de dados
    sql = ('SELECT cpf, numero_titulo, mesario, chave_acesso FROM eleitores WHERE numero_titulo=%s')
    values = [titulo_abrindo]
    conexaobd.cursor.execute(sql, values)
    cpf, numero_titulo, mesario, chave_acesso = conexaobd.cursor.fetchone()

    #compara os dados do banco de dados com os dados informados pelos eleitores
    if mesario != True:
        print('\nVocê não tem permissão para abrir o sistema de votação!')
        return
    elif cpf_abrindo != cpf[0:4]:
        print('\nValídação dos dados falhou, pois o cpf está errado, não será possível fazer a abertura da votação! ')
        return
    elif titulo_abrindo != numero_titulo:
        print('\nValídação dos dados falhou, pois o título de eleitor está errado, não será possível fazer a abertura da votação! ')
        return
    elif chave_acesso_abrindo != chave_acesso:
        print('\nValídação dos dados falhou, pois a chave de acesso está errada, não será possível fazer a abertura da votação! ')
        return
        
    #fazendo a zerázima
    conexaobd.cursor.execute('DELETE FROM votos')
    conexaobd.conexao.commit()
    conexaobd.cursor.execute('''
    SELECT c.nome, c.numero, COUNT(v.voto) AS total_votos
    FROM candidatos AS c
    LEFT JOIN votos AS v ON c.numero = v.voto
    GROUP BY c.numero, c.nome
    ''')

    print("\n================= ZERÉZIMA ===================")
    for (nome, numero, total_votos) in conexaobd.cursor.fetchall():
        print(f'\nNúmero: {numero} - Nome: {nome} - Total de votos: {total_votos}')
    print("================================================\n")
    input('Precione enter para iniciar a votação! ')

    os.system('cls')
    #computação dos votos
    print('''
    ====================================
                  Votação
    ====================================
    ''')
    encerrar = 'n'
    while encerrar == 'n':
        #verificando validade do CPF
        cpf = str(input("Digite seu CPF: "))
        while verificacoes.verificarCPF(cpf) == False:
            cpf = str(input('Informe o CPF do eleitor: '))
        #verificando validade do título
        titulo_eleitor = str(input('Digite seu título de eleitor: '))
        while verificacoes.verificarTitulo(titulo_eleitor) == False:
            print('Título de eleitor inválido!')
            titulo_eleitor = str(input('Informe o título de eleitor: '))
        #verificando se o eleitor está no sistema
        verificar_eleitor(titulo_eleitor, cpf)