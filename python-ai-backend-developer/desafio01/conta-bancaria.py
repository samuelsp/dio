from datetime import datetime

menu = """
[1] Depositar
[2] Sacar
[3] Extrato
[4] Sair
"""

saldo, limite, numero_saques = 0, 500, 3
extrato = ''

print("###### SISTEMA BANCÁRIO DIO ######")

while True:
    print(menu)
    hoje = datetime.now()

    try:
        opcao = int(input("Informe uma opção: "))
    except ValueError:
        print("Digite um caracter válido!")
        continue

    if opcao == 1:
        deposito = float(input("Informe o valor do depósito: "))
        if deposito > 0:
            saldo += deposito
            hoje = hoje.strftime("%d/%m/%Y %H:%M:%S")
            extrato += f"Depósito: R$ {deposito:.2f} realizado em {hoje}.\n"
        else:
            print("Operação falhou! O valor informado para depósito é inválido!")

    elif opcao == 2:
        saque = float(input("Informe o valor do saque: "))

        saldo_permitido   = saldo >= saque
        limite_permitido  = limite >= saque
        saques_permitidos = numero_saques > 0

        if not saldo_permitido:
            print("Operação falhou! Você não possui saldo suficiente.")

        elif not limite_permitido:
            print("Operação falhou! Você excedeu o valor limite por transação de saque diário.")

        elif not saques_permitidos:
            print("Operação falhou! Você excedeu a quantidade de saques diários.")

        elif saque > 0:
            saldo -= saque
            numero_saques -= 1
            hoje = hoje.strftime("%d/%m/%Y %H:%M:%S")
            extrato += f"Saque: R$ {saque:.2f} realizado em {hoje}.\n"

        else:
            print("Operação falhou! O valor informado para saque é inválido.")

    elif opcao == 3:
        print("#################### EXTRATO ########################")
        print(extrato)
        print(f"Saldo atual: R$ {saldo:.2f}")
        if numero_saques > 1:
            print(f"Você pode realizar {numero_saques} transações de saque em sua conta.")
        elif numero_saques > 0:
            print(f"Você pode realizar {numero_saques} transação de saque em sua conta.")
        else:
            print(f"Você não possui mais transação de saque permitida em sua conta nesta data.")
        print(f"Seu limite de saque por transação é R$ {limite:.2f}.")
        print("#####################################################")

    elif opcao == 4:
        print("Obrigado por utilizar nosso sistema bancário!")
        break

    else:
        print("Opção inválida!")