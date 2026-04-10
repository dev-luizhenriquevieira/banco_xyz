import textwrap


def recuperar_conta_cliente(banco, cpf):
    resultado = banco.contas_do_cliente(cpf)
    if not resultado.success:
        print(f"\n{resultado.message}")
        return None

    contas = resultado.data
    if not contas:
        print("\nCliente nao possui conta cadastrada.")
        return None

    if len(contas) == 1:
        return contas[0]

    print("\nContas disponiveis:")
    for i, conta in enumerate(contas, start=1):
        print(f"[{i}] Agencia: {conta.agencia} | Conta: {conta.numero}")

    while True:
        try:
            opcao = int(input("Selecione o numero da conta: "))
            if 1 <= opcao <= len(contas):
                return contas[opcao - 1]
            print("Opcao invalida.")
        except ValueError:
            print("Digite um numero valido.")


def depositar(banco):
    cpf = input("Informe o CPF do cliente: ")
    conta = recuperar_conta_cliente(banco, cpf)
    if not conta:
        return

    try:
        valor = float(input("Informe o valor do deposito: "))
    except ValueError:
        print("\nValor invalido. Operacao cancelada.")
        return

    sucesso, mensagem = banco.depositar(conta.numero, valor)
    print(f"\n{mensagem}")


def sacar(banco):
    cpf = input("Informe o CPF do cliente: ")
    conta = recuperar_conta_cliente(banco, cpf)
    if not conta:
        return

    try:
        valor = float(input("Informe o valor do saque: "))
    except ValueError:
        print("\nValor invalido. Operacao cancelada.")
        return

    sucesso, mensagem = banco.sacar(conta.numero, valor)
    print(f"\n{mensagem}")


def exibir_extrato(banco):
    cpf = input("Informe o CPF do cliente: ")
    conta = recuperar_conta_cliente(banco, cpf)
    if not conta:
        return

    sucesso, mensagem, extrato = banco.obter_extrato(conta.numero)
    if not sucesso:
        print(f"\n{mensagem}")
        return

    transacoes = extrato["transacoes"]
    saldo = extrato["saldo"]
    print("\n================ EXTRATO ================")
    corpo = ""
    if not transacoes:
        corpo = "Nao foram realizadas movimentacoes."
    else:
        for transacao in transacoes:
            corpo += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

    print(corpo)
    print(f"\nSaldo:\n\tR$ {saldo:.2f}")
    print("=========================================")


def criar_cliente(banco):
    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    cpf = input("Informe o CPF (somente numero): ")
    endereco = input(
        "Informe o endereco (logradouro, numero - bairro - cidade/sigla estado): "
    )

    sucesso, mensagem = banco.criar_cliente(
        nome=nome,
        data_nascimento=data_nascimento,
        cpf=cpf,
        endereco=endereco,
    )
    print(f"\n{mensagem}")


def criar_conta(banco):
    cpf = input("Informe o CPF do cliente: ")
    sucesso, mensagem = banco.criar_conta(cpf)
    print(f"\n{mensagem}")


def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))
