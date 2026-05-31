from datetime import datetime
import random
import conexaobd
import verificacoes
import os
import criptografia_descriptografia

def registrar_log(mensagem):
    #função que faz o registro do log e registra a hora que ocorrerá o log, parametro é a mensagem do log.

    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    #tenta registra o log no arquivo txt, caso não de mostrará uma mensagem de erro
    try:
        with open("codigo/logs_ocorrencia.txt", "a", encoding="utf-8") as arq:
            arq.write(f"{data_hora} -> {mensagem}\n")
    except:
        print("não foi possível salvar o log")

def exibir_logs ():
    # Essa função faz a leitura dos logs no arquivo txt e depois printa, caso não exista o arquivo será mostrado uma mensagem de erro
    try:
        with open("codigo/logs_ocorrencia.txt", "r", encoding="utf-8") as arq:
            conteudo = arq.read()
            print(conteudo)
    except FileNotFoundError:
        print('Arquivo não encontrado')

def gerar_protocolo_votacao (candidato):
    #Função que gera o protocolo de votação a partir do candidato que votou.
    
    # obtenção das letras e dos números aleários do protocolo
    alfabeto = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M','N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    letras_aleatorias = ''.join(random.choices(alfabeto, k=2))
    numeros_aleatorios = random.randint(10000, 99999)

    #todo protocolo nulo terá 'NL" ao invés do número do candidato
    if candidato == None:
        candidato = 'NL'
    protocolo = 'V' + letras_aleatorias + '26' + str(candidato) + str(numeros_aleatorios)
    
    # criptografando e fazendo o retorno do protocolo, tanto criptografado(guardado no banco) qunato o normal(exibido para o eleitor após confirmação do voto)
    protocolo_criptografado = criptografia_descriptografia.criptografar(protocolo)
    return protocolo, protocolo_criptografado

def exibir_protocolos():
    #Função para fazer a listagem dos protocólos de votação

    # busca no banco
    conexaobd.cursor.execute("SELECT protocolo_voto, data_hora FROM votos")
    resultados = conexaobd.cursor.fetchall()

    print("\n================================================")
    print("             Protocolos de Votacao")
    print("================================================")

    # verificando se tem algum protocolo no banco
    if not resultados:
        print("Nenhum protocolo registrado.")
    else:
        #descriptografando os protocolos
        protocolos = []
        for (protocolo_cifrado, data_hora) in resultados:
            #descriptografando o protocolo e salvando na lista
            protocolo_original = criptografia_descriptografia.descriptografar(protocolo_cifrado).rstrip('A')
            protocolos.append((protocolo_original, data_hora))

        #ordenando os protocolos 
        protocolos.sort(key=lambda x: x[0])

        # for para o print dos protocolos
        for i, (protocolo_original, data_hora) in enumerate(protocolos):
            print(f"{i+1}. Protocolo: {protocolo_original} | Data/Hora: {data_hora}")

    
    print("================================================")

def verificar_eleitor(titulo_eleitor, cpf_eleitor, chave_acesso_eleitor):
    # a função verifica se o eleitor está no banco de dados e se ele já votou, para permitir que ele vote

    # busca no banco
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
        print('Valídação dos dados falhou, pois a chave de acessa está errada\n')
        return False

    #verificando se o eleitor já votou
    ja_votou = resultado[3]
    if ja_votou == True:
        print('Não é possível votar duas vezes!\n')
        registrar_log('ALERTA: Tentativa de voto duplo')
        return False
    return True

