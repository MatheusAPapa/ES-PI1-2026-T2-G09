import mysql.connector
import conexaobd
import random
import verificacoes
import os
import criptografia_descriptografia
import funcoesVotacao
import verificacoes

#Gera a chave de acesso a partir do nome do eleitor
def gerar_chave_acesso(nome):

    #remove os espaços e transforma a string em uma lista
    partes = nome.strip().split()
    
    # Pega as duas primeiras letras do primeiro nome e deixa em maiúsculo
    primeiro_nome = partes[0][:2].upper()
    
    # Primeira letra do segundo nome (se existir)
    if len(partes) >= 2:
        segunda_letra = partes[1][0].upper()
    else:
        segunda_letra = "X"   # caso tenha apenas um nome
    
    # Gera os 4 dígitos aleatórios da chave de acesso
    numeros = ''.join(str(random.randint(1000, 9999)))
    # Monta a chave, sendo essa: 2 letras do primeiro nome + inicial do segundo + 4 dígitos
    chave = primeiro_nome + segunda_letra + numeros
    return chave

# Cadastra o eleitor no banco e seus dados (nome, titulo, cpf e se será mesário)
def cadastrar_novo_eleitor(nome, numero_titulo, cpf, mesario):

    # Gerando a cheve de acesso do eleitor 
    chave_acesso = gerar_chave_acesso(nome)

    # ✅ Criptografa antes de salvar no banco
    cpf_criptografado = criptografia_descriptografia.criptografar(cpf)
    chave_criptografada = criptografia_descriptografia.criptografar(chave_acesso)

    # Inserindo no banco de dados os dados do eleitor
    try: 
        sql = "INSERT INTO eleitores (nome, cpf, numero_titulo, mesario, chave_acesso) VALUES (%s, %s, %s, %s, %s)"
        valores = (nome, cpf_criptografado, numero_titulo, mesario, chave_criptografada)
        conexaobd.cursor.execute(sql, valores)
        conexaobd.conexao.commit()
        # Exibir os dados cadastrados
        print("\n=====================================")
        print("✅ ELEITOR CADASTRADO COM SUCESSO!")
        print("=====================================\n")
        print(f"Nome: {nome}")
        print(f"Título: {numero_titulo}")
        print(f"CPF: {cpf}")
        print(f"Chave de acesso: {chave_acesso}")
        print(f"Mesário: {'Sim' if mesario else 'Não'}")
        input("\nPressione Enter para voltar a tela inicial...")
        funcoesVotacao.registrar_log('Novo eleitor cadastrado.')
    
    except mysql.connector.IntegrityError as err:
        if "Duplicate entry" in str(err):
            # Verificando duplicidade do cpf
            if "cpf" in str(err).lower():
                print("\n❌ Erro: Este CPF já está cadastrado no sistema!")
                input("\nPressione Enter para voltar!")
                
            # Verificando duplicidade de título de eleitor
            if "numero_titulo" in str(err).lower():
                print("\n❌ Erro: Este título de eleitor já está cadastrado no sistema!")
                input("\nPressione Enter para voltar!")
        else:
            print(f"\n❌ Erro: {err}")
    # Trata erros genéricos de banco de dados (conexão, sintaxe SQL, etc.)
    except mysql.connector.Error as err:
        print(f"\n❌ Erro ao cadastrar no banco de dados: {err}")
        input('\nPrecione enter para voltar! ')

# Faz a listagem de todos os eleitores cadastrados no banco de dados, mostrando o nome, se é mesário e se já votou
def listar_eleitores():
    # Busca o nome, status de voto e se é mesario ou não na tabela de eleitores, no banco de dados
    conexaobd.cursor.execute('SELECT nome, mesario, status_de_voto FROM eleitores')
    contador = 0
    # Faz o print da listagem de todos os eleitores 
    for (nome, mesario, status_de_voto) in conexaobd.cursor.fetchall():
        contador += 1
        print(f'Eleitor {contador} -> Nome: {nome} - Mesario: {'mesario' if mesario == 1 else 'não mesario'} - Status do voto: {'Pendente' if status_de_voto == 0 else 'Votou'}')
    
