import mysql.connector
import conexaobd
import random

def gerar_chave_acesso(nome):
    """Gera a chave de acesso no formato solicitado a partir do nome do eleitor"""

    #remove os espaços e sapara as palavras em listas
    partes = nome.strip().split()
    
    # Duas primeiras letras do primeiro nome e deixa em maiúsculo
    primeiro_nome = partes[0][:2].upper()
    
    # Primeira letra do segundo nome (se existir)
    if len(partes) >= 2:
        segunda_letra = partes[1][0].upper()
    else:
        segunda_letra = "X"   # caso tenha apenas um nome
    
    # gera os 4 dígitos aleatórios da chave de acesso
    numeros = ''.join(str(random.randint(1000, 9999)))
    
    chave = primeiro_nome + segunda_letra + numeros
    return chave

def cadastrar_novo_eleitor(nome, numero_titulo, cpf, mesario):
    #gerando a cheve de acesso do eleitor
    chave_acesso = gerar_chave_acesso(nome)

    # Inserindo no banco de dados os dados do eleitor
    try: 
        sql = "INSERT INTO eleitores (nome, cpf, numero_titulo, mesario, chave_acesso) VALUES (%s, %s, %s, %s, %s)"
        valores = (nome, cpf, numero_titulo, mesario, chave_acesso)
        conexaobd.cursor.execute(sql, valores)
        conexaobd.conexao.commit()
        
        print("\n=====================================")
        print("✅ ELEITOR CADASTRADO COM SUCESSO!")
        print("=====================================\n")
        print(f"Nome: {nome}")
        print(f"Título: {numero_titulo}")
        print(f"CPF: {cpf}")
        print(f"Chave de acesso: {chave_acesso}")
        print(f"Mesário: {'Sim' if mesario else 'Não'}")
        input("\nPressione Enter para voltar a tela inicial...")
    
    except mysql.connector.IntegrityError as err:
        if "Duplicate entry" in str(err):
            #verificando duplicidade do cpf
            if "cpf" in str(err).lower():
                print("\n❌ Erro: Este CPF já está cadastrado no sistema!")
                input("\nPressione Enter para voltar a tela inicial...")
                
            #verificando duplicidade de título de eleitor
            if "numero_titulo" in str(err).lower():
                print("\n❌ Erro: Este título de eleitor já está cadastrado no sistema!")
                input("\nPressione Enter para voltar a tela inicial...")
        else:
            print(f"\n❌ Erro: {err}")
            
    except mysql.connector.Error as err:
        print(f"\n❌ Erro ao cadastrar no banco de dados: {err}")
        input("\nPressione Enter para voltar a tela inicial...")

    finally:
        if 'conn' in locals() and conexaobd.conexao.is_connected():
            conexaobd.cursor.close()
            conexaobd.conexao.close()

def listar_eleitores():
    conexaobd.cursor.execute('SELECT id, nome, mesario, status_de_voto FROM eleitores')
    for (id, nome, mesario, status_de_voto) in conexaobd.cursor.fetchall():
        print(f'ID: {id} - Nome: {nome} - Mesario: {mesario} - Status do voto: {'Pendente' if status_de_voto == 0 else 'Votou'}')
    
def busca_eleitores(cpf, titulo):
    sql = "SELECT id, nome, mesario, status_de_voto FROM eleitores WHERE cpf=%s and numero_titulo=%s"
    valores = (cpf, titulo)
    conexaobd.cursor.execute(sql, valores)

    try:
        #fetchone retorna uma tupla com os valores do banco de dados(apenas de uma linha), caso não aja eleitor será retornado None
        id, nome, mesario, status_de_voto = conexaobd.cursor.fetchone()
        print(f'ID: {id} - Nome: {nome} - Mesario: {'Será mesario' if mesario == 1 else 'Não mesario'} - Status do voto: {'Pendente' if status_de_voto == 0 else 'Votou'}')
    except:
        print('Eleitor não encontrado!')

def deletar_eleitor(cpf, titulo):
    try:
        sql = "DELETE FROM eleitores WHERE cpf=%s and numero_titulo=%s"
        values = (cpf, titulo)
        conexaobd.cursor.execute(sql, values)
        conexaobd.conexao.commit()
        print('Eleitor removido com sucesso')
    except Exception as e:
        conexaobd.conexao.rollback()
        print(f'Eleitor não encontrado! {e}')

