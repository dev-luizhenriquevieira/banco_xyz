from sistema_bancario.services.operacoes import (
    criar_cliente,
    criar_conta,
    depositar,
    exibir_extrato,
    listar_contas,
    sacar,
)
from sistema_bancario.ui.menu import menu


def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "1":
            depositar(clientes)

        elif opcao == "2":
            sacar(clientes)

        elif opcao == "3":
            exibir_extrato(clientes)

        elif opcao == "6":
            criar_cliente(clientes)

        elif opcao == "4":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif opcao == "5":
            listar_contas(contas)

        elif opcao == "0":
            break

        else:
            print(
                "\nâš ï¸ OperaÃ§Ã£o invÃ¡lida, por favor selecione novamente a operaÃ§Ã£o desejada."
            )
