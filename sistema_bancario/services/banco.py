import io
from contextlib import redirect_stdout

from sistema_bancario.models import ContaCorrente, Deposito, PessoaFisica, Saque
from sistema_bancario.services.result import OperationResult


class Banco:
    def __init__(self):
        self._clientes = []
        self._contas = []

    @property
    def clientes(self):
        return self._clientes

    @property
    def contas(self):
        return self._contas

    def listar_clientes(self):
        return list(self._clientes)

    def listar_contas(self):
        return list(self._contas)

    def buscar_cliente_por_cpf(self, cpf):
        for cliente in self._clientes:
            if cliente.cpf == cpf:
                return cliente
        return None

    def buscar_conta(self, numero_conta):
        for conta in self._contas:
            if conta.numero == numero_conta:
                return conta
        return None

    def criar_cliente(self, nome, data_nascimento, cpf, endereco):
        if self.buscar_cliente_por_cpf(cpf):
            return False, "Ja existe um cliente com esse CPF."

        cliente = PessoaFisica(
            nome=nome,
            data_nascimento=data_nascimento,
            cpf=cpf,
            endereco=endereco,
        )
        self._clientes.append(cliente)
        return True, "Cliente cadastrado com sucesso."

    def criar_conta(self, cpf):
        cliente = self.buscar_cliente_por_cpf(cpf)
        if not cliente:
            return False, "Cliente nao encontrado."

        numero_conta = len(self._contas) + 1
        conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
        self._contas.append(conta)
        cliente.adicionar_conta(conta)
        return True, f"Conta {numero_conta} criada com sucesso."

    def contas_do_cliente(self, cpf):
        cliente = self.buscar_cliente_por_cpf(cpf)
        if not cliente:
            return OperationResult(False, "Cliente nao encontrado.")
        return OperationResult(True, "Contas carregadas com sucesso.", list(cliente.contas))

    def depositar(self, numero_conta, valor):
        conta = self.buscar_conta(numero_conta)
        if not conta:
            return False, "Conta nao encontrada."

        transacao = Deposito(valor)
        sucesso, mensagem = self._executar_operacao(lambda: conta.depositar(transacao.valor))
        if not sucesso:
            return False, mensagem or "Nao foi possivel realizar o deposito."

        conta.historico.adicionar_transacao(transacao)
        return True, mensagem or "Deposito realizado com sucesso."

    def sacar(self, numero_conta, valor):
        conta = self.buscar_conta(numero_conta)
        if not conta:
            return False, "Conta nao encontrada."

        transacao = Saque(valor)
        sucesso, mensagem = self._executar_operacao(lambda: conta.sacar(transacao.valor))
        if not sucesso:
            return False, mensagem or "Nao foi possivel realizar o saque."

        conta.historico.adicionar_transacao(transacao)
        return True, mensagem or "Saque realizado com sucesso."

    def obter_extrato(self, numero_conta):
        conta = self.buscar_conta(numero_conta)
        if not conta:
            return False, "Conta nao encontrada.", None

        extrato = {
            "conta": conta,
            "saldo": conta.saldo,
            "transacoes": conta.historico.transacoes,
        }
        return True, "Extrato carregado com sucesso.", extrato

    def _executar_operacao(self, operacao):
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            sucesso = operacao()

        mensagem = buffer.getvalue().strip()
        mensagem = " ".join(mensagem.split())
        return sucesso, mensagem
