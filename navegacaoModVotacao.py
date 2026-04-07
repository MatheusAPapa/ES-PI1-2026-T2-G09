import menus

def modAuditoria():
    opcaoAudVota = menus.menuAudVota()
    match opcaoAudVota:
        #logs 
        case 1:
            print('logs')
        #protocolos
        case 2:
            print('protocolos de votação')
        #voltar
        case 3: 
            modVotacao()

def modResultado():
    opcaoResulVota = menus.menuResulVota()
    match opcaoResulVota:
        #boletim de urna
        case 1:
            print('Boletim de urna')
        #estatísticas por candidato
        case 2:
            print('Estatisticas')
        #votos por partido
        case 3:
            print('votos por partido')
        #validação do resultado
        case 4:
            print('validação')
        case 5:
            modVotacao()

def modVotacao():
    opcao = menus.menuModVota()
    match opcao:
        #abrir sistema de votação
        case 1:
            print('abrir sistema')
        #auditoria
        case 2:
            modAuditoria()
        #resultado
        case 3:
            modResultado()
        #voltar
        case 4:
            pass