def sistema_votacao (titulo_abrindo, cpf_abrindo, chave_acesso_abrindo):
    #função do sistema de votação, parametros: título, CPF, chave de acesso, do usuário para verficar se é mesário

    #pega os dados de quem ta abrindo o sistema no banco de dados
    sql = ('SELECT cpf, mesario, chave_acesso FROM eleitores WHERE numero_titulo=%s')
    values = [titulo_abrindo]
    conexaobd.cursor.execute(sql, values)
    resultado = conexaobd.cursor.fetchone()

    #verificando se o título está cadastrado no banco
    if resultado is None:
        print('\nEleitor não encontrado no sistema!')
        registrar_log('ALERTA: Tentativa de acesso negada')
        return
    cpf, mesario, chave_acesso = resultado

    # descriptografando o cpf e a chave de acesso para fazer a comparação
    cpf = criptografia_descriptografia.descriptografar(cpf)
    chave_acesso = criptografia_descriptografia.descriptografar(chave_acesso).rstrip('A')

    # compara os dados do banco de dados com os dados com os dados informados pelo usuáro abrindo o sistema 
        # verificando se é mesário
    if mesario != True:
        print('\nVocê não tem permissão para abrir o sistema de votação!')
        registrar_log('ALERTA: Tentativa de acesso negada')
        # o return faz com a função encerra na hora
        return
        # verificando se os 4 dígitos do cpf informados confere com o armazenado no banco
    elif cpf_abrindo != cpf[0:4]:
        print('\nValídação dos dados falhou, pois o cpf está errado, não será possível fazer a abertura da votação! ')
        registrar_log('ALERTA: Tentativa de acesso negada')
        return
        # verificando se a chave de acesso informada confere com a chave armazenado no banco
    elif chave_acesso_abrindo != chave_acesso:
        print('\nValídação dos dados falhou, pois a chave de acesso está errada, não será possível fazer a abertura da votação! ')
        registrar_log('ALERTA: Tentativa de acesso negada')
        return
    # não teve nenhuma inconsitensia de dados, portanto o sistema pode ser aberto
    else:
        print('\nSistema de votação aberto com sucesso!')
    
    #fazendo a zerézima
    input('Precione enter para iniciar a zerézima! ')
        #deleta todos os votos
    conexaobd.cursor.execute('DELETE FROM votos')
    conexaobd.conexao.commit()
        #deleta o status de voto dos eleitores, assim fazendo com que todos inicie a votação sem ter votado
    conexaobd.cursor.execute('UPDATE eleitores SET status_de_voto = FALSE')  
    conexaobd.conexao.commit()

    # faz a contagem de cada candidato e mostra que todos estão com 0 votos
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
    registrar_log('ABERTURA: Votação iniciada com sucesso. Total de votos zerado.')      

    os.system('cls')
    # votação
    print("\n================================================")
    print(f'{'Votação':^50}')
    print("================================================")
    # encerrar == 1 faz com que continue votando, caso vire 2, entra na parte de encerar votação
    encerrar = 1
    while encerrar == 1:
        os.system('cls')
        print('\n===================================')
        print('1 - Votar')
        print('2 - Encerrar votação')
        print('===================================\n')
        #pergunta se irá votar ou encerrar
        encerrar = verificacoes.ler_opcao('Digite a ação desejada: ')
        while encerrar not in [1, 2]: 
            encerrar = verificacoes.ler_opcao('Digite a ação desejada: ')
        
        os.system('cls')
        match encerrar:
            # caso tenha escolhido votar
            case 1:
                print('''
=======================================
        Identificaçao do eleitor
=======================================
        ''')
                # apuração dos dados do eleitor
                    #verificando validade do título
                titulo_eleitor = str(input('Digite seu título de eleitor: '))
                while verificacoes.verificarTitulo(titulo_eleitor) == False:
                    titulo_eleitor = str(input('Informe o título de eleitor: '))
                cpf = str(input('Digite os 4 primeiros dígitos do seu CPF: '))
                chave_acesso = str(input('Digite a sua chave de acesso: '))

                    #verificando se o eleitor está no sistema e se o eleitor já votou
                if not verificar_eleitor(titulo_eleitor, cpf, chave_acesso):
                    input('Precione enter para voltar no menu de votação! ')
                    continue
                
                print('\nEleitor encontrado!')
                
                # esse laço faz com que o usuário fique colocando o candidato que ele quer votar até confirmar o voto
                confirmacao = 'n'
                while confirmacao.lower() not in ['s', 'sim']:
                    #verificando se o voto é um número e pedindo para o usuário digitar novamente caso contrário
                    voto = ''
                    while voto.isnumeric() == False:
                        try:
                            voto = int(input('\nDigite o número do candidato para votar: '))
                            break
                        except ValueError:
                            print('Digite apenas números!')
                    #busca do candidato no banco e verificando se ele existe
                    sql = ('SELECT nome, partido FROM candidatos WHERE numero=%s')
                    valores = [voto]
                    conexaobd.cursor.execute(sql, valores)
                    candidato = conexaobd.cursor.fetchone()
                    if candidato == None:
                        print('Voto nulo.')
                        # perguntando ao usuário se ele quer confirmar o voto nulo
                        confirmacao = str(input(f'VocÊ deseja votar nulo? [S - votar nulo/N - votar em outra pessoa]: '))
                        while confirmacao.lower() not in ['s', 'sim', 'n', 'nao', 'não']:
                            confirmacao = str(input(f'Escolha uma oção válida[S/N]: '))
                        if confirmacao.lower() in ['s', 'sim']:
                            voto = None
                            break
                        else:
                            continue
                        
                    else:
                        #mostra o candidato que o usuário escolheu
                        print(f'''
                ======================================
                            Candidato
                ======================================
                        Candidato: {candidato[0]}
                        Partido: {candidato[1]}
                        ''')
                        # perguntando ao usuário se ele quer confirmar o voto em tal candidato
                        confirmacao = str(input(f'Confirme o voto [S - votar em {candidato[0]}/N - votar em outra pessoa]: '))
                        while confirmacao.lower() not in ['s', 'sim', 'n', 'nao', 'não']:
                            confirmacao = str(input(f'Escolha uma oção válida[S/N]: '))
            
                #computar voto
                    # gerando protocolo e o horário do voto
                protocolo, protocolo_criptografado = gerar_protocolo_votacao(voto)
                data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    # guardando no banco
                sql = 'INSERT INTO votos (voto, protocolo_voto, data_hora) VALUES (%s, %s, %s)'
                valores = [voto, protocolo_criptografado, data_hora]
                conexaobd.cursor.execute(sql, valores)
                conexaobd.conexao.commit()

                    # atualizando status de voto
                sql = 'UPDATE eleitores SET status_de_voto = TRUE WHERE numero_titulo = %s'
                valores = [titulo_eleitor]
                conexaobd.cursor.execute(sql, valores)
                conexaobd.conexao.commit()
                
                # mostrando protocolo de votação
                print('\nVoto registrado com sucesso!')
                print(f'\nProtocolo da votação: {protocolo}')
                registrar_log('SUCESSO: Voto registrado com sucesso')
                input('Precione enter para continuar! ')
            case 2:
                # caso tenha escolhido encerar
                print('\n======================================')
                print('         Encerrando votação')
                print('======================================')
                # laço para continuar na parte de enceramento do sistema até o usuário ter acesso ao encerramento ou até ele cancelar o encerramento da votação e continuar votando
                encerrando = 'n'
                while encerrando.lower() in ['n', 'nao', 'não']:
                    # informando o usuári que caso ele queira cancelar o encerramento da votação basta digitar 0 em qualquer opção dos dados
                    print('\nCASO NECESSÀRIO, DIGITE 0 PARA CANCELSAR ENCERRAMENTO.\n')
                    titulo_eleitor = str(input('Digite o título de eleitor: '))
                    if titulo_eleitor != '0':
                        while verificacoes.verificarTitulo(titulo_eleitor) == False:
                            titulo_eleitor = str(input('Informe o título de eleitor: '))
                    else:
                        encerrar = 1
                        break
                    cpf = str(input('Digite os 4 primeiros dígitos do seu CPF: '))
                    chave_acesso = str(input('Digite a sua chave de acesso: '))

                    if cpf == '0' or chave_acesso == '0':
                        encerrar = 1
                        break
                        
                        # buscando no banco o eleito
                    sql = ('SELECT cpf, numero_titulo, mesario, chave_acesso FROM eleitores WHERE numero_titulo=%s')
                    valores = [titulo_eleitor]
                    conexaobd.cursor.execute(sql, valores)
                    mesario = conexaobd.cursor.fetchone()
                        # verificando e o eleitor achado é mesario
                    if mesario == None:
                        print('Mesario não encontrado no sistema! Faça o login novamente')
                        registrar_log('ALERTA: Tentativa de acesso negada')
                        continue
                    
                    #descriptografando os dados pegos no banco
                    cpf_mesario = criptografia_descriptografia.descriptografar(mesario[0]).rstrip('A')
                    chave_mesario = criptografia_descriptografia.descriptografar(mesario[3]).rstrip('A')
                    status_mesario = mesario[2]
                        #verificando se o cpf está correto:
                    if cpf != cpf_mesario[0:4]:
                        print('\nErro ao validar dados! CPF incorreto! Faça o login novamente!')
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

                    # perguntando se o usuário quer encerrar
                    encerrando = str(input('\nDeseja realmente encerrar a votação [S/N]? '))
                    while encerrando.lower() not in ['s', 'sim', 'n', 'nao', 'não']:
                        encerrando = str(input(f'Escolha uma oção válida[S/N]: '))

                        # caso queira é necessário confirmar a chave de acesso
                    if encerrando.lower() in ['s', 'sim']:
                        chave_acesso = str(input('\nConfirme a sua chave de acesso: '))
                        # esse laço da ao usuário 3 tentavias de acertar a chave de acesso, caso ele erre as 3 o sistema voltará para o menu de votação
                        for tentativas in range(3, 0, -1):
                            if chave_acesso == chave_mesario:
                                break
                            else:
                                print(f'\nErro ao validar chave de acesso! {tentativas - 1} tentativa(s) restantes!')
                                registrar_log('ALERTA: Erro ao validar chave de acesso!')
                                #verificando se ainda tem tentativas, caso tenha pedirá a confirmação da chave de acesso
                                if tentativas - 1 > 0:
                                    chave_acesso = str(input('\nConfirme a sua chave de acesso: '))
                                else:
                                    encerrar = 1
                                    registrar_log('ALERTA: Tentativas de validar chave de acesso para encerramento esgotadas!')
                                    break
                                    
                        if chave_acesso == chave_mesario:
                            encerrar = 2
                            print('\nVotação encerrada com sucesso!')
                            registrar_log('ENCERRAMENTO: Votação finalizada com sucesso.')
                            break
                    else:                   
                        encerrar = 1
                        break


