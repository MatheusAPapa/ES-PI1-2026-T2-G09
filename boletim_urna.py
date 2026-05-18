def gerar_boletim_urna(votos):
    total_votos = len(votos)

    contagem = {}

    for voto in votos:
        voto = str(voto).strip()

        if voto in contagem:
            contagem[voto] += 1
        else:
            contagem[voto] = 1

    print("===== BOLETIM DE URNA =====")
    print(f"Total de votos: {total_votos}")
    print("---------------------------")

    for voto, quantidade in contagem.items():
        print(f"{voto}: {quantidade} voto(s)")

    print("===========================")


# Teste simples sem mexer na main
if __name__ == "__main__":
    votos_teste = [
        "10", "13", "10", "22",
        "branco", "nulo", "13", "10"
    ]

    gerar_boletim_urna(votos_teste)
