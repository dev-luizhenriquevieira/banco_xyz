import textwrap


def menu():
    menu_texto = """\n
    ================ MENU PRINCIPAL ================
    [1] Realizar depÃ³sito
    [2] Realizar saque
    [3] Consultar extrato
    [4] Criar nova conta
    [5] Listar contas cadastradas
    [6] Cadastrar novo usuÃ¡rio
    [0] Sair
    ================================================
    Selecione a opÃ§Ã£o desejada: """
    return input(textwrap.dedent(menu_texto))
