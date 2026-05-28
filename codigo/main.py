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
            opcao = 0
            while opcao != 6:
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
                            titulo_eleitor = str(input('Informe o título de eleitor: '))

                        #verificando se o cpf é válido
                        cpf = str(input('Informe o CPF do eleitor: '))
                        while verificacoes.verificarCPF(cpf) == False:
                            cpf = str(input('Informe o CPF do eleitor: '))

                        #verificando possíveis respostas para se o eleitor é mesário
                        mesario = str(input('Informe se o mesário será eleitor [S/N]: '))
                        while mesario.lower() not in ['s', 'sim', 'n', 'nao', 'não']:
                            print('Opção inválida!')
                            mesario = str(input('Informe se o mesário será eleitor [S/N]: '))
                        if mesario in ['s', 'sim']:
                            mesario = True
                        else:
                            mesario = False                             

                        #cadastrando o novo eleitor
                        funcoesEleitor.cadastrar_novo_eleitor(nome_eleitor, titulo_eleitor, cpf, mesario)

                    #editar dados do eleitor
                    case 2:
                        cpf = str(input("\nDigite o CPF do eleitor: "))
                        while verificacoes.verificarCPF(cpf) == False:
                            cpf = str(input("Digite o CPF do eleitor: "))
                        funcoesEleitor.alterar_dados_eleitor(cpf)

                    #listagem de todos os eleitores
                    case 3:
                        os.system('cls')
                        funcoesEleitor.listar_eleitores()
                        input('\nPrecione enter para voltar! ')
                    
                    #fazer uma busca por eleitor
                    case 4:
                        os.system("cls")
                        print("=====================================")
                        print("        Buscar eleitor")
                        print("=====================================\n")
                        print('1 - Buscar por cpf')
                        print('2 - Buscar por título de eleitor')
                        busca = verificacoes.ler_opcao('Digite sua escolha: ')

                        funcoesEleitor.busca_eleitores(busca)
                        input('\nPrecione enter para voltar! ')
                    
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
                        input('\nPrecione enter para voltar! ')
                        funcoesVotacao.registrar_log('Um eleitor foi removido do sistema.')

                    #voltar
                    case 6:
                        pass
    
       #modulo de votação
        case 2:
            navegacaoModVotacao.modVotacao()

        case 3:
            print('Saindo do sistema')