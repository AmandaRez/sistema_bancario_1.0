from abc import ABC, abstractmethod

#Atualizar a implementação do sistema bancário, para armazenar os dados de clientes e contas bancárias em objetos ao invés de dicionários. 

clientes = []
contas = []

class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor
        })

    def listar_transacoes(self):
        for t in self.transacoes:
            print(f"{t['tipo']}: R$ {t['valor']:.2f}")

class Transacao(ABC):
    @abstractmethod
    def registrar(self, conta):
        pass

class TransacaoMonetaria(Transacao, ABC):    
    def __init__(self, valor):
        self.valor = valor

    def __str__(self):
        return f"{self.__class__.__name__}: R$ {self.valor:.2f}"

class Deposito(TransacaoMonetaria):
    def registrar(self, conta):
       sucesso = conta.depositar(self.valor)
       if sucesso:
           conta.historico.adicionar_transacao(self)
    
       
class Saque(TransacaoMonetaria):
    def registrar(self, conta):
        sucesso = conta.sacar(self.valor)
        if sucesso:
            conta.historico.adicionar_transacao(self)

class Conta:   
    def __init__(self, numero, cliente, agencia="0001"):
        self.numero = numero
        self.cliente = cliente
        self.agencia = agencia
        self.saldo = 0.0
        self.historico = Historico()    
    
    def saldo(self):
        return self.saldo
    
    def depositar(self, valor):
        if valor <= 0:
            print("Valor inválido! O valor do depósito deve ser maior que zero.")
            return False
        self.saldo += valor
        print(f"Depósito de R$ {valor:.2f} realizado com sucesso! Saldo atual: R$ {self.saldo:.2f}")        
        return True   
    
    def sacar(self, valor):
        if valor <= 0:
            print("Valor inválido! O valor do saque deve ser maior que zero.")
            return False
        if valor > self.saldo:
            print("Saldo insuficiente para realizar o saque.")
            return False
        self.saldo -= valor
        print(f"Saque de R$ {valor:.2f} realizado com sucesso! Saldo atual: R$ {self.saldo:.2f}")
        return True        

    @classmethod            
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)      

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500.0, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques
        self._saques_realizados = 0
        self._valor_saque_diario = 0.0

    def sacar(self, valor):
        if self._saques_realizados >= self.limite_saques:
            print("Limite de saques diários atingido.")
            return False
        if valor > self.saldo:
            print("Saldo insuficiente para realizar o saque.")
            return False
        if self._valor_saque_diario + valor > self.limite:
            print(f"Valor do saque excede o limite diário de R$ {self.limite:.2f}.")
            return False
        self.saldo -= valor
        self._saques_realizados += 1
        self._valor_saque_diario += valor
        print(f"Saque de R$ {valor:.2f} realizado com sucesso! Saldo atual: R$ {self.saldo:.2f}")
        return True

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def adicionar_conta(self, conta):
        self.contas.append(conta)
    
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, cpf, data_nascimento, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento

    def __str__(self):
        return f"{self.nome} - CPF: {self.cpf}"
    

def encontrar_cliente_por_cpf(cpf):
    for cliente in clientes:
        if isinstance(cliente, PessoaFisica) and cliente.cpf == cpf:
            return cliente
    return None

def encontrar_conta_por_numero(numero):
    for conta in contas:
        if conta.numero == numero:
            return conta
    return None


def listar_clientes():
    print("\n=== Lista de Clientes ===")
    for idx, cliente in enumerate(clientes, 1):
        print(f"{idx} - {cliente.nome} (CPF: {cliente.cpf})")

def listar_contas():
    print("\n=== Lista de Contas ===")
    for idx, conta in enumerate(contas, 1):
        print(f"{idx} - Conta: {conta.numero} | Cliente: {conta.cliente.nome} | Saldo: R$ {conta.saldo:.2f}")

def selecionar_conta():
    listar_contas()
    if not contas:
        print("Nenhuma conta cadastrada.")
        return None
    try:
        idx = int(input("Selecione o número da conta: ")) - 1
        if 0 <= idx < len(contas):
            return contas[idx]
        else:
            print("Índice inválido.")
            return None
    except ValueError:
        print("Entrada inválida.")
        return None

def menu():
    print("\n=== Sistema Bancário CLI ===")
    print("1 - Criar cliente")
    print("2 - Criar conta")
    print("3 - Listar clientes")
    print("4 - Listar contas")
    print("5 - Selecionar conta para transações")
    print("6 - Sair")
    return input("Escolha uma opção: ")

def menu_conta(conta):
    print(f"\n=== Conta {conta.numero} de {conta.cliente.nome} ===")
    print("1 - Depositar")
    print("2 - Sacar")
    print("3 - Extrato")
    print("4 - Voltar")
    return input("Escolha uma opção: ")

if __name__ == "__main__":
    while True:
        opcao = menu()
        if opcao == "1":
            nome = input("Nome: ")
            cpf = input("CPF: ")
            data_nascimento = input("Data de nascimento (dd/mm/aaaa): ")
            endereco = input("Endereço: ")
            if encontrar_cliente_por_cpf(cpf):
                print("Cliente já cadastrado.")
            else:
                cliente = PessoaFisica(nome, cpf, data_nascimento, endereco)
                clientes.append(cliente)
                print("Cliente criado com sucesso!")
                
        elif opcao == "2":
            cpf = input("CPF do cliente: ")
            cliente = encontrar_cliente_por_cpf(cpf)
            if not cliente:
                print("Cliente não encontrado.")
            else:
                numero = str(len(contas) + 1).zfill(4)  # Gera número sequencial com 4 dígitos
                conta = ContaCorrente(numero, cliente)
                cliente.adicionar_conta(conta)
                contas.append(conta)
                print(f"Conta criada com sucesso! Número da conta: {numero}")
        
        elif opcao == "3":
            listar_clientes()
        elif opcao == "4":
            listar_contas()
        elif opcao == "5":
            conta = selecionar_conta()
            if conta:
                while True:
                    op = menu_conta(conta)
                    if op == "1":
                        valor = float(input("Valor do depósito: "))
                        transacao = Deposito(valor)
                        conta.cliente.realizar_transacao(conta, transacao)
                    elif op == "2":
                        valor = float(input("Valor do saque: "))
                        transacao = Saque(valor)
                        conta.cliente.realizar_transacao(conta, transacao)
                    elif op == "3":
                        print(f"\nExtrato da conta {conta.numero}:")
                        conta.historico.listar_transacoes()
                        print(f"Saldo atual: R$ {conta.saldo:.2f}")
                    elif op == "4":
                        break
                    else:
                        print("Opção inválida.")
        elif opcao == "6":
            print("Saindo...")
            break
        else:
            print("Opção inválida.")