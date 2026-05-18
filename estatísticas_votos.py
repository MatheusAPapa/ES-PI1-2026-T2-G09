from collections import Counter


def gerar_estatisticas_votos(votos):
    total_votos = len(votos)

    if total_votos == 0:
        return {
            "total_votos": 0,
            "mais_votado": None,
            "menos_votado": None,
            "estatisticas": {}
        }

    contagem = Counter(votos)

    estatisticas = {}

    for candidato, quantidade in contagem.items():
        porcentagem = (quantidade / total_votos) * 100

        estatisticas[candidato] = {
            "quantidade": quantidade,
            "porcentagem": round(porcentagem, 2)
        }

    mais_votado = contagem.most_common(1)[0]
    menos_votado = min(contagem.items(), key=lambda item: item[1])

    return {
        "total_votos": total_votos,
        "mais_votado": {
            "candidato": mais_votado[0],
            "votos": mais_votado[1]
        },
        "menos_votado": {
            "candidato": menos_votado[0],
            "votos": menos_votado[1]
        },
        "estatisticas": estatisticas
    }


def exibir_estatisticas_votos(votos):
    resultado = gerar_estatisticas_votos(votos)

    print("\n===== ESTATÍSTICAS DE VOTOS =====")
    print(f"Total de votos: {resultado['total_votos']}")

    if resultado["total_votos"] == 0:
        print("Nenhum voto registrado.")
        return

    print("\nVotos por candidato/partido:")

    for nome, dados in resultado["estatisticas"].items():
        print(f"{nome}: {dados['quantidade']} votos ({dados['porcentagem']}%)")

    print("\nMais votado:")
    print(f"{resultado['mais_votado']['candidato']} - {resultado['mais_votado']['votos']} votos")

    print("\nMenos votado:")
    print(f"{resultado['menos_votado']['candidato']} - {resultado['menos_votado']['votos']} votos")
