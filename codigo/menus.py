import os
from verificacoes import ler_opcao

# Menu inicial
def menuInic ():
    os.system('cls')
    print('''
    ====================================
              Menu Inicial
    ====================================
          
    1 - Módulo de gerênciamento
    2 - Módulo de votação
    3 - Sair do sistema
          
    ====================================
          
    ''')
    escolha = ler_opcao('Qual módulo você deseja entrar? ')
    
    # Verificação de escolha válida
    while escolha not in (1, 2, 3):
        print('Opção inválida!')
        escolha = ler_opcao('Selecione um opção válida: ')
    return escolha

# Modulo de gerenciamento
def menuModGere ():
    os.system('cls')
    print('''
    ====================================
          Módulo de gerenciamento
    ====================================
          
    1 - Cadastrar eleitor 
    2 - Editar dados do eleitor
    3 - Listar todos os eleitores
    4 - Buscar eleitor
    5 - Remover eleitor 
    6 - Voltar para menu anterior   
 
    ====================================
          
    ''')
    opcao = ler_opcao('\nSelecione uma das opções acima: ')
   
    # Verificação de escolha válida
    while opcao not in (1, 2, 3, 4, 5, 6):
        print('Opção inválida!')
        opcao = ler_opcao('\nSelecione um opção válida: ')
    return opcao

# Modulo de votação
def menuModVota ():
    os.system('cls')
    print('''
    ====================================
            Módulo de votação
    ====================================
    
    1 - Abrir sistema de votação
    2 - Auditoria da votação
    3 - Resultado da votação
    4 - Voltar para menu anterior
          
    ====================================
          
    ''')
    opcao = ler_opcao('Selecione uma das opções acima: ')

    # Verificação de escolha válida
    while opcao not in (1, 2, 3, 4):
        print('Opção inválida!')
        opcao = ler_opcao('Selecione um opção válida: ')
    return opcao
# Modulo de auditoria da votação
def menuAudVota ():
    os.system('cls')
    print('''
    ====================================
            Auditoria da votação
    ====================================
          
    1 - Logs da votação
    2 - Protocolos de votação
    3 - Voltar para menu anterior
          
    ====================================
          
    ''')
    opcao = ler_opcao('Selecione uma das opções acima: ')

    # Verificação de escolha válida
    while opcao not in (1, 2, 3):
        print('Opção inválida!')
        opcao = ler_opcao('Selecione um opção válida: ')
    
    return opcao
# Modul de resultado da votação
def menuResulVota ():
    os.system('cls')
    print('''
    ====================================
           Resultado da votação
    ====================================
          
    1 - Boletim de urna
    2 - Estatísticas 
    3 - Validar votação
    4 - Voltar para menu anterior
          
    ====================================
          
    ''')
    opcao = ler_opcao('Selecione uma das opções acima: ')
    
    # Verificação de escolha válida
    while opcao not in (1, 2, 3, 4):
        print('Opção inválida!')
        opcao = ler_opcao('Selecione um opção válida: ')
    return opcao