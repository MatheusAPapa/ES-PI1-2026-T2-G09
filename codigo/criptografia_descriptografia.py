ALFABETO = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
TAMANHO = len(ALFABETO) 
# Matriz chave
CHAVE = [[3, 2],
         [5, 7]]
# Funçao que criptografa o texto desejado, usando:
def criptografar(texto):

    # Converte tudo para maiúsculo, filtrar apenas caracteres e juntar numa string
    texto_maiusculo = texto.upper()
    caracteres_filtrados = []
    for c in texto_maiusculo:
        if c in ALFABETO:
            caracteres_filtrados.append(c)
    texto = ''.join(caracteres_filtrados)

    # Se o texto tiver número impar de caracteres será adicionado uma letra a mais
    if len(texto) % 2 != 0:
        texto += 'A'
    resultado = ""

    # Percorre em bloco de 2 em 2
    for i in range(0, len(texto), 2):
        # Converte cada caracter para seu indice no alfabeto
        n1 = ALFABETO.index(texto[i])
        n2 = ALFABETO.index(texto[i+1])
        # Multiplicação do vetor pela matriz chave
        c1 = (CHAVE[0][0] * n1 + CHAVE[0][1] * n2) % TAMANHO
        c2 = (CHAVE[1][0] * n1 + CHAVE[1][1] * n2) % TAMANHO
        # Converte os indices de volta para seus caracteres
        resultado += ALFABETO[c1] + ALFABETO[c2]
    
    return resultado

# Calcula o inverso mutiplicativo de 'a' mod 'm'
def inverso_modular(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None
# Calcula a matriz inversa
def matriz_inversa(chave):
    # Calcula o determinante da matriz
    det = (chave[0][0] * chave[1][1] - chave[0][1] * chave[1][0]) % TAMANHO
    inv_det = inverso_modular(det, TAMANHO)

    # Se o determinante não tiver inverso modular, a chave não pode ser usada
    if inv_det is None:
        raise ValueError("A chave não é invertível para este alfabeto.")
    
    # Fórmula da inversa de uma matriz 2x2 no espaço modular:
    # M^~-1 = inv_det * [[ d, -b],
    #                   [-c,  a]]
    return [
        [(chave[1][1] * inv_det) % TAMANHO,  (-chave[0][1] * inv_det) % TAMANHO],
        [(-chave[1][0] * inv_det) % TAMANHO, (chave[0][0] * inv_det) % TAMANHO]
    ]
# Essa função descriptografa o texto criptografado, usando:
def descriptografar(texto_cifrado):
    # Obtem a matriz inversa da chave
    inv = matriz_inversa(CHAVE)
    resultado = ""
    # Converte cada caracter para seu indice no alfabeto, em bloco de 2
    for i in range(0, len(texto_cifrado), 2):
        n1 = ALFABETO.index(texto_cifrado[i])
        n2 = ALFABETO.index(texto_cifrado[i+1])
        # Multiplicação do vetor pela matriz inversa da chave
        c1 = (inv[0][0] * n1 + inv[0][1] * n2) % TAMANHO
        c2 = (inv[1][0] * n1 + inv[1][1] * n2) % TAMANHO
        # Converte os indices de volta para seus caracteres originais
        resultado += ALFABETO[c1] + ALFABETO[c2]

    return resultado
