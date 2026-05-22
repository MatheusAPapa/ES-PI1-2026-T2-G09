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

    #todo protocolo nulo terá 'NL" ao invés do número do candidato
    if candidato == None:
        candidato = 'NL'
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
        for i, (protocolo_cifrado, data_hora) in enumerate(resultados):  # ← enumerate aqui
            try:
                protocolo_original = criptografia_descriptografia.descriptografar(protocolo_cifrado)
                protocolo_original = protocolo_original.rstrip('A')
            except Exception:
                protocolo_original = protocolo_cifrado
            
            print(f"{i+1}. Protocolo: {protocolo_original} | Data/Hora: {data_hora}")
    
    print("================================================")

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
    
    # descriptografa os dados do banco antes de comparar
    cpf_banco = criptografia_descriptografia.descriptografar(resultado[0]).rstrip('A')
    chave_banco = criptografia_descriptografia.descriptografar(resultado[2]).rstrip('A')
    
    #verificando se o cpf confere com o do banco de dados
    if cpf_eleitor != cpf_banco[0:4]:
        print('Valídação dos dados falhou, pois o cpf está errado\n')
        return False
    
    #verificando se a chave de acesso comfere com a do banco
    if chave_acesso_eleitor != chave_banco:
        return False

    #verificando se o eleitor já votou
    ja_votou = resultado[3]
    if ja_votou == True:
        print('Não é possível votar duas vezes!\n')
        registrar_log('ALERTA: Tentativa de voto duplo')
        return False
    return True

