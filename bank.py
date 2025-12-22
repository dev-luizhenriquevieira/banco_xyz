from datetime import datetime


class Usuario:
    def __init__(self, nome, cpf, data_nascimento, endereco):
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento
        self.endereco = endereco
        self.data_criacao = datetime.now().strftime(
            "%d/%m/%Y %H:%M:%S")  # Registro da criação


class Conta:
    LIMITE_SAQUES = 3
    LIMITE_VALOR = 500

    def __init__(self, agencia, numero, usuario):
        self.agencia = agencia
        self.numero = numero
        self.usuario = usuario
        self.saldo = 0
        self.extrato = ""
        self.numero_saques = 0
        self.data_criacao = datetime.now().strftime(
            "%d/%m/%Y %H:%M:%S")  # Registro da criação

    def registrar_movimento(self, tipo, valor):
        """Registra movimentação com data e hora"""
        horario = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.extrato += f"{tipo}:\tR$ {valor:.2f} | {horario}\n"

    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            self.registrar_movimento("Depósito", valor)
            print("\n✅ Depósito efetuado com sucesso.")
            print(f"Saldo atual: R$ {self.saldo:.2f}")
        else:
            print("\n⚠️ Operação inválida: informe um valor positivo para depósito.")

    def sacar(self, valor):
        if valor > self.saldo:
            print("\n⚠️ Operação não autorizada: saldo insuficiente.")
        elif valor > Conta.LIMITE_VALOR:
            print(
                "\n⚠️ Operação não autorizada: valor solicitado excede o limite por saque.")
        elif self.numero_saques >= Conta.LIMITE_SAQUES:
            print("\n⚠️ Operação não autorizada: limite diário de saques atingido.")
        elif valor > 0:
            self.saldo -= valor
            self.numero_saques += 1
            self.registrar_movimento("Saque", valor)
            print("\n✅ Saque realizado com sucesso.")
            print(f"Saldo atual: R$ {self.saldo:.2f}")
        else:
            print("\n⚠️ Operação inválida: informe um valor positivo para saque.")

    def exibir_extrato(self):
        print("\n📊 Extrato da Conta")
        print("------------------------------------------")
        print("Nenhuma movimentação registrada." if not self.extrato else self.extrato)
        print(f"Saldo disponível: R$ {self.saldo:.2f}")
        print("------------------------------------------")


class Banco:
    def __init__(self):
        self.usuarios = []
        self.contas = []
        self.agencia = "0001"

    def criar_usuario(self):
        cpf = input("Informe o CPF (somente números): ")
        if any(u.cpf == cpf for u in self.usuarios):
            print("\n⚠️ Cadastro não realizado: já existe usuário com este CPF.")
            return

        nome = input("Informe o nome completo: ")
        data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
        endereco = input("Informe o endereço completo: ")

        usuario = Usuario(nome, cpf, data_nascimento, endereco)
        self.usuarios.append(usuario)
        print("\n✅ Usuário cadastrado com sucesso.")
        print(f"Data de criação do cadastro: {usuario.data_criacao}")

    def criar_conta(self):
        cpf = input("Informe o CPF do titular da conta: ")
        usuario = next((u for u in self.usuarios if u.cpf == cpf), None)

        if usuario:
            numero_conta = len(self.contas) + 1
            conta = Conta(self.agencia, numero_conta, usuario)
            self.contas.append(conta)
            print("\n✅ Conta criada com sucesso.")
            print(
                f"Agência: {conta.agencia} | Conta: {conta.numero} | Titular: {usuario.nome}")
            print(f"Data de criação da conta: {conta.data_criacao}")
        else:
            print("\n⚠️ Não foi possível criar a conta: usuário não encontrado.")

    def listar_contas(self):
        if not self.contas:
            print("\n⚠️ Nenhuma conta cadastrada até o momento.")
            return

        print("\n📋 Lista de Contas Cadastradas")
        print("=" * 50)
        for conta in self.contas:
            print(
                f"Agência: {conta.agencia} | Conta: {conta.numero} | Titular: {conta.usuario.nome}")
            print(f"Data de criação: {conta.data_criacao}")
            print("-" * 50)
        print("=" * 50)

    def excluir_conta(self):
        if not self.contas:
            print("\n⚠️ Nenhuma conta disponível para exclusão.")
            return

        numero = int(input("Informe o número da conta que deseja excluir: "))
        conta = next((c for c in self.contas if c.numero == numero), None)

        if conta:
            self.contas.remove(conta)
            horario = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            print(f"\n✅ Conta {numero} excluída com sucesso em {horario}.")
        else:
            print("\n⚠️ Conta não encontrada. Verifique o número informado.")


def menu():
    return input("""
================ MENU PRINCIPAL ================
[1] Realizar depósito
[2] Realizar saque
[3] Consultar extrato
[4] Criar nova conta
[5] Listar contas cadastradas
[6] Cadastrar novo usuário
[7] Excluir conta
[0] Encerrar sistema
================================================
Selecione a opção desejada: """)


def main():
    banco = Banco()

    while True:
        opcao = menu()

        if opcao == "6":
            banco.criar_usuario()
        elif opcao == "4":
            banco.criar_conta()
        elif opcao == "5":
            banco.listar_contas()
        elif opcao == "7":
            banco.excluir_conta()
        elif opcao in ["1", "2", "3"]:
            if not banco.contas:
                print(
                    "\n⚠️ Nenhuma conta disponível. Crie uma conta antes de realizar operações financeiras.")
                continue

            numero = int(input("Informe o número da conta: "))
            conta = next((c for c in banco.contas if c.numero == numero), None)

            if not conta:
                print("\n⚠️ Conta não encontrada. Verifique o número informado.")
                continue

            if opcao == "1":
                valor = float(input("Informe o valor do depósito: "))
                conta.depositar(valor)
            elif opcao == "2":
                valor = float(input("Informe o valor do saque: "))
                conta.sacar(valor)
            elif opcao == "3":
                conta.exibir_extrato()
        elif opcao == "0":
            print("\n✅ Sistema encerrado. Obrigado por utilizar nossos serviços!")
            break
        else:
            print("\n⚠️ Opção inválida. Por favor, selecione uma opção do menu.")


main()
