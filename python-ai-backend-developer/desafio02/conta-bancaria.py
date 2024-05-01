from datetime import datetime
from variables import *

menu = '''
[1] - Depositar
[2] - Sacar
[3] - Extrato
[4] - Criar usuario
[5] - Criar conta corrente
[6] - Listar contas 
[7] - Listar usuários
[8] - Sair
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
            criar_extrato(valor, 'S', conta=conta_corrente)
            return True

    return False

def depositar(valor: float, conta_corrente, /):
    if valor > 0:
        conta_corrente['saldo'] += valor
        criar_extrato(valor, 'D',conta=conta_corrente)
        return True
    return False

def criar_extrato(valor, operacao, /, *, conta):
    hoje = datetime.now().strftime("%d/%m/%Y às %H:%M:%S")
    if operacao == 'D':
        mensagem = f"Depósito .....: \tR${valor:.2f} realizado em {hoje}."
    elif operacao == 'S':
        mensagem = f"Saque ........: \tR${valor:.2f} realizado em {hoje}."
    conta['extrato'].append(mensagem)

def exibir_extrato(*, conta_corrente, nro_conta):
    print(f"Titular ......: \t{conta_corrente['dados_correntista']['nome']}")
    print(f"Agência ......: \t{conta_corrente['agencia']}")
    print(f"Conta ........: \t{nro_conta}\n")
    for item in conta_corrente['extrato']:
        print(item, end="\n")
    return f"\nSaldo ........: \tR${conta_corrente['saldo']:.2f}"

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
                                       'quantidade_saques': LIMITES_SAQUES,
                                       'extrato': []}})
    return nro_conta

def listar_contas_correntes():
    for conta in conta_corrente:
        print(conta)

def listar_usuarios():
    for usuario in usuarios:
        print(usuario)

def filtrar_usuario():
    cpf = input('Informe o número do cpf: ')
    for index, usuario in enumerate(usuarios):
        if cpf == usuario['cpf']:
            return usuarios[index]
    return False

def obter_conta_corrente(agencia, nro_conta):
    for conta in conta_corrente:
       if nro_conta in conta:
            if conta[nro_conta]['agencia'] == agencia:
                return conta
    return False

def validar_cpf():
    cpf = input('Informe o número do cpf: ')

    for usuario in usuarios:
        if cpf == usuario['cpf']:
            print('Já existe um correntista com este número de cpf.')
            return False
    return cpf


while True:
    print(menu)
    opcao = input('Informe uma opção: ')

    if opcao in ('1','2','3'):
        agencia     = input('Informe o número da agência: ')
        nro_conta   = int(input('Informe o número da conta: '))
        conta       = obter_conta_corrente(agencia, nro_conta)

        if conta:
            if opcao == '1':
                valor   = float(input('Informe o valor do depósito: '))
                sucesso = depositar(valor, conta[nro_conta])
                if sucesso:
                    print('=== Depósito realizado com sucesso! ===')

            elif opcao == '2':
                valor   = float(input('Informe o valor do saque: '))
                sucesso = sacar( valor=valor
                               , limite=LIMITE
                               , conta_corrente=conta[nro_conta])
                if sucesso:
                    print('=== Saque realizado com sucesso! ===')

            elif opcao == '3':
                print(cab_extrato)
                print(exibir_extrato(conta_corrente=conta[nro_conta], nro_conta=nro_conta))
                print(rod_extrato)

        else:
            print('Não existe esta conta em nosso sistema.')

    elif opcao == '4':
        cpf_valido = validar_cpf()
        if cpf_valido:
            nome     = input('Informe o nome do correntista: ')
            dt_nasc  = input('Informe a data de nascimento: ')
            endereco = input('Informe o endereço no formato (logradouro, nro, bairro, cidade/sigla, estado): ')
            usuario  = criar_usuario(nome=nome, dt_nasc=dt_nasc, cpf=cpf_valido, endereco=endereco)
            print('=== Usuário criado com sucesso! ===')

    elif opcao == '5':
        usuario_valido = filtrar_usuario()
        if usuario_valido:
            seq_nro_conta = criar_conta_corrente(usuario=usuario_valido, seq_nro_conta=seq_nro_conta)
            print('=== Conta criada com sucesso! ===')
        else:
            print('Não existe um usuário com este número de cpf.')


    elif opcao == '6':
        listar_contas_correntes()

    elif opcao == '7':
        listar_usuarios()

    elif opcao == '8':
        break

    else:
        print('Opção inválida!')




