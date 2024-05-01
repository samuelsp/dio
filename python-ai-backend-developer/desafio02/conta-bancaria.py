from datetime import datetime
from variables import *

menu = '''
[1] - Depositar
[2] - Sacar
[3] - Extrato
[4] - Criar conta corrente
[5] - Listar conta corrente
[6] - Sair
'''

def sacar(*, valor, limite, conta_corrente):
    saldo_permitido   = conta_corrente['saldo'] >= valor
    saques_permitidos = conta_corrente['quantidade_saques'] > 0
    limite_permitido  = limite >= valor

    if not saldo_permitido:
        print("Operação falhou! Você não possui saldo suficiente.")

    elif not limite_permitido:
        print("Operação falhou! Você excedeu o valor limite por transação de saque diário.")

    elif not saques_permitidos:
        print("Operação falhou! Você excedeu a quantidade de saques diários.")

    else:
        if valor > 0:
            conta_corrente['saldo'] -= valor
            conta_corrente['quantidade_saques'] -= 1
            criar_extrato(valor, 'S', conta_corrente)

    return conta_corrente['saldo']

def depositar(valor: float, /, conta_corrente):
    if valor > 0:
        conta_corrente['saldo'] += valor
        criar_extrato(valor, 'D', conta_corrente)
    return conta_corrente['saldo']

def criar_extrato(valor, operacao, conta_corrente):
    hoje = datetime.now().strftime("%d/%m/%Y às %H:%M:%S")
    if operacao == 'D':
        mensagem = f"Depósito: R${valor:.2f} realizado em {hoje}."
    elif operacao == 'S':
        mensagem = f"Saque: R${valor:.2f} realizado em {hoje}."
    conta_corrente['extrato'].append(mensagem)

def obter_extrato(*, conta_corrente):
    for item in conta_corrente['extrato']:
        print(item, end="\n")
    return f"Saldo atual: R${conta_corrente['saldo']:.2f}"

def criar_usuario(**dados_usuario):
    nome      = dados_usuario['nome']
    dt_nasc   = dados_usuario['dt_nasc']
    cpf       = dados_usuario['cpf']
    endereco  = dados_usuario['endereco']

    usuario = {'nome': nome,
               'nascimento': dt_nasc,
               'cpf': cpf,
               'endereco': endereco}
    usuarios.append(usuario)

    return usuario

def criar_conta_corrente(**dados_conta_corrente):
    nro_conta = dados_conta_corrente['seq_nro_conta'] + 1
    usuario   = dados_conta_corrente['usuario']
    agencia   = f"{1:04}"
    conta_corrente.append({nro_conta: {'agencia': agencia,
                                       'dados_correntista': usuario,
                                       'saldo': 0.0,
                                       'quantidade_saques': 3,
                                       'extrato': extrato}})
    return nro_conta

def listar_contas_correntes():
    for conta in conta_corrente:
        print(conta)

def obter_conta_corrente(agencia, nro_conta):
    for conta in conta_corrente:
       if nro_conta in conta:
            if conta[nro_conta]['agencia'] == agencia:
                return conta
    return None

def validar_cpf():
    cpf = input('Informe o número do cpf: ')

    for usuario in usuarios:
        if cpf in usuario['cpf']:
            print('Já existe um correntista com este número de cpf.')
            return validar_cpf()
    return cpf

while True:
    print(menu)

    opcao = input('Informe uma opção: ')

    if opcao in ('1','2','3'):
        agencia     = input('Informe o número da agência: ')
        nro_conta   = int(input('Informe o número da conta: '))
        conta       = obter_conta_corrente(agencia, nro_conta)

        if conta is not None:
            if opcao == '1':
                valor = float(input('Informe o valor do depósito: '))
                saldo = depositar(valor, conta[nro_conta])

            elif opcao == '2':
                valor = float(input('Informe o valor do saque: '))
                saldo = sacar( valor=valor
                             , limite=limite
                             , conta_corrente=conta[nro_conta])

            elif opcao == '3':
                print(cab_extrato)
                print(obter_extrato(conta_corrente=conta[nro_conta]))
                print(rod_extrato)

        else:
            print('Não existe esta conta em nosso sistema.')

    elif opcao == '4':
        nome            = input('Informe o nome do correntista: ')
        dt_nasc         = input('Informe a data de nascimento: ')
        cpf             = validar_cpf()
        endereco        = input('Informe o endereço no formato (logradouro, nro, bairro, cidade/sigla, estado): ')
        usuario         = criar_usuario(nome=nome, dt_nasc=dt_nasc, cpf=cpf, endereco=endereco)
        seq_nro_conta   = criar_conta_corrente(usuario=usuario, seq_nro_conta=seq_nro_conta)

    elif opcao == '5':
        listar_contas_correntes()

    elif opcao == '6':
        break

    else:
        print('Opção inválida!')




