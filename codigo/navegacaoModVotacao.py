import menus 
import funcoesVotacao
import verificacoes

def modAuditoria():
    opcaoAudVota = menus.menuAudVota()
    match opcaoAudVota:
        #logs 
        case 1:
            funcoesVotacao.exibir_logs()
            input('\nPrecione enter para voltar à tela inicial! ')
        #protocolos
        case 2:
            print('protocolos de votação')
            exit()
        #voltar
        case 3: 
            modVotacao()

def modResultado():
    opcaoResulVota = menus.menuResulVota()
    match opcaoResulVota:
        #boletim de urna
        case 1:
            print('Boletim de urna')
            exit()
        #estatísticas por candidato
        case 2:
            print('Estatisticas')
            exit()
        #votos por partido
        case 3:
            print('votos por partido')
            exit()
        #validação do resultado
        case 4:
            print('validação')
            exit()
        case 5:
            modVotacao()

def modVotacao():
    opcao = menus.menuModVota()
    match opcao:
        #abrir sistema de votação
        case 1:
            print('''
    ====================================
         Abrir sistema da votação
    ====================================
            ''')
            #verificando validade do título
            titulo_eleitor = str(input('Informe o título do eleitor: '))
            while verificacoes.verificarTitulo(titulo_eleitor) == False:
                print('Título de eleitor inválido!')
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
