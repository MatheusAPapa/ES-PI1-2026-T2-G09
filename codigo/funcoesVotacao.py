from datetime import datetime
import random
import conexaobd
import verificacoes
import os
import criptografia_descriptografia

def registrar_log(mensagem):
    #regista a hora que ocorrerá o log
    data_hora = datetime.now().strftime("%Y-%m-%d - %H:%M:%S")
    
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
    protocolo_criptografado = criptografia_descriptografia.criptografar(protocolo)
    return protocolo, protocolo_criptografado

def exibir_protocolos():
    conexaobd.cursor.execute("SELECT protocolo_voto, data_hora FROM votos")
    resultados = conexaobd.cursor.fetchall()

    print("\n================================================")
    print("             Protocolos de Votacao")
    print("================================================")

    if not resultados:
        print("Nenhum protocolo registrado.")
    else:
        for i, (protocolo_cifrado, data_hora) in resultados:
            try:
                protocolo_original = criptografia_descriptografia.descriptografar(protocolo_cifrado)
                protocolo_original = protocolo_original.rstrip('A')
            except Exception:
                protocolo_original = protocolo_cifrado

def verificar_eleitor(titulo_eleitor, cpf_eleitor, chave_acesso_eleitor):
    # a função verifica se o eleitor está no banco de dados e se ele já votou
    sql = 'SELECT cpf, numero_titulo, chave_acesso, status_de_voto FROM eleitores WHERE numero_titulo=%s'
    values = [titulo_eleitor]
    conexaobd.cursor.execute(sql, values)
    
    resultado = conexaobd.cursor.fetchone()
    
    # verifica se o eleitor está cadastrado
    if resultado is None:
        print('Eleitor não encontrado!\n')
        return False
    cpf_banco, _, chave_banco, ja_votou = resultado
    cpf_real = criptografia_descriptografia.descriptografar(cpf_banco)

    #verificando se o cpf confere com o do banco de dados
    cpf = resultado[0]
    if cpf_eleitor != cpf[0:4]:
        print('Valídação dos dados falhou, pois o cpf está errado\n')
        return False
    
    #verificando se a chave de acesso comfere com a do banco
    chave_de_acesso = resultado[2]
    if chave_acesso_eleitor != chave_de_acesso:
        return False
    chave_eleitor_criptografada = criptografia_descriptografia.criptografar(chave_acesso_eleitor)

    #verificando se o eleitor já votou
    ja_votou = resultado[3]
    if ja_votou == True:
        print('Não é possível votar duas vezes!\n')
        return False
    return True