def sistema_votacao (titulo_abrindo, cpf_abrindo, chave_acesso_abrindo):
    
    #pega os dados de quem ta abrindo o sistema no banco de dados
    sql = ('SELECT cpf, numero_titulo, mesario, chave_acesso FROM eleitores WHERE numero_titulo=%s')
    values = [titulo_abrindo]
    conexaobd.cursor.execute(sql, values)
    cpf, numero_titulo, mesario, chave_acesso = conexaobd.cursor.fetchone()

    # descriptografando
    cpf = criptografia_descriptografia.descriptografar(cpf)
    chave_acesso = criptografia_descriptografia.descriptografar(chave_acesso).rstrip('A')

    #compara os dados do banco de dados com os dados informados pelo usuáro abrindo o sistema
    if mesario != True:
        print('\nVocê não tem permissão para abrir o sistema de votação!')
        registrar_log('ALERTA: Tentativa de acesso negada')
        return
    elif cpf_abrindo != cpf[0:4]:
        print('\nValídação dos dados falhou, pois o cpf está errado, não será possível fazer a abertura da votação! ')
        registrar_log('ALERTA: Tentativa de acesso negada')
        return
    elif titulo_abrindo != numero_titulo:
        print('\nValídação dos dados falhou, pois o título de eleitor está errado, não será possível fazer a abertura da votação! ')
        registrar_log('ALERTA: Tentativa de acesso negada')
        return
    elif chave_acesso_abrindo != chave_acesso:
        print('\nValídação dos dados falhou, pois a chave de acesso está errada, não será possível fazer a abertura da votação! ')
        registrar_log('ALERTA: Tentativa de acesso negada')
        return
    else:
        print('\nSistema de votação aberto com sucesso!')
        registrar_log('ABERTURA: Sistema de votação aberto com sucesso')
    
    #fazendo a zerézima
    input('Precione enter para iniciar a zerézima! ')
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
    registrar_log('Zerézima realizada, total de votos zerado')      

    os.system('cls')
    #computação dos votos
    print("\n================================================")
    print(f'{'Votação':^50}')
    print("================================================")
    encerrar = 1
    while encerrar == 1:
        os.system('cls')
        print('\n===================================')
        print('1 - Votar')
        print('2 - Encerrar votação')
        print('===================================\n')

        encerrar = int(input('Digite a ação desejada: '))
        while encerrar not in [1, 2]: 
            encerrar = int(input('Digite a ação desejada: '))
        
        os.system('cls')
        match encerrar:
            case 1:
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

                #verificando se o eleitor está no sistema e se o eleitor já votou
                if not verificar_eleitor(titulo_eleitor, cpf, chave_acesso):
                    input('Precione enter para voltar no menu de votação! ')
                    continue
                
                print('\nEleitor encontrado!')
                confirmacao = 'n'
                while confirmacao.lower() not in ['s', 'sim']:
                    voto = int(input('\nDigite o número do candidato para votar: '))
                    sql = ('SELECT nome, partido FROM candidatos WHERE numero=%s')
                    valores = [voto]
                    conexaobd.cursor.execute(sql, valores)
                    candidato = conexaobd.cursor.fetchone()
                    if candidato == None:
                        print('Voto nulo.')
                        confirmacao = str(input(f'VocÊ deseja votar nulo? [S - votar nulo/N - votar em outra pessoa]: '))
                        while confirmacao.lower() not in ['s', 'sim', 'n', 'nao', 'não']:
                            confirmacao = str(input(f'Escolha uma oção válida[S/N]: '))
                        if confirmacao.lower() in ['s', 'sim']:
                            voto = None
                            break
                        else:
                            continue
                        
                    else:
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
                protocolo, protocolo_criptografado = gerar_protocolo_votacao(voto)
                data_hora = datetime.now().strftime("%Y/%m/%d - %H:%M:%S")
                sql = 'INSERT INTO votos (voto, protocolo_voto, data_hora) VALUES (%s, %s, %s)'
                valores = [voto, protocolo_criptografado, data_hora]
                conexaobd.cursor.execute(sql, valores)
                conexaobd.conexao.commit()

                sql = 'UPDATE eleitores SET status_de_voto = TRUE WHERE numero_titulo = %s'
                valores = [titulo_eleitor]
                conexaobd.cursor.execute(sql, valores)
                conexaobd.conexao.commit()
                print('Voto registrado com sucesso!')
                print(f'Protocolo da votação: {protocolo}')
                registrar_log('SUCESSO: Voto registrado com sucesso')
                input('Precione enter para continuar! ')
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
                        registrar_log('ALERTA: Tentativa de acesso negada')
                        continue
                    
                    #guarda os valores do banco de dados e depois verifica se pode encerrar a votação
                    cpf_mesario = criptografia_descriptografia.descriptografar(mesario[0]).rstrip('A')
                    chave_mesario = criptografia_descriptografia.descriptografar(mesario[3]).rstrip('A')
                    status_mesario = mesario[2]
                        #verificando se o cpf está correto:
                    if cpf != cpf_mesario[0:4]:
                        print('\nErro ao validar dados! CPF incorreto!\nFaça o login novamente:')
                        registrar_log('ALERTA: Tentativa de acesso negada')
                        continue
                        #verificando chave de acesso
                    elif chave_acesso != chave_mesario:
                        print('\nErro ao validar dados! Chave de acesso incorreta!\nFaça o login novamente:')
                        registrar_log('ALERTA: Tentativa de acesso negada')
                        continue
                        #verificando se é mesário
                    elif status_mesario == False:
                        print('\nVocê não tem permição para encerrar o sistema!\nFaça o login novamente:')
                        registrar_log('ALERTA: Tentativa de acesso negada')
                        continue
                    
                    encerrando = str(input('\nDeseja realmente encerrar a votação [S/N]? '))
                    chave_acesso = str(input('\nConfirme a sua chave de acesso: '))
                    while encerrando.lower() not in ['s', 'sim', 'n', 'nao', 'não']:
                        encerrando = str(input(f'Escolha uma oção válida[S/N]: '))
                    if encerrando.lower() in ['s', 'sim']:
                        while chave_acesso != chave_mesario:
                            print('\nErro ao validar chave de acesso!')
                            chave_acesso = str(input('\nConfirme a sua chave de acesso: '))
                            registrar_log('ALERTA: Erro ao validar chave de acesso!')
                            encerrando = 'n'
                            continue

                        encerrar = 2
                        print('\nVotação encerrada com sucesso!')
                        registrar_log('Votação encerrada')
                        break
                    else:                   
                        encerrar = 1
                        break


def boletim_urna():
    conexaobd.cursor.execute
    resultados = conexaobd.cursor.fetchall()
    