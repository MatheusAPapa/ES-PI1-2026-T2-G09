def verificarCPF (cpf):
    #verifica se o cpf tem 11 números
    if len(cpf) != 11:
        print('CPF não possui 11 números')
        return False
    
    #verifica se tem letra no meio do cpf
    elif cpf.isdigit() == False:
        return False
    
    #verifica se todos os digitos do cpf são iguais, pois assim ele passa na conta que verifica o CPF
    elif cpf == cpf[0] * 11:
        print('CPF inválidado')
        return False
    
    #verificar se o primeiro digito verificador está correto
    soma1 = 0
    contador1 = 10
    for i in range(9):
        soma1 += int(cpf[i]) * contador1
        contador1 -= 1
    digito1 = (soma1 % 11) % 10
    if digito1 >= 2:
        digito1 = 11 - digito1
    else:
        digito1 = 0
    
    if digito1 != int(cpf[9]):
        print('CPF inválidado')
        return False
    
    #verificar se o segundo digito verificador está correto
    soma2 = 0
    contador2 = 11
    for i in range(10):
        soma2 += int(cpf[i]) * contador2
        contador2 -= 1
    digito2 = (soma2 % 11) % 10
    if digito2 >= 2:
        digito2 = 11 - digito2
    else:
        digito2 = 0

    if digito2 != int(cpf[10]):
        print('CPF inválidado')
        return False
    else:
        return True

def verificarTitulo (titulo):
    titulo = str(titulo)
    #remover os espaços em branco, caso tenha
    titulo = titulo.strip()
    #verificar se tem 12 digitos 
    if len(titulo) != 12:
        return False
    
    #separando o titulo de eleitor em partes
    numeros = titulo[:8]
    uf = titulo[8: 10]
    dv_informado = titulo[10:]

    #descobrindo o 1º dígito verificador
    soma1 = 0
    multiplicador = 2
    for i in numeros:
        soma1 += int(i) * multiplicador
        multiplicador += 1
    
    resto1 = soma1 % 11

    if resto1 == 10:
        dv1 = 0
    #verificando se é de sp ou minas e se o resto da divisão é igual a 0
    elif uf == '01' or uf == '02':
        if resto1 == 0:
            dv1 = 1
        else:
            dv1 = resto1
    else:
        dv1 = resto1
    

    #descobrindo o 2º dígito verificador
    soma2 = int(uf[0]) * 7 + int(uf[1]) * 8 + dv1 * 9
    resto2 = soma2 % 11
    if resto2 == 10:
        dv2 = 0
    #verificando se é de sp ou minas e se o resto da divisão é igual a 0
    elif uf == '01' or uf == '02':
        if resto2 == 0:
            dv2 = 1
        else:
            dv2 = resto2
    else:
        dv2 = resto2

    dv_verificado = str(dv1) + str(dv2)
    
    #verificação final
    if dv_informado == dv_verificado:
        return True
    else:
        return False
