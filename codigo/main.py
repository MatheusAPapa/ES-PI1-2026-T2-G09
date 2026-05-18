import os
import menus
import navegacaoModVotacao
import funcoesEleitor
import funcoesVotacao
import verificacoes
import criptografia_descriptografia


escolha = 0
while escolha != 3:
    escolha = menus.menuInic()
    #modulo de gerenciamento
    match escolha:
        case 1:
            opcao = menus.menuModGere()
            match opcao:
                case 1:
                    os.system("cls")
                    print("====================================")
                    print("        Cadastrar eleitor")
                    print("====================================\n")

                    #receberá os dados do eleitor
                    nome_eleitor = str(input('Informe o nome do eleitor: '))

                        #verificando se o título é válido
                    titulo_eleitor = str(input('Informe o título de eleitor: '))
                    while verificacoes.verificarTitulo(titulo_eleitor) == False:
                        print('Título de eleitor inválido!')
                        titulo_eleitor = str(input('Informe o título de eleitor: '))

                        #verificando se o cpf é válido
                    cpf = str(input('Informe o CPF do eleitor: '))
                    while verificacoes.verificarCPF(cpf) == False:
                        cpf = str(input('Informe o CPF do eleitor: '))

                        #verificando possíveis respostas para se o eleitor é mesário
                    mesario = str(input('Informe se o mesário será eleitor [S/N]: '))
                    if mesario in ['s', 'S', 'sim', 'Sim']:
                        mesario = True
                    elif mesario in ['n', 'N', 'não', 'Não']:
                        mesario = False
                    else:
                        print('Opção inválida para mesário')
                        mesario = str(input('Informe se o mesário será eleitor [S/N]: '))

                    #cadastrando o novo eleitor
                    funcoesEleitor.cadastrar_novo_eleitor(nome_eleitor, titulo_eleitor, cpf, mesario)
                    funcoesVotacao.registrar_log('Novo eleitor cadastrado.')

                #editar dados do eleitor
                case 2:
                    cpf = str(input("\nDigite o CPF do eleitor: "))
                    while verificacoes.verificarCPF(cpf) == False:
                        print('CPF inválido Digite novamente. ')
                        cpf = str(input("Digite o CPF do eleitor: "))
                    funcoesEleitor.alterar_dados_eleitor(cpf)
                    funcoesVotacao.registrar_log('Foi alterado os dados de um eleitor.')

                #listagem de todos os eleitores
                case 3:
                    funcoesEleitor.listar_eleitores()
                    input('\nPrecione enter para voltar à tela inicial! ')
                
                #fazer uma busca por eleitor
                case 4:
                    os.system("cls")
                    print("=====================================")
                    print("        Buscar eleitor")
                    print("=====================================\n")
                    cpf = str(input("Digite o CPF do eleitor: "))
                    while verificacoes.verificarCPF(cpf) == False:
                       cpf = str(input('Informe o CPF do eleitor: '))
                    
                    titulo_eleitor = str(input('Informe o título do eleitor: '))
                    while verificacoes.verificarTitulo(titulo_eleitor) == False:
                        print('Título de eleitor inválido!')
                        titulo_eleitor = str(input('Informe o título de eleitor: '))
                    
                    funcoesEleitor.busca_eleitores(cpf, titulo_eleitor)
                    input('\nPrecione enter para voltar à tela inicial! ')
                
                #remover um eleitor
                case 5:
                    os.system("cls")
                    print("=====================================")
                    print("        Removendo eleitor")
                    print("=====================================\n")
                    #validação do cpf
                    cpf = str(input("Digite o CPF do eleitor: "))
                    while verificacoes.verificarCPF(cpf) == False:
                       cpf = str(input('Informe o CPF do eleitor: '))
                    
                    #validação do titulo de eleitor
                    titulo_eleitor = str(input('Informe o título do eleitor: '))
                    while verificacoes.verificarTitulo(titulo_eleitor) == False:
                        print('Título de eleitor inválido!')
                        titulo_eleitor = str(input('Informe o título de eleitor: '))

                    funcoesEleitor.deletar_eleitor(cpf, titulo_eleitor)
                    input('\nPrecione enter para voltar à tela inicial! ')
                    funcoesVotacao.registrar_log('Um eleitor foi removido do sistema.')

                #voltar
                case 6:
                    pass
    
       #modulo de votação
        case 2:
            navegacaoModVotacao.modVotacao()

        case 3:
            print('Saindo do sistema')
