import mysql.connector
import navegacaoModVotacao
import menus

escolha = 0
while escolha != 3:
    escolha = menus.menuInic()
    #modulo de gerenciamento
    match escolha:
        case 1:
            opcao = menus.menuModGere()
            match opcao:
                #cadastro de novo eleitor
                case 1:
                    print('cadastrar de novo eleitor')
                #editar dados do eleitor
                case 2:
                    print('editar dados do eleitor')
                #listagem de todos os eleitores
                case 3:
                    print('listagem de todos os eleitores')
                #fazer uma busca por eleitor
                case 4:
                    print('fazer uma busca por um eleitor')
                #remover um eleitor
                case 5:
                    print('remover um eleitor')
                #voltar
                case 6:
                    pass
    
        #modulo de votação
        case 2:
            opcao = navegacaoModVotacao.modVotacao()
        case 3:
            print('Saindo do sistema')
