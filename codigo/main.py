import mysql.connector
import os
import menus
import navegacaoModVotacao
import funcoesEleitor
import verificacoes

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
                    titulo_eleitor = str(input('Informe o título de eleitor: '))
                    cpf = str(input('Informe o CPF do eleitor: '))
                    while verificacoes.verificarCPF(cpf) == False:
                            cpf = str(input('Informe o CPF do eleitor: '))
                    mesario = str(input('Informe se o mesário será eleitor [S/N]: '))
                    if mesario in ['s', 'S', 'sim', 'Sim']:
                        mesario = True
                    elif mesario in ['n', 'N', 'não', 'Não']:
                        mesario = False
                    else:
                        print('Opção inválida para mesário')
                        mesario = str(input('Informe se o mesário será eleitor [S/N]: '))
                    #cadastro de novo eleitor
                    funcoesEleitor.cadastrar_novo_eleitor(nome_eleitor, titulo_eleitor, cpf, mesario)
                #editar dados do eleitor
                case 2:
                    print('editar dados do eleitor')
                    break
                #listagem de todos os eleitores
                case 3:
                    print('listagem de todos os eleitores')
                    break
                #fazer uma busca por eleitor
                case 4:
                    print('fazer uma busca por um eleitor')
                    break
                #remover um eleitor
                case 5:
                    print('remover um eleitor')
                    break
                #voltar
                case 6:
                    pass
    
        #modulo de votação
        case 2:
            navegacaoModVotacao.modVotacao()
        case 3:
            print('Saindo do sistema')
