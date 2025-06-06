#Sistema bancário melhorado com funções: Saque - 2 argumentos apenas por nome; Depósito - argumentos apenas por posição; Extrato - argumentos por posição e nome.
#Criar usuários (nome, nascimento, cpf, endereço) e contas (agencia, conta sequencial, usuário) e vinculá-los.
#Um usuário pode ter mais de uma conta, mas uma conta só pode ter 1 usuário. O CPF não pode ser repetido. 

usuarios = []
contas = []

def criar_usuario():
    print("NOVO USUÁRIO".center(30, "-"), "\n")
    cpf = input("Informe o seu CPF (apenas números): ")

    if len(cpf) != 11 or not cpf.isdigit():
        print("CPF inválido! O CPF deve conter 11 dígitos numéricos.\n")
    
    elif cpf in [usuario['cpf'] for usuario in usuarios]:
        print("CPF já cadastrado!")
        usuario = next((usuario for usuario in usuarios if usuario['cpf'] == cpf), None)
        selecionar_conta(usuario)

    else:
        primeiro_nome = input("Informe o seu primeiro nome: ")
        sobrenome = input("Informe o seu sobrenome: ")
        nome = {"Nome": primeiro_nome,"Sobrenome": sobrenome}
        data_nascimento = input("Informe a sua data de nascimento (dd/mm/aaaa): ")
        logradouro = input("Informe o seu logradouro: ")
        numero = input("Informe o número da sua residência: ")  
        bairro = input("Informe o seu bairro: ")
        cidade = input("Informe a sua cidade: ")                      
        sigla_estado = input("Informe a sigla do seu estado (ex: SP, RJ): ")
        endereco = {
            "logradouro": logradouro,
            "numero": numero,
            "bairro": bairro,
            "cidade": cidade,
            "sigla_estado": sigla_estado
        }
        usuario = {
            "nome": nome,
            "data_nascimento": data_nascimento,
            "cpf": cpf,
            "endereco": endereco
        }
        print(f"Usuário {primeiro_nome} cadastrado com sucesso!\n")
        usuarios.append(usuario)
        selecionar_conta(usuario)   
  
def criar_conta(usuario):
    print("NOVA CONTA".center(30, "-"), "\n")
    AGENCIA = "0001"  # Agência padrão
    numero_conta = len(contas) + 1 
    conta = {
        "numero": numero_conta,
        "agencia": AGENCIA,
        "usuario": usuario,
        "nome": usuario['nome']['Nome'],
        "saldo": 0.0,        
        "depositos": [],
        "saques": [],
    }

    contas.append(conta)
    print(f"Conta {numero_conta} criada com sucesso para o cliente {usuario['nome']['Nome']}!\n") 
    selecionar_conta(usuario)
            
def listar_contas(usuario):
    print("CONTAS ABERTAS".center(30, "-"), "\n")
    contas_usuario = [conta for conta in contas if conta['usuario']['cpf'] == usuario['cpf']]
    for conta in contas_usuario:
        print(f"Conta {conta['numero']} - Agência {conta['agencia']} - Saldo: R$ {conta['saldo']:.2f}")
    return usuario, contas_usuario

def selecionar_conta(usuario):
    print(f"Olá, {usuario['nome']['Nome']}!\n")
    contas_usuario = listar_contas(usuario)
    
    if not contas_usuario:
        print("Você não possui contas abertas. Por favor, crie uma nova conta.\n")
        criar_conta(usuario)
        return
    
    escolha_conta = int(input("Digite o número da conta que deseja acessar, ou 0 para criar uma nova conta: \n"))
        
    if escolha_conta == 0:
        criar_conta(usuario)

    else:
        conta = next((conta for conta in contas if conta['numero'] == escolha_conta), None)

        if conta:
            print(f"Conta {conta['numero']} selecionada com sucesso! \n")
            apresentar_menu(conta)  
    
        else:
            print("Conta não encontrada! Por favor, verifique o número da conta.\n")
                
def informar_valor():
    valor = float(input("Digite o valor da transação: \n"))
    if valor <= 0:
        print("Valor inválido! O valor informado deve ser maior que zero.\n")
    else:
        return valor

#Deposito: deve receber argumentos apenas por posição (positional only).
def realizar_deposito(valor, saldo, depositos, /):
    depositos.append(valor)
    saldo += valor  
    print(f'''Depósito de R$ {valor:.2f} realizado com sucesso!
          \nSeu saldo atual é R$ {saldo:.2f}.\n''')
    return saldo

#Saque: deve receber os argumentos apenas por nome (keyword only).
def realizar_saque(*, valor, saques, saldo, limite_saque_diario = 3, limite_transacao = 500.00):
    if len(saques) >= limite_saque_diario:
        print(f"Você já atingiu o limite de {limite_saque_diario} saques diários.\n")
    elif valor > limite_transacao:
            print(f"O limite máximo por transação é {limite_transacao}.\n")
    elif valor > saldo:
        print(f" O seu saldo (R${saldo}) é insuficiente para realizar o saque de R${valor}.\n")
    else:
        saques.append(valor)
        saldo -= valor
        print(f"Saque efetuado com sucesso! Você já utililizou {len(saques)} de {limite_saque_diario} transações disponíveis por dia.\n")
    return saldo

#Extrato: deve receber argumentos por posição e nome (positional only e keyword only). 
# Argumentos posicionais: saldo, argumentos nomeados: extrato.
def solicitar_extrato(saldo, /, *, depositos=None, saques=None):
    if depositos is None:
        depositos = []
    if saques is None:
        saques = []     
    print("EXTRATO".center(30, "#"), "\n")
    print("DEPÓSITOS".center(30, "-"))  
    if not depositos:
        print("Nenhum depósito realizado.\n")
    else:
        print(f"Total de depósitos: {len(depositos)}")
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
     
def main():
    print("Bem-vindo(a) ao nosso Sistema Bancário!")
    while True:
        cpf = input("Para começar, informe o CPF do cliente, ou 0 para criar um novo usuário.\n")
    
        if cpf == "0":
            criar_usuario()
        
        elif not cpf.isdigit() or len(cpf) != 11:
            print("CPF inválido! O CPF deve conter 11 dígitos.\n")
            return
               
        elif cpf in [usuario['cpf'] for usuario in usuarios]:
            usuario = next((usuario for usuario in usuarios if usuario['cpf'] == cpf), None)
            selecionar_conta(usuario)
        else:
            print("Usuário não encontrado! Por favor, verifique o CPF informado.\n")
                  
def apresentar_menu(conta):
    while True:
        print("\n***MENU DE OPÇÕES***")
        opcao = input(f"{conta['nome']}, escolha uma opção:\n1 - Depósito\n2 - Saque\n3 - Extrato\n4 - Sair\n")

        if opcao == "1":
            valor = informar_valor()
            if valor:
                conta['saldo'] = realizar_deposito(valor, conta['saldo'], conta['depositos'])
               
        elif opcao == "2":
            valor = informar_valor()
            if valor:
                conta['saldo'] = realizar_saque(valor=valor, saques=conta['saques'], saldo=conta['saldo'])
                        
        elif opcao == "3":
            solicitar_extrato(
                conta['saldo'],
                depositos=conta['depositos'],
                saques=conta['saques']
            )
       
        elif opcao == "4":  
            print("Obrigado(a) por usar nosso sistema bancário!")
            break   

        else:
            print("Opção inválida! Por favor, escolha uma opção válida.")
        
if __name__ == "__main__":
    main()