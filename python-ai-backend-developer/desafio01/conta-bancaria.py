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
    opcao = int(input("Informe uma opção: "))

    if opcao == 1:
        deposito = float(input("Informe o valor do depósito: "))
        if deposito > 0:
            saldo += deposito
            extrato += f"Depósito: R$ {deposito:.2f}\n"
        else:
            print("Operação falhou! O valor informado para depósito é inválido!")

    elif opcao == 2:
        saque = float(input("Informe o valor do saque: "))
        if saque > 0:
            if saldo >= saque:
                if limite >= saque:
                    if numero_saques > 0:
                        saldo -= saque
                        numero_saques -= 1
                        extrato += f"Saque: R$ {saque:.2f}\n"
                    else:
                        print("Operação falhou! Você excedeu a quantidade de saques diários.")
                else:
                    print("Operação falhou! Você excedeu o valor limite por transação de saque diário.")
            else:
                print("Operação falhou! Você não possui saldo suficiente.")
        else:
            print("Operação falhou! O valor informado para saque é inválido.")

    elif opcao == 3:
        print("#################### EXTRATO ########################")
        print(extrato)
        print(f"Saldo atual: R$ {saldo:.2f}")
        if numero_saques > 1:
            print(f"Você pode realizar hoje {numero_saques} transações de saque em sua conta.")
        elif numero_saques > 0:
            print(f"Você pode realizar hoje {numero_saques} transação de saque em sua conta.")
        else:
            print(f"Você não possui mais transação de saque permitida em sua conta nesta data.")
        print(f"Seu limite de saque por transação é R$ {limite:.2f}.")
        print("#####################################################")

    elif opcao == 4:
        print("Obrigado por utilizar nosso sistema bancário!")
        break

    else:
        print("Opção inválida!")