def sistema_votacao (titulo_abrindo, cpf_abrindo, chave_acesso_abrindo):
    
    #pega os dados de quem ta abrindo o sistema no banco de dados
    sql = ('SELECT cpf, numero_titulo, mesario, chave_acesso FROM eleitores WHERE numero_titulo=%s')
    values = [titulo_abrindo]
    conexaobd.cursor.execute(sql, values)
    cpf, numero_titulo, mesario, chave_acesso = conexaobd.cursor.fetchone()

    #compara os dados do banco de dados com os dados informados pelo usuáro abrindo o sistema
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
    print('\nSistema de votação aberto com sucesso!')
    input('Precione enter para iniciar a zerézima! ')
        
    #fazendo a zerézima
        #deleta todos os votos
    conexaobd.cursor.execute('DELETE FROM votos')
    conexaobd.conexao.commit()
        #deleta o status de voto dos eleitores, assim fazendo com que todos inicie a votação sem ter votado
    conexaobd.cursor.execute('UPDATE eleitores SET status_de_voto = FALSE')  
    conexaobd.conexao.commit()

    conexaobd.cursor.execute('''
    SELECT c.nome, c.numero, COUNT(v.voto) AS total_votos
    FROM candidatos AS c
    LEFT JOIN votos AS v ON c.numero = v.voto
    GROUP BY c.numero, c.nome
    ''')

    os.system('cls')
    print('\n=================================================')
    print(f'{'Zerézima realizada':^50}')
    print('\nCandidatos:')
    for (nome, numero, total_votos) in conexaobd.cursor.fetchall():
        print(f'\nNúmero: {numero} - Nome: {nome} - Total de votos: {total_votos}')
    print('=================================================\n')
    input('Precione enter para iniciar a votação! ')

    os.system('cls')
    #computação dos votos
    print("\n================================================")
    print(f'{'Votação':^50}')
    print("================================================")
    encerrar = 1
    while encerrar == 1:
        print('''
=======================================
        Identificaçao do eleitor
=======================================
        ''')

        #verificando validade do título
        titulo_eleitor = str(input('Digite seu título de eleitor: '))
        while verificacoes.verificarTitulo(titulo_eleitor) == False:
            print('Título de eleitor inválido!')
            titulo_eleitor = str(input('Informe o título de eleitor: '))
        cpf = str(input('Digite os 4 primeiros dígitos do seu CPF: '))
        chave_acesso = str(input('Digite a sua chave de acesso: '))

        #verificando se o eleitor está no sistema
        if not verificar_eleitor(titulo_eleitor, cpf, chave_acesso):
            continue
        
        print('\nEleitor encontrado!')
        confirmacao = 'n'
        while confirmacao.lower() not in ['s', 'sim']:
            voto = int(input('\nDigite o número do candidato para votar: '))
            sql = ('SELECT nome, partido FROM candidatos WHERE numero=%s')
            valores = [voto]
            conexaobd.cursor.execute(sql, valores)
            candidato = conexaobd.cursor.fetchone()
            while candidato == None:
                print('Candidato não encontrado!')
                voto = int(input('Digite o número de um candidato existente: '))
                sql = ('SELECT nome, partido FROM candidatos WHERE numero=%s')
                valores = [voto]
                conexaobd.cursor.execute(sql, valores)
                candidato = conexaobd.cursor.fetchone()
            
            print(f'''
            ======================================
                        Candidato
            ======================================
            Candidato: {candidato[0]}
            Partido: {candidato[1]}
            ''')
            confirmacao = str(input(f'Confirme o voto [S - votar em {candidato[0]}/N - votar em outra pessoa]: '))
            while confirmacao.lower() not in ['s', 'sim', 'n', 'nao', 'não']:
                confirmacao = str(input(f'Escolha uma oção válida[S/N]: '))
    
        #computar voto
        protocolo = gerar_protocolo_votacao(voto)
        data_hora = datetime.now().strftime("%Y/%m/%d - %H:%M:%S")
        sql = 'INSERT INTO votos (voto, protocolo_voto, data_hora) VALUES (%s, %s, %s)'
        valores = [voto, protocolo, data_hora]
        conexaobd.cursor.execute(sql, valores)
        conexaobd.conexao.commit()

        sql = 'UPDATE eleitores SET status_de_voto = TRUE WHERE numero_titulo = %s'
        valores = [titulo_eleitor]
        conexaobd.cursor.execute(sql, valores)
        conexaobd.conexao.commit()
        print('Voto registrado com sucesso!')
        print(f'Protocolo da votação: {protocolo}')
        input('Precione enter para continuar! ')

        os.system('cls')
        print('\n======================================')
        print('1 - Voltar à votar')
        print('2 - Encerrar votação')
        print('======================================')

        encerrar = int(input('Digite a ação desejada: '))
        while encerrar not in [1, 2]: 
            encerrar = int(input('Digite a ação desejada: '))
        
        os.system('cls')
        match encerrar:
            case 1:
                #aqui o continue també faz voltar à votação
                continue
            case 2:
                print('\n======================================')
                print('         Encerrando votação')
                print('======================================')
                encerrando = 'n'
                while encerrando.lower() in ['n', 'nao', 'não']:
                    titulo_eleitor = str(input('Digite o título de eleitor: '))
                    while verificacoes.verificarTitulo(titulo_eleitor) == False:
                        print('Título de eleitor inválido!')
                        titulo_eleitor = str(input('Informe o título de eleitor: '))
                    cpf = str(input('Digite os 4 primeiros dígitos do seu CPF: '))
                    chave_acesso = str(input('Digite a sua chave de acesso: '))

                    sql = ('SELECT cpf, numero_titulo, mesario, chave_acesso FROM eleitores WHERE numero_titulo=%s')
                    valores = [titulo_eleitor]
                    conexaobd.cursor.execute(sql, valores)
                    mesario = conexaobd.cursor.fetchone()

                    if mesario == None:
                        print('Mesario não encontrado no sistema! Faça o login novamente')
                        continue
                    
                    #guarda os valores do banco de dados e depois verifica se pode encerrar a votação
                    cpf_mesario = mesario[0]
                    status_mesario = mesario[2]
                        #verificando se o cpf está correto:
                    if cpf != cpf_mesario[0:4]:
                        print('Erro ao validar dados! CPF incorreto!')
                        continue
                        #verificando se é mesário
                    if status_mesario == False:
                        print('Você não tem permição para encerrar o sistema!')
                        continue
                    
                    encerrando = str(input('Deseja realmente encerrar a votação [S/N]? '))
                    while encerrando.lower() not in ['s', 'sim', 'n', 'nao', 'não']:
                        encerrando = str(input(f'Escolha uma oção válida[S/N]: '))
                    if encerrando.lower() in ['s', 'sim']:
                        encerrar = 2
                        print('\nVotação encerrada com sucesso!')
                    else:                   
                        encerrar = 1
                        break


def boletim_urna():
    conexaobd.cursor.execute
    resultados = conexaobd.cursor.fetchall()
    print('\n======================================')
    print('              Boletim de Urna')
    print('======================================')

    if not resultados:
        print("  Nenhum candidato cadastrado.")
        print("================================================\n")
        return
    vencedor = None
    max_votos = -1

    for nome, numero, partido, total_votos in resultados:
        print(f"  {nome} (Nº {numero} - {partido}): {total_votos} voto(s)")
        if total_votos > max_votos:
            max_votos = total_votos
            vencedor = (nome, numero, partido, total_votos)
        print(f"\nVencedor: {vencedor[0]}")
        print(f"Numero: {vencedor[1]}  |  Partido: {vencedor[2]}  |  Votos: {vencedor[3]}") 