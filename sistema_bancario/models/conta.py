from datetime import datetime


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\nâš ï¸ OperaÃ§Ã£o nÃ£o autorizada! Saldo insuficiente.")

        elif valor > 0:
            self._saldo -= valor
            print("\nâœ… Saque realizado com sucesso.")
            return True

        else:
            print("\n âš ï¸ OperaÃ§Ã£o invÃ¡lida! Informe um valor positivo para saque.")
        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\nâœ… DepÃ³sito efetuado com sucesso.")
        else:
            print("\nâš ï¸ OperaÃ§Ã£o invÃ¡lida! Informe um valor positivo para depÃ³sito.")
            return False
        return True


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [
                transacao
                for transacao in self.historico.transacoes
                if transacao["tipo"] == "Saque"
            ]
        )

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print("\nâš ï¸ OperaÃ§Ã£o nÃ£o autorizada! Valor do saque excede o limite.")

        elif excedeu_saques:
            print(
                "\nâš ï¸ OperaÃ§Ã£o nÃ£o autorizada! NÃºmero mÃ¡ximo de saques diÃ¡rios atingido."
            )

        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f"""\
            AgÃªncia:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """
