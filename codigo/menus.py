import os

#menu inicial
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
    escolha = int(input('Qual módulo você deseja entrar? '))
    
    #verificação de escolha válida
    while escolha not in (1, 2, 3):
        print('Opção inválida!')
        escolha = int(input('Selecione um opção válida: '))
    return escolha

#modulo de gerenciamento
def menuModGere ():
    os.system('cls')
    print('''
    ====================================
          Módulo de gerenciamento
    ====================================
          
    1 - Cadastrar eleitor 
    2 - Editar dados do eleitor
    3 - Todos os eleitores
    4 - Buscar eleitor
    5 - Remover eleitor 
    6 - Voltar para menu anterior   
 
    ====================================
          
    ''')
    opcao = int(input('Selecione uma das opções acima: '))
   
    #verificação de escolha válida
    while opcao not in (1, 2, 3, 4, 5, 6):
        print('Opção inválida!')
        opcao = int(input('Selecione um opção válida: '))
    return opcao

#modulo de votação
def menuModVota ():
    os.system('cls')
    print('''
    ====================================
            Módulo de votação
    ====================================
    
    1 - Abri sistema de votação
    2 - Auditoria da votação
    3 - Resultado da votação
    4 - Voltar para menu anterior
          
    ====================================
          
    ''')
    opcao = int(input('Selecione uma das opções acima: '))

    #verificação de escolha válida
    while opcao not in (1, 2, 3, 4):
        print('Opção inválida!')
        opcao = int(input('Selecione um opção válida: '))
    return opcao

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
    opcao = int(input('Selecione uma das opções acima: '))

    #verificação de escolha válida
    while opcao not in (1, 2, 3):
        print('Opção inválida!')
        opcao = int(input('Selecione um opção válida: '))
    
    return opcao

def menuResulVota ():
    os.system('cls')
    print('''
    ====================================
           Resultado da votação
    ====================================
          
    1 - Boletim de urna
    2 - Estatísticas 
    3 - Votos por partido
    4 - Validação de integridade
    5 - Voltar para menu anterior
          
    ====================================
          
    ''')
    opcao = int(input('Selecione uma das opções acima: '))
    
    #verificação de escolha válida
    while opcao not in (1, 2, 3, 4, 5):
        print('Opção inválida!')
        opcao = int(input('Selecione um opção válida: '))
    return opcao