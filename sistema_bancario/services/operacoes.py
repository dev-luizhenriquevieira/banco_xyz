import textwrap

from sistema_bancario.models import ContaCorrente, Deposito, PessoaFisica, Saque


def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\nâš ï¸ Cliente nÃ£o possui conta cadastrada.")
        return None

    if len(cliente.contas) == 1:
        return cliente.contas[0]

    print("\nContas disponÃ­veis:")
    for i, conta in enumerate(cliente.contas, start=1):
        print(f"[{i}] AgÃªncia: {conta.agencia} | Conta: {conta.numero}")

    while True:
        try:
            opcao = int(input("Selecione o nÃºmero da conta: "))
            if 1 <= opcao <= len(cliente.contas):
                return cliente.contas[opcao - 1]
            else:
                print("âš ï¸ OpÃ§Ã£o invÃ¡lida.")
        except ValueError:
            print("âš ï¸ Digite um nÃºmero vÃ¡lido.")


def depositar(clientes):
    cpf = input("Informe o CPF do cliente:")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nâš ï¸ Cliente nÃ£o encontrado.")
        return

    try:
        valor = float(input("Informe o valor do depÃ³sito: "))
    except ValueError:
        print("\nâš ï¸ Valor invÃ¡lido. OperaÃ§Ã£o cancelada.")
        return

    transacao = Deposito(valor)
    conta = recuperar_conta_cliente(cliente)

    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


def sacar(clientes):
    cpf = input("Informe o CPF do cliente:")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nâš ï¸ Cliente nÃ£o encontrado.")
        return

    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente:")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nâš ï¸ Cliente nÃ£o encontrado.")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "NÃ£o foram realizadas movimentaÃ§Ãµes."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("=========================================")


def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente nÃºmero): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\nâš ï¸ JÃ¡ existe um cliente cadastrado com esse CPF.")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input(
        "Informe o endereÃ§o (logradouro, nÃºmero - bairro - cidade/sigla estado): "
    )

    cliente = PessoaFisica(
        nome=nome,
        data_nascimento=data_nascimento,
        cpf=cpf,
        endereco=endereco,
    )

    clientes.append(cliente)
    print("\nâœ… Cliente cadastrado com sucesso!")


def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print(
            "\nâš ï¸ Cliente nÃ£o encontrado. Ã‰ necessÃ¡rio cadastrar um cliente antes de criar uma conta."
        )
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("\nâœ… Conta criada com sucesso!")


def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))