def boletim_urna():
    #Função para visualizar o boletim de urna

    # fazendo a contagem dos votos de cada candidato
    cursor = conexaobd.conexao.cursor()
    cursor.execute("""
        SELECT c.nome, c.numero, c.partido, COUNT(v.voto) AS total_votos
        FROM candidatos AS c
        LEFT JOIN votos AS v 
        ON c.numero = v.voto
        GROUP BY c.numero, c.nome, c.partido
        ORDER BY c.nome ASC
    """)
    resultados = cursor.fetchall()

    sql = ("SELECT COUNT(*) FROM votos")
    cursor.execute(sql)
    #como o fetchone retorna uma tupla, por isso precisa do [0]
    total_geral = cursor.fetchone()[0]

    #fazendo a contagem dos votos nulos
    cursor.execute("SELECT COUNT(*) FROM votos WHERE voto IS NULL")
    votos_nulos = cursor.fetchone()[0]
    
    print('\n======================================')
    print('            Boletim de Urna')
    print('======================================')

        #caso não tenha nenhum voto cadastrado mostrará uma mensaegm de erro
    if not resultados:
        print("  Nenhum candidato cadastrado.")
        input('\nPressione Enter para voltar!')
        return
    vencedor = None
    max_votos = -1

    # dando print nos resultados e descobrindo o vencedor
    for nome, numero, partido, total_votos in resultados:
        if total_geral > 0: 
            porcentagem = (total_votos / total_geral) * 100 
        else:
            porcentagem = 0
        print(f"  {nome} (N {numero} - {partido}): {total_votos} voto(s) - {porcentagem:.1f}%")
        if total_votos > max_votos:
            max_votos = total_votos
            vencedor = (nome, numero, partido, total_votos)
    print(f'  Votos nulos: {votos_nulos} voto(s)')
    
    # dando print no vencedor
    if vencedor:
        print(f"\n  Vencedor: {vencedor[0]}")
        print(f"  Numero: {vencedor[1]}  |  Partido: {vencedor[2]}  |  Votos: {vencedor[3]}")
    cursor.close()


