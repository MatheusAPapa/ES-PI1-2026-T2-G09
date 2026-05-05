from datetime import datetime

def registrar_log(mensagem):
    
    
    data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    try:
        arquivo = open("auditoria_projeto.txt", "a", encoding="utf-8")
        arquivo.write(f"[{data_hora}] {mensagem}\n")
        arquivo.close()
    except:
        print("não foi possível salvar o log")
