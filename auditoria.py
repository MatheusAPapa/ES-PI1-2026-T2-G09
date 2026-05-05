from datetime import datetime

registros_auditoria = []

def registrar_evento(evento):
    horario = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    registros_auditoria.append(f"[{horario}] {evento}")

def mostrar_auditoria():
    print("===== RELATÓRIO DE AUDITORIA =====")
    
    if len(registros_auditoria) == 0:
        print("Nenhum evento registrado.")
    else:
        for item in registros_auditoria:
            print(item)

# exemplos de eventos simulados
registrar_evento("Sistema iniciado")
registrar_evento("Votação aberta")
registrar_evento("Eleitor realizou voto")
registrar_evento("Administrador encerrou votação")
