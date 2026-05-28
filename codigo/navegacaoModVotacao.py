import menus 
import funcoesVotacao
import verificacoes
import os

def modAuditoria():
    opcaoAudVota = 0
    while opcaoAudVota != 3:
        opcaoAudVota = menus.menuAudVota()
        match opcaoAudVota:
            #logs 
            case 1:
                os.system('cls')
                funcoesVotacao.exibir_logs()
                input('\nPrecione enter para voltar! ')
            #protocolos
            case 2:
                os.system('cls')
                funcoesVotacao.exibir_protocolos()
                input('\nPrecione enter para voltar! ')    
            #voltar
            case 3: 
                return

def modResultado():
    opcaoResulVota = 0
    while opcaoResulVota != 4:
        opcaoResulVota = menus.menuResulVota()
        opcaoEstats = 0
        match opcaoResulVota:
            #boletim de urna
            case 1:
                os.system('cls')
                funcoesVotacao.boletim_urna()
                input('\nPressione Enter para voltar!')
            #estatísticas
            case 2:
                while opcaoEstats != 3:
                    os.system('cls')
                    print('''
    ====================================
           Resultado da votação
    ====================================
          
    1 - Estatísticas de comparencimento
    2 - Votos por partido
    3 - Voltar para o menu anterior

    ====================================
          
                ''')
                    opcaoEstats = verificacoes.ler_opcao('Selecione uma das opções acima: ')
            
                    #verificação de escolha válida
                    while opcaoEstats not in (1, 2, 3):
                        print('Opção inválida!')
                        opcaoEstats = verificacoes.ler_opcao('Selecione um opção válida: ')
                    match opcaoEstats:
                        case 1:
                            #estatísticas de comparecimento
                            os.system('cls')
                            funcoesVotacao.estatisticas_comparecimento()
                            input('\nPressione Enter para voltar!')
                        case 2:
                            #votos por partido
                            os.system('cls')
                            funcoesVotacao.votor_por_partido()
                            input('\nPressione Enter para voltar!')
                        case 3:
                            # o return vai fazer voltar para o menu anterior
                            pass
            #validar integridade
            case 3:
                os.system('cls')
                funcoesVotacao.validar_integridade()
                input('\nPressione Enter para voltar!')
            case 4:
                return

def modVotacao():
    opcao = 0
    while opcao != 4:
        opcao = menus.menuModVota()
        match opcao:
            #abrir sistema de votação
            case 1:
                os.system('cls')
                print('''
    ====================================
        Abrir sistema da votação
    ====================================
                ''')
                #verificando validade do título
                titulo_eleitor = str(input('Informe o título do eleitor: '))
                while verificacoes.verificarTitulo(titulo_eleitor) == False:
                    titulo_eleitor = str(input('Informe seu título de eleitor: '))
                #verificando validade do cpf
                cpf = str(input("Digite os 4 primeiros dígitos do CPF: "))
                chave_acesso = str(input('Digite a sua chave de acesso: '))

                funcoesVotacao.sistema_votacao(titulo_eleitor, cpf, chave_acesso)
                input('Precione enter para voltar à tela inicial! ')
            #auditoria
            case 2:
                modAuditoria()
            #resultado
            case 3:
                
                modResultado()
            #voltar
            case 4:
                pass