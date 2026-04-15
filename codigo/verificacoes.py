def verificarCPF (cpf):
    #verifica se o cpf tem 11 números
    if len(cpf) != 11:
        print('CPF não possui 11 números')
        return False
    
    #verifica se tem letra no meio do cpf
    elif cpf.isdigit() == False:
        return False
    #verifica se todos os digitos do cpf são iguais, pois assim ele passa na conta de verificação
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