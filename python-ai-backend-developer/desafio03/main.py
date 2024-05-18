from pessoafisica import PessoaFisica
from contacorrente import ContaCorrente
from cliente import Cliente
from conta import Conta
from deposito import Deposito
from saque import Saque
from transacao import Transacao
from historico import Historico

import textwrap

menu = '''
[1] - Depositar
[2] - Sacar
[3] - Extrato
[4] - Criar cliente
[5] - Criar conta corrente
[6] - Listar contas 
[7] - Listar clientes
[8] - Sair
'''

# cliente
def criar_cliente(clientes):
    cpf = input("Informe o CPF: ")
    cliente = recuperar_cliente(clientes, cpf)

    if cliente:
        print('Cliente já cadastrado')
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")
    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
    clientes.append(cliente)
    print("\n=== Cliente criado com sucesso! ===")

def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente):
    return cliente.contas[0] if cliente.contas else None

def recuperar_cliente(clientes, cpf):
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        return None
    return cliente

def listar_clientes(clientes):
    for cliente in clientes:
        print("=" * 100)
        print(textwrap.dedent(str(cliente)))
# conta
def criar_conta(numero_conta, clientes, contas):
    cpf = input('Digite o CPF do cliente: ')
    cliente = recuperar_cliente(clientes, cpf)
    if not cliente:
        print('Cliente não encontrado')
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)
    print("\n=== Conta criada com sucesso! ===")

def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))

def depositar(clientes):
    cpf = input('Digite o CPF do cliente: ')
    cliente = recuperar_cliente(clientes, cpf)
    if cliente:
        valor = float(input('Digite o valor a ser depositado: '))
        transacao = Deposito(valor)
        conta = recuperar_conta_cliente(cliente)
        if not conta:
            print('Conta não encontrada')
            return

        cliente.realizar_transacao(conta, transacao)

def sacar(clientes):
    cpf = input('Digite o CPF do cliente: ')
    cliente = recuperar_cliente(clientes, cpf)
    if cliente:
        valor = float(input('Digite o valor do saque: '))
        transacao = Saque(valor)
        conta = recuperar_conta_cliente(cliente)
        if not conta:
            print('Conta não encontrada')
            return

        cliente.realizar_transacao(conta, transacao)

def exibir_extrato(clientes):
    cpf = input('Digite o CPF do cliente: ')
    cliente = recuperar_cliente(clientes, cpf)

    if not cliente:
        print('Cliente não encontrado')
        return

    if cliente:
        conta = recuperar_conta_cliente(cliente)
        if not conta:
            print('Conta não encontrada')
            return

        print("\n================ EXTRATO ================")
        transacoes = conta.historico.transacoes

        extrato = ""
        if not transacoes:
            extrato = "Não foram realizadas movimentações."
        else:
            for transacao in transacoes:
                extrato += f"{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}\n"

        print(extrato)
        print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
        print("==========================================")

def atm():
    clientes = []
    contas = []

    while True:
        print(menu)
        opcao = input('Digite a opção desejada: ')
        if opcao == '1':
            depositar(clientes)
        elif opcao == '2':
            sacar(clientes)
        elif opcao == '3':
            exibir_extrato(clientes)
        elif opcao == '4':
            criar_cliente(clientes)
        elif opcao == '5':
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)
        elif opcao == '6':
            listar_contas(contas)
        elif opcao == '7':
            listar_clientes(clientes)
        elif opcao == '8':
            break
        else:
            print('Opção inválida')


if __name__ == '__main__':
    atm()