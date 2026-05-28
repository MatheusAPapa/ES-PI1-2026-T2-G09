import menus 
import funcoesVotacao
import verificacoes
import os
# Funcionamento do modulo de auditoria
def modAuditoria():
    opcaoAudVota = menus.menuAudVota()
    match opcaoAudVota:
        # Logs 
        case 1:
            os.system('cls')
            funcoesVotacao.exibir_logs()
            input('\nPrecione enter para voltar à tela inicial! ')
        # Protocolos
        case 2:
            os.system('cls')
            funcoesVotacao.exibir_protocolos()
            input('\nPrecione enter para voltar à tela inicial! ')    
        # Voltar
        case 3: 
            return
# Funcionamento do modulo de resultado
def modResultado():
    opcaoResulVota = 0
    while opcaoResulVota != 4:
        opcaoResulVota = menus.menuResulVota()
        opcaoEstats = 0
        match opcaoResulVota:
            # Boletim de urna
            case 1:
                funcoesVotacao.boletim_urna()
                input('\nPressione Enter para voltar!')
            # Estatísticas
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
                    opcaoEstats = int(input('Selecione uma das opções acima: '))
            
                    # Verificação de escolha válida
                    while opcaoEstats not in (1, 2, 3):
                        print('Opção inválida!')
                        opcaoEstats = int(input('Selecione um opção válida: '))
                    match opcaoEstats:
                        case 1:
                            # Estatísticas de comparecimento
                            os.system('cls')
                            funcoesVotacao.estatisticas_comparecimento()
                            input('\nPressione Enter para voltar!')
                        case 2:
                            # Votos por partido
                            os.system('cls')
                            funcoesVotacao.votor_por_partido()
                            input('\nPressione Enter para voltar!')
                        case 3:
                            # O return vai fazer voltar para o menu anterior
                            pass
            # Validar integridade
            case 3:
                os.system('cls')
                funcoesVotacao.validar_integridade()
                input('\nPressione Enter para voltar!')
            case 4:
                return
# Funcionamento do modulo de votação
def modVotacao():
    opcao = 0
    while opcao != 4:
        opcao = menus.menuModVota()
        match opcao:
            # Abrir sistema de votação
            case 1:
                os.system('cls')
                print('''
    ====================================
        Abrir sistema da votação
    ====================================
                ''')
                # Verificando validade do título
                titulo_eleitor = str(input('Informe o título do eleitor: '))
                while verificacoes.verificarTitulo(titulo_eleitor) == False:
                    print('Título de eleitor inválido!')
                    titulo_eleitor = str(input('Informe seu título de eleitor: '))
                # Verificando validade do cpf
                cpf = str(input("Digite os 4 primeiros dígitos do CPF: "))
                chave_acesso = str(input('Digite a sua chave de acesso: '))

                funcoesVotacao.sistema_votacao(titulo_eleitor, cpf, chave_acesso)
                input('Precione enter para voltar à tela inicial! ')
            # Auditoria
            case 2:
                modAuditoria()
            # Resultado
            case 3:
                modResultado()
            # Voltar
            case 4:
                pass