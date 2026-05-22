def validar_voto(voto, candidatos_validos):
    """
    Regras:
    - Enter vazio = inválido
    - 'branco' = voto em branco
    - Número inexistente = voto nulo
    - Número existente = voto válido
    """

    if voto is None:
        return "invalido"

    voto = str(voto).strip()

    if voto == "":
        return "invalido"

    if voto.lower() == "branco":
        return "branco"

    # Verifica se o número existe
    if voto in candidatos_validos:
        return "valido"

    # Qualquer número inexistente vira nulo
    return "nulo"


def registrar_voto(urna, tipo_voto, voto=None):
    """
    Registra o voto na urna.
    """

    if tipo_voto == "valido":
        urna[voto] += 1

    elif tipo_voto == "branco":
        urna["branco"] += 1

    elif tipo_voto == "nulo":
        urna["nulo"] += 1


def mostrar_resultado(urna, candidatos):
    """
    Mostra o resultado final.
    """

    print("\n===== RESULTADO FINAL =====")

    total_votos = sum(urna.values())

    for numero, nome in candidatos.items():

        votos = urna[numero]

        porcentagem = (votos / total_votos) * 100

        print(
            f"{nome} ({numero}): "
            f"{votos} voto(s) "
            f"({porcentagem:.1f}%)"
        )

    print(f"\nBrancos: {urna['branco']}")
    print(f"Nulos: {urna['nulo']}")
    print(f"Total de votos: {total_votos}")


# =========================
# SISTEMA PRINCIPAL
# =========================

candidatos = {
    "10": "Felipe",
    "20": "Joao",
    "30": "Maria"
}

urna = {
    "10": 0,
    "20": 0,
    "30": 0,
    "branco": 0,
    "nulo": 0
}

print("===== SISTEMA DE VOTAÇÃO =====")
print("Digite 'encerrar' para finalizar.\n")

print("Candidatos disponíveis:")

for numero, nome in candidatos.items():
    print(f"{numero} - {nome}")

while True:

    voto = input("\nDigite seu voto: ")

    if voto.lower() == "encerrar":
        break

    resultado = validar_voto(voto, candidatos)

    if resultado == "invalido":

        print("Voto inválido!")

    else:

        registrar_voto(urna, resultado, voto)

        if resultado == "valido":
            print("Voto registrado com sucesso!")

        elif resultado == "branco":
            print("Voto em branco registrado!")

        elif resultado == "nulo":
            print("Voto nulo registrado!")

mostrar_resultado(urna, candidatos)
