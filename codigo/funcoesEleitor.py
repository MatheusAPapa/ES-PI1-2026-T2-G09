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
    
def busca_eleitores():
    sql = "SELECT id, nome, mesario, status_de_voto FROM eleitores WHERE id = 1"
    valores = ()
    conexaobd.cursor.execute(sql, valores)