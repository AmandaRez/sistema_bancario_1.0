#Sistema bancário simples, que permite depositar, sacar e consultar extrato. Existe um limite de 3 saques diários, com um valor máximo de R$ 500,00 por transação.

saldo = 0.0
depositos = []
saques = []
LIMITE_SAQUES = 3

print("Bem-vind@ ao nosso Sistema Bancário!")

while True:
    print("\n***MENU DE OPÇÕES***")
    opcao = input("Escolha uma opção:\n1 - Depósito\n2 - Saque\n3 - Extrato\n4 - Sair\n")

    if opcao == "1":
        deposito = float(input("Digite o valor do deposito: \n"))
        if deposito <= 0:
            print("Valor inválido! O depósito deve ser maior que zero.\n")
        else:
            depositos.append(deposito)
            saldo += deposito
            print(f"Depósito de R$ {deposito:.2f} realizado com sucesso!\n")

    elif opcao == "2":
        saque = float(input("Digite o valor do saque: \n"))
        if len(saques) >= LIMITE_SAQUES:
            print(f"Você já atingiu o limite de {LIMITE_SAQUES} saques diários.\n")
        elif saque <= 0:
            print("Valor inválido! O saque deve ser maior que zero.\n")
        elif saque > 500:
            print("O limite máximo por transação é R$ 500,00.\n")
        elif saque > saldo:
            print("Saldo insuficiente para realizar o saque.\n")
        
        else:
            saques.append(saque)
            saldo -= saque
            print(f"Saque efetuado com sucesso! Você já utililizou {len(saques)} de {LIMITE_SAQUES} transações disponíveis por dia.\n")
                          
    elif opcao == "3":
        print("EXTRATO".center(30, "#"), "\n")
        print("DEPÓSITOS".center(30, "-"))
        if not depositos:
            print("Nenhum depósito realizado.\n")
        else:
            print(f"Total de depositos: {len(depositos)}")
            for i, deposito in enumerate(depositos, start=1):
                print(f"{i}. R$ {deposito:.2f}")
            print("\n")
        print("SAQUES".center(30, "-"))
        if not saques:
            print("Nenhum saque realizado.\n")
        else:
            print(f"Total de saques: {len(saques)}")
            for i, saque in enumerate(saques, start=1):
                print(f"{i}. R$ {saque:.2f}")
        print("\n")

        print(f"SALDO ATUAL: R$ {saldo:.2f}\n")

    elif opcao == "4":
        print("Obrigad@ por usar nosso sistema bancário!")
        break   

    else:
        print("Opção inválida! Por favor, escolha uma opção válida.")
