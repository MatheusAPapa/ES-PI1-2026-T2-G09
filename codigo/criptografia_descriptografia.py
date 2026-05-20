ALFABETO = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
TAMANHO = len(ALFABETO) 

CHAVE = [[3, 2],
         [5, 7]]

def criptografar(texto):
    texto = ''.join(c for c in texto.upper() if c in ALFABETO)

    if len(texto) % 2 != 0:
        texto += 'A'
    
    resultado = ""
    for i in range(0, len(texto), 2):
        n1 = ALFABETO.index(texto[i])
        n2 = ALFABETO.index(texto[i+1])
        
        c1 = (CHAVE[0][0] * n1 + CHAVE[0][1] * n2) % TAMANHO
        c2 = (CHAVE[1][0] * n1 + CHAVE[1][1] * n2) % TAMANHO
        
        resultado += ALFABETO[c1] + ALFABETO[c2]
    
    return resultado

def inverso_modular(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def matriz_inversa(chave):
    det = (chave[0][0] * chave[1][1] - chave[0][1] * chave[1][0]) % TAMANHO
    inv_det = inverso_modular(det, TAMANHO)
    
    if inv_det is None:
        raise ValueError("A chave não é invertível para este alfabeto.")
    
    return [
        [(chave[1][1] * inv_det) % TAMANHO,  (-chave[0][1] * inv_det) % TAMANHO],
        [(-chave[1][0] * inv_det) % TAMANHO, (chave[0][0] * inv_det) % TAMANHO]
    ]

def descriptografar(texto_cifrado):
    inv = matriz_inversa(CHAVE)
    resultado = ""
    
    for i in range(0, len(texto_cifrado), 2):
        n1 = ALFABETO.index(texto_cifrado[i])
        n2 = ALFABETO.index(texto_cifrado[i+1])
        
        c1 = (inv[0][0] * n1 + inv[0][1] * n2) % TAMANHO
        c2 = (inv[1][0] * n1 + inv[1][1] * n2) % TAMANHO
        
        resultado += ALFABETO[c1] + ALFABETO[c2]

    return resultado
print(descriptografar('FNCIFN8IEPVL'))
'''Ana
18081840095
ANC9611
'''

'''João
52172466859
FEX9078
'''
