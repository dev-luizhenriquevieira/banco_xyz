from sistema_bancario.services.banco import Banco
from sistema_bancario.ui.cli_operacoes import (
    criar_cliente,
    criar_conta,
    depositar,
    exibir_extrato,
    listar_contas,
    sacar,
)
from sistema_bancario.ui.menu import menu


def main():
    banco = Banco()

    while True:
        opcao = menu()

        if opcao == "1":
            depositar(banco)

        elif opcao == "2":
            sacar(banco)

        elif opcao == "3":
            exibir_extrato(banco)

        elif opcao == "6":
            criar_cliente(banco)

        elif opcao == "4":
            criar_conta(banco)

        elif opcao == "5":
            listar_contas(banco.listar_contas())

        elif opcao == "0":
            break

        else:
            print(
                "\nâš ï¸ OperaÃ§Ã£o invÃ¡lida, por favor selecione novamente a operaÃ§Ã£o desejada."
            )
