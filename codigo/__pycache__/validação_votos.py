def validar_voto(voto, candidatos_validos):
    """
    Função responsável por validar os votos do sistema.
    Ela verifica se o voto é branco, nulo ou se pertence
    à lista de candidatos válidos.
    """

    if voto is None:
        return False

    voto = str(voto).strip()

    if voto == "":
        return False

    if voto.lower() == "branco":
        return True

    if voto.lower() == "nulo":
        return True

    if voto in candidatos_validos:
        return True

    return False


# Testes simples da validação
if __name__ == "__main__":
    candidatos_validos = ["10", "13", "22", "45"]

    votos_teste = ["10", "13", "22", "45", "branco", "nulo", "", "99", None]

    for voto in votos_teste:
        if validar_voto(voto, candidatos_validos):
            print(f"Voto '{voto}' é válido")
        else:
            print(f"Voto '{voto}' é inválido")