def alterar_dados_eleitor(nome, numero_titulo, cpf, mesario, chave_acesso):
    try:
        cpf = input("Digite o CPF do eleitor: ")
        sql_busca = "SELECT * FROM eleitores WHERE cpf = %s"
        conexaobd.cursor.execute(sql, ) # não sei oq colocar dentro do ()
        eleitor = conexaobd.cursor.fetchone()
        if eleitor is None:
            print("\n=====================================")
            print("❌ ELEITOR NÃO ENCONTRADO!")
            print("=====================================\n")

        print("\n=====================================")
        print(f"\nELEITOR ENCONTRADO: {nome}")
        print("=====================================\n")

        print("\n=====================================")
        print("  O QUE DESEJA EDITAR?")
        print("=====================================\n")
        print("\nO que deseja editar?")
        print("1 - Nome")
        print("2 - Número do titulo de eleitor")
        print("3 - CPF")
        print("4 - Status de mesário")
        print("0 - Cancelar")
        opcao = input("\nEscolha uma opção: ")

    
        match opcao:
            case 0:
                print("Edição cancelada!")
                input("Pressione Enter para voltar a tela inicial...")
                return
            case 1:
                novo_nome = input("Informe o  novo nome do eleitor: ")
                sql = "UPDATE eleitores SET nome = %s, WHERE cpf = %s"
                conexaobd.cursor.execute(sql, ) # nao sei oq coloca dentro do ()
            case 2:
                novo_titulo = input("Digite o novo número do título: ")
                sql = "UPDATE eleitores SET numero_titulo = %s WHERE cpf = %s"
                conexaobd.cursor.execute(sql, ) #nao sei oq coloca dentro do ()
            case 3:
                novo_cpf = input("Digite o novo CPF: ")
                sql = "UPDATE eleitores SET cpf = %s WHERE cpf = %s"
                conexaobd.cursor.execute(sql, ) #nao sei oq coloca dentro do ()
            case 4:
                print("Eleitor é mesário?")
                print("1 - Sim")
                print("2 - Não")
                opcao_mesario = input("Escolha: ")
                match opcao_mesario:
                    case 1:
                        opcao_mesario == 1
                        novo_valor = True
                    case 2:
                        opcao_mesario == 2
                        novo_valor = False
                    case _:
                        print("\n❌ Opção inválida!")
                        input("\nPressione Enter para voltar a tela inicial...")
                        return

                sql = "UPDATE eleitores SET mesario = %s WHERE cpf = %s"
                conexaobd.cursor.execute(sql, ) #nao sei oq coloca dentro do ()
            case _:
                    print("\n❌ Opção inválida!")
                    input("\nPressione Enter para voltar a tela inicial...")
                    return
        conexaobd.conexao.commit(sql, )
        print("\n=====================================")
        print("✅ DADOS ATUALIZADOS COM SUCESSO!")
        print("=====================================\n")
        print(f"Nome: {nome}")
        print(f"Título: {numero_titulo}")
        print(f"CPF: {cpf}")
        print(f"Chave de acesso: {chave_acesso}")
        print(f"Mesário: {'Sim' if mesario else 'Não'}")
        input("\nPressione Enter para voltar a tela inicial...")
   
    except mysql.connector.IntegrityError as err:
        match "cpf" in str(err).lower(), "numero_titulo" in str(err).lower():
            case (True, _):
                print("\n❌ Erro: Este CPF já está cadastrado no sistema!")
                input("\nPressione Enter para voltar a tela inicial...")
            case (_, True):
                print("\n❌ Erro: Este título já está cadastrado no sistema!")
                input("\nPressione Enter para voltar a tela inicial...")
            case _:
                print(f"\n❌ Erro: {err}")

    except mysql.connector.Error as err:
        print(f"\n❌ Erro ao editar no banco de dados: {err}")
        input("\nPressione Enter para voltar a tela inicial...")

    finally:
        if 'conn' in locals() and conexaobd.conexao.is_connected():
            conexaobd.cursor.close()
            conexaobd.conexao.close()
