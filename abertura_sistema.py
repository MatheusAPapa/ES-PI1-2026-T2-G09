from datetime import datetime

sistema_aberto = False
horario_abertura = None


def abrir_sistema():
    global sistema_aberto, horario_abertura

    if sistema_aberto:
        return "O sistema de votação já está aberto."

    sistema_aberto = True
    horario_abertura = datetime.now()

    return f"Sistema de votação aberto em {horario_abertura.strftime('%d/%m/%Y %H:%M:%S')}"


def sistema_esta_aberto():
    return sistema_aberto


def get_horario_abertura():
    if horario_abertura is None:
        return "O sistema ainda não foi aberto."
    return horario_abertura.strftime('%d/%m/%Y %H:%M:%S')
