import mysql.connector
import navegacaoModVotacao
import menus
from cadastroEleitor import cadastrar_novo_eleitor

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
                    cadastrar_novo_eleitor()
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