def busca_eleitores(busca):
    match busca:
        #busca por cpf
        case 1:
            cpf = str(input("Digite o CPF do eleitor: "))
            while verificacoes.verificarCPF(cpf) == False:
                cpf = str(input('Informe o CPF do eleitor: '))

            cpf_criptografado = criptografia_descriptografia.criptografar(cpf)
            sql = "SELECT nome, mesario, status_de_voto FROM eleitores WHERE cpf=%s"
            valores = [cpf_criptografado]
            conexaobd.cursor.execute(sql, valores)
            
        #busca por título de eleitor
        case 2:
            titulo = str(input("Digite o títudo de eleitor: "))
            while verificacoes.verificarTitulo(titulo) == False:
                titulo = str(input('Informe o titulo do eleitor: '))
            
            sql = "SELECT nome, mesario, status_de_voto FROM eleitores WHERE numero_titulo=%s"
            valores = [titulo]
            conexaobd.cursor.execute(sql, valores)
    # faz o print dos dados do eleitor ou mostra uma mensagem de erro caso esse eleitor não esteja cadastrado
    eleitor = conexaobd.cursor.fetchone()
    #fetchone retorna uma tupla com os valores do banco de dados(apenas de uma linha), caso não aja eleitor será retornado None
    if eleitor is None:
        print('Eleitor não encontrado!')
        return
    else:
        nome, mesario, status_de_voto = eleitor
        print(f'\nNome: {nome} - Mesario: {'Será mesario' if mesario == 1 else 'Não mesario'} - Status do voto: {'Pendente' if status_de_voto == 0 else 'Votou'}')

# Deleta eleitor do sistema e do banco de dados
def deletar_eleitor(cpf, titulo):
    # Criptografia o CPF do eleito para buscar no banco de dados
    cpf_criptografado = criptografia_descriptografia.criptografar(cpf)

    sql_busca = "SELECT cpf FROM eleitores WHERE cpf = %s AND numero_titulo = %s"
    conexaobd.cursor.execute(sql_busca, (cpf_criptografado, titulo))

    if conexaobd.cursor.fetchone() is None:
        print('Eleitor não encontrado!')
        return

    else:
        sql = "DELETE FROM eleitores WHERE cpf=%s and numero_titulo=%s"
        values = (cpf_criptografado, titulo)
        conexaobd.cursor.execute(sql, values)
        conexaobd.conexao.commit()
        print('Eleitor removido com sucesso!')

