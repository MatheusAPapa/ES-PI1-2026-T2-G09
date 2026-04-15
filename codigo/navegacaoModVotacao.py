import menus as menus

def modAuditoria():
    opcaoAudVota = menus.menuAudVota()
    match opcaoAudVota:
        #logs 
        case 1:
            print('logs')
            exit()
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
            print('abrir sistema')
            exit()
        #auditoria
        case 2:
            modAuditoria()
        #resultado
        case 3:
            modResultado()
        #voltar
        case 4:
            pass