def estatisticas_comparecimento():
    #função para mostrar o percentual de eleitores que votaram.

    # fazendo a contagem de leitores e votos cadastrados no banco
    cursor = conexaobd.conexao.cursor()
    cursor.execute("SELECT COUNT(*) FROM eleitores")
    total_eleitores = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM eleitores WHERE status_de_voto = TRUE")
    total_votaram = cursor.fetchone()[0]

    # fazendo o percentual de eleitores que votaram
    percentual = (total_votaram / total_eleitores * 100) if total_eleitores > 0 else 0

    # mostrando o resultado
    print("\n======================================")
    print("   Estatisticas de Comparecimento")
    print("======================================")
    print(f"  Total de eleitores cadastrados: {total_eleitores}")
    print(f"  Total que votou               : {total_votaram}")
    print(f"  Percentual de comparecimento  : {percentual:.2f}%")
    cursor.close()

def votor_por_partido():
    #Função para mostrar o relatório de votos por partido.

    #fazendo a busca no banco
    cursor = conexaobd.conexao.cursor()
    cursor.execute("""
    SELECT c.partido, COUNT(v.voto) AS total_votos
    FROM candidatos AS c
    LEFT JOIN votos AS v ON c.numero = v.voto        
    GROUP BY c.partido
    ORDER BY total_votos DESC
    """)
    resultados = cursor.fetchall()

    #conta a quantidade total de votos registrados
    cursor.execute("SELECT COUNT(*) FROM votos")
    total_geral = cursor.fetchone()[0]

    #conta a quantidade de votos nulos
    cursor.execute("SELECT COUNT(*) FROM votos WHERE voto IS NULL OR voto = 0")
    votos_nulos = cursor.fetchone()[0]

    print("\n======================================")
    print("         Voto(s) por partido")
    print("======================================")
    # caso não tenha nehnum voto registrado mostrará esse mensagem de erro
    if not resultados:
        print("Nenhum partido encontrado")
        input('\nPressione Enter para voltar!')
    else:
        for partido, total in resultados:
            #cauculando a porcentagem de votos de cada partido
            porcentagem = (total / total_geral * 100) if total_geral > 0 else 0
            print(f"Partido: {partido}: {total} voto(s) - {porcentagem:.1f}%")
        #cauculando a porcentagem de votos nulos
        porcentagem_nulos = (votos_nulos / total_geral * 100) if total_geral > 0 else 0
        print(f"Votos nulos: {votos_nulos} - {porcentagem_nulos:.1f}%")
        
    cursor.close()

def validar_integridade():
    #Função para validar a integridade da votação a partir da diferença de pessoas que votaram e eleitores cadastrados.

    #fazendo a conta de eleitores e votos cadastrados no bd
    cursor = conexaobd.conexao.cursor()
    cursor.execute("SELECT COUNT(*) FROM votos")
    total_votos_urna = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM eleitores WHERE status_de_voto = TRUE")
    total_ja_votou = cursor.fetchone()[0]

    #mostrando a quantidade de elitores e votos registrados
    print("\n======================================")
    print("        Validação de Integridade")
    print("======================================")
    print(f"Votos registrados na urna    : {total_votos_urna}")
    print(f"Eleitores com status Ja Votou: {total_ja_votou}")
    
    #mostrando se a votção pode ter alguma inconsistência apartir da conta
    if total_votos_urna == total_ja_votou:
        print("\nIntegridade confirmada!")
    else:
        print("ATENÇÃO: os números não coincidem")
        print("Possível inconsistência na votação!")
        