# Essa função pode alterar os dados do eleitor
def alterar_dados_eleitor(cpf):
    # Criptografa o CPF para buscar no banco de dados
    cpf_criptografado = criptografia_descriptografia.criptografar(cpf)
    try:
        # Busca o nome, numero do titulo, se é mesario, chave de acesso da tabela de eleitores, de acordo com o CPF digitado
        sql_busca = "SELECT nome, numero_titulo, mesario, chave_acesso FROM eleitores WHERE cpf = %s"
        valores = [cpf_criptografado]
        conexaobd.cursor.execute(sql_busca, valores)
        eleitor = conexaobd.cursor.fetchone()
        # se nao encontrado o eleitor pede novamente o CPF
        while eleitor is None:
            os.system('cls')
            print("\n=====================================")
            print("❌ ELEITOR NÃO ENCONTRADO!")
            print("=====================================\n")
            
            cpf = str(input("Digite o CPF do eleitor: "))

            # Verifica se o CPF é valido, se não for valido ele pede para digitar novamente
            while not verificacoes.verificarCPF(cpf):
                print('CPF inválido. Digite novamente.')
                cpf = str(input("Digite o CPF do eleitor: "))
            # Criptografa o CPF para buscar no banco de dados
            cpf_criptografado = criptografia_descriptografia.criptografar(cpf)
            conexaobd.cursor.execute(sql_busca, [cpf_criptografado])
            eleitor = conexaobd.cursor.fetchone()

            
        # Atribuindo dados ao eleitor à variaveis
        nome, numero_titulo, mesario, chave_acesso = eleitor
        
        os.system('cls')
        # Menu de  opção de edição
        print("\n=====================================")
        print(f"ELEITOR ENCONTRADO: {nome}")
        print("=====================================\n")
        print("O QUE DESEJA EDITAR?")
        print("1 - Nome")
        print("2 - Número do título de eleitor")
        print("3 - CPF")
        print("4 - Status de mesário")
        print("0 - Cancelar")
        opcao = verificacoes.ler_opcao("\nEscolha uma opção: ")

        # Verifica se a opção escolhida existe, se não existir pede para escolher novamente
        while opcao not in [0, 1, 2, 3, 4]:
            print("\n❌ Opção inválida!")
            opcao = verificacoes.ler_opcao("\nEscolha uma opção válida: ")

        match opcao:
            # Sai do meni de edição
            case 0:
                print("Edição cancelada!")
                input("Pressione Enter para voltar a tela inicial...")
                # o return força sair da função
                return
                
            # Altera o nome do eleitor
            case 1:        
                novo_nome = str(input("Informe o novo nome do eleitor: "))
                # Atualiza no banco de dados
                sql = "UPDATE eleitores SET nome = %s WHERE cpf = %s"  
                conexaobd.cursor.execute(sql, [novo_nome, cpf_criptografado])        
            # Altera o numero do titulo do eleitor
            case 2:
                novo_titulo = str(input("Digite o novo número do título: "))
                # Verifica se o novo titulo é valido
                while verificacoes.verificarTitulo(novo_titulo) == False:
                    novo_titulo = str(input("Digite o novo título de eleitor: "))

                # Verificando se o título de eleitor novo é o mesmo do atual
                if novo_titulo == numero_titulo:
                    print("\n⚠️ Este já é o título atual do eleitor!")
                    input("\nPressione Enter para voltar!")
                    return
                sql = "UPDATE eleitores SET numero_titulo = %s WHERE cpf = %s"
                conexaobd.cursor.execute(sql, [novo_titulo, cpf_criptografado])      
            # Altera o CPF do eleitor
            case 3:
                novo_cpf = str(input("Digite o novo CPF: "))
                # Verifica se o novo CPF é valido
                while verificacoes.verificarCPF(novo_cpf) == False:
                    novo_cpf = str(input("Digite o novo CPF: "))

                novo_cpf = criptografia_descriptografia.criptografar(novo_cpf)

                # Verificando se o cpf novo é o mesmo do atual
                if novo_cpf == cpf_criptografado:
                    print("\n⚠️ Este já é o CPF atual do eleitor!")
                    input("\nPressione Enter para voltar!")
                    return
                sql = "UPDATE eleitores SET cpf = %s WHERE cpf = %s"
                conexaobd.cursor.execute(sql, [novo_cpf, cpf_criptografado])        
            # Altera o status de mesario
            case 4:
                print("Eleitor é mesário?")
                print("1 - Sim")
                print("2 - Não")
                opcao_mesario = verificacoes.ler_opcao("Escolha: ")

                while opcao_mesario not in [1, 2]:  
                    print('Opção inválida!')
                    opcao_mesario = verificacoes.ler_opcao("Escolha: ")

                if opcao_mesario == 1:
                    novo_valor = True
                else:
                    novo_valor = False
                sql = "UPDATE eleitores SET mesario = %s WHERE cpf = %s"
                conexaobd.cursor.execute(sql, [novo_valor, cpf_criptografado])       
                

        conexaobd.conexao.commit()
        
        # Mostrando os dados do eleitor após alteração
        cpf_busca = novo_cpf if opcao == 3 else cpf_criptografado
        # Limpa o cache do cursor, assim mostrando os dados atualizado, não os atingos
        conexaobd.cursor = conexaobd.conexao.cursor()

        # Busca o nome, CPF, numero do itulo de eleitor, se é mesario, chave de acesso da tabela de eleitores, de acordo com o CPF inserido, mas com os dados atualizados
        sql_busca = "SELECT nome, cpf, numero_titulo, mesario, chave_acesso FROM eleitores WHERE cpf = %s"
        conexaobd.cursor.execute(sql_busca, [cpf_busca])
        eleitor = conexaobd.cursor.fetchone()

        #  Atribuindo dados ao eleitor à variaveis
        nome, cpf, numero_titulo, mesario, chave_acesso = eleitor 

        os.system('cls')
        # Menu de resuldado da edição
        print("\n=====================================")
        print("✅ DADOS ATUALIZADOS COM SUCESSO!")
        print("=====================================\n")
        print(f"Nome: {nome}")
        print(f"Título: {numero_titulo}")
        print(f"CPF: {criptografia_descriptografia.descriptografar(cpf).rstrip('A')}")
        print(f"Chave de acesso: {criptografia_descriptografia.descriptografar(chave_acesso).rstrip('A')}")
        print(f"Mesário: {'Sim' if mesario == 1 else 'Não'}")
        input("\nPressione Enter para voltar!")
        funcoesVotacao.registrar_log('Foi alterado os dados de um eleitor.')
    # Erros de duplicidade
    except mysql.connector.IntegrityError as err:
        if "cpf" in str(err).lower():
            print("\n❌ Erro: Este CPF já está cadastrado no sistema!")
        elif "numero_titulo" in str(err).lower():
            print("\n❌ Erro: Este título já está cadastrado no sistema!")
        else:
            print(f"\n❌ Erro: {err}")
        input('\nPrecione enter para voltar! ')
    # Erros de conexão
    except mysql.connector.Error as err:
        print(f"\n❌ Erro ao editar no banco de dados: {err}")
        input('\nPrecione enter para voltar! ')