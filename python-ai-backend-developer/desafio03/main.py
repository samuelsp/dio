import textwrap
from datetime import datetime

from pytz import timezone

from clientes_iterator import ClientesIterator
from contacorrente import ContaCorrente
from contas_iterador import ContasIterador
from deposito import Deposito
from pessoafisica import PessoaFisica
from saque import Saque

menu = """
[1] - Depositar
[2] - Sacar
[3] - Extrato
[4] - Criar cliente
[5] - Criar conta corrente
[6] - Listar contas 
[7] - Listar clientes
[8] - Sair
"""


def log_transacao(func):
    def wrapper(*args, **kwargs):
        data_hora = datetime.now(timezone("America/Sao_Paulo")).strftime(
            "%d/%m/%Y %H:%M:%S"
        )
        resultado = func(*args, **kwargs)
        with open("log.txt", "a") as arquivo:
            arquivo.write(
                f"[{data_hora}]: Função '{func.__name__}' executada com argumentos {args} e {kwargs}."
                f"Retornou {resultado}\n"
            )
        return resultado

    return wrapper


# cliente
@log_transacao
def criar_cliente(clientes):
    cpf = input("Informe o CPF: ")
    cliente = recuperar_cliente(clientes, cpf)

    if cliente:
        print("Cliente já cadastrado")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input(
        "Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): "
    )
    cliente = PessoaFisica(
        nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco
    )
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
    for cliente in ClientesIterator(clientes):
        print("=" * 100)
        print(textwrap.dedent(str(cliente)))


# conta
@log_transacao
def criar_conta(numero_conta, clientes, contas):
    cpf = input("Digite o CPF do cliente: ")
    cliente = recuperar_cliente(clientes, cpf)
    if not cliente:
        print("Cliente não encontrado")
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)
    print("\n=== Conta criada com sucesso! ===")


def filtrar_conta(nro_conta, agencia, contas):
    contas_filtradas = [
        conta
        for conta in contas
        if conta.numero == nro_conta and conta.agencia == agencia
    ]
    return contas_filtradas[0] if contas_filtradas else None


def listar_contas(contas):
    for conta in ContasIterador(contas):
        print("=" * 100)
        print(textwrap.dedent(str(conta)))


def recuperar_conta(nro_conta, agencia, contas):
    conta = filtrar_conta(nro_conta, agencia, contas)
    if not conta:
        return None
    return conta


@log_transacao
def depositar(contas):
    nro_conta = int(input("Digite o número da conta: "))
    agencia = input("Digite a agência: ")
    conta = recuperar_conta(nro_conta, agencia, contas)

    if conta:
        valor = float(input("Digite o valor a ser depositado: "))
        transacao = Deposito(valor)
        conta.cliente.realizar_transacao(conta, transacao)

    if not conta:
        print("Conta não encontrada")
        return


@log_transacao
def sacar(contas):
    nro_conta = int(input("Digite o número da conta: "))
    agencia = input("Digite a agência: ")
    conta = recuperar_conta(nro_conta, agencia, contas)

    if conta:
        valor = float(input("Digite o valor do saque: "))
        transacao = Saque(valor)
        conta.cliente.realizar_transacao(conta, transacao)

    if not conta:
        print("Conta não encontrada")
        return


@log_transacao
def exibir_extrato(contas):
    nro_conta = int(input("Digite o número da conta: "))
    agencia = input("Digite a agência: ")
    conta = recuperar_conta(nro_conta, agencia, contas)
    titular = conta.cliente.nome

    if not conta:
        print("Conta não encontrado")
        return

    if conta:
        print("\n================ EXTRATO ================")
        print("Titular:", titular)

        extrato = ""
        tem_transacao = False

        for transacao in conta.historico.gerar_relatorio():
            tem_transacao = True
            extrato += (
                f"\n{transacao['tipo']}\n"
                f"Realizado em {transacao['data']}"
                f"\nValor: R$ {transacao['valor']:.2f}\n"
            )

        if not tem_transacao:
            extrato = "Não foram realizadas movimentações."

        print(extrato)
        print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
        print("==========================================")


def atm():
    clientes = []
    contas = []

    while True:
        print(menu)
        opcao = input("Digite a opção desejada: ")
        if opcao == "1":
            depositar(contas)
        elif opcao == "2":
            sacar(contas)
        elif opcao == "3":
            exibir_extrato(contas)
        elif opcao == "4":
            criar_cliente(clientes)
        elif opcao == "5":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)
        elif opcao == "6":
            listar_contas(contas)
        elif opcao == "7":
            listar_clientes(clientes)
        elif opcao == "8":
            break
        else:
            print("Opção inválida")


if __name__ == "__main__":
    atm()
