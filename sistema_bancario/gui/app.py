import tkinter as tk
from tkinter import ttk

from sistema_bancario.auth.service import AuthService
from sistema_bancario.services.banco import Banco


class BankApp:
    def __init__(self):
        self.banco = Banco()
        self.auth = AuthService()
        self.root = tk.Tk()
        self.root.title("Sistema Bancario")
        self.root.geometry("1200x760")
        self.root.minsize(1024, 680)
        self.root.configure(bg="#f4efe7")

        self.status_var = tk.StringVar(value="Sistema pronto para uso.")
        self.login_user_var = tk.StringVar(value="consultor")
        self.login_password_var = tk.StringVar()

        self._configure_styles()
        self._build_login()

    def _configure_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("App.TFrame", background="#f4efe7")
        style.configure("Card.TFrame", background="#fbf8f3", relief="flat")
        style.configure(
            "Title.TLabel",
            background="#f4efe7",
            foreground="#16302b",
            font=("Georgia", 26, "bold"),
        )
        style.configure(
            "Subtitle.TLabel",
            background="#f4efe7",
            foreground="#50615d",
            font=("Segoe UI", 10),
        )
        style.configure(
            "CardTitle.TLabel",
            background="#fbf8f3",
            foreground="#16302b",
            font=("Segoe UI", 13, "bold"),
        )
        style.configure(
            "CardText.TLabel",
            background="#fbf8f3",
            foreground="#41504d",
            font=("Segoe UI", 10),
        )
        style.configure(
            "Accent.TButton",
            font=("Segoe UI", 10, "bold"),
            padding=(14, 10),
            background="#16302b",
            foreground="#fbf8f3",
            borderwidth=0,
        )
        style.map(
            "Accent.TButton",
            background=[("active", "#20413b")],
            foreground=[("active", "#fbf8f3")],
        )
        style.configure(
            "Treeview",
            rowheight=28,
            font=("Segoe UI", 10),
            background="#fffdf9",
            fieldbackground="#fffdf9",
            foreground="#273533",
        )
        style.configure(
            "Treeview.Heading",
            font=("Segoe UI", 10, "bold"),
            background="#e7ddd0",
            foreground="#16302b",
        )

    def _build_layout(self):
        self._clear_root()
        wrapper = ttk.Frame(self.root, style="App.TFrame", padding=24)
        wrapper.pack(fill="both", expand=True)

        header = ttk.Frame(wrapper, style="App.TFrame")
        header.pack(fill="x")

        ttk.Label(header, text="Painel Bancario", style="Title.TLabel").pack(
            anchor="w"
        )
        ttk.Label(
            header,
            text=f"Painel interno autenticado como {self.auth.session.username}.",
            style="Subtitle.TLabel",
        ).pack(anchor="w", pady=(4, 18))

        metrics = ttk.Frame(wrapper, style="App.TFrame")
        metrics.pack(fill="x", pady=(0, 18))

        self.metric_clientes = self._create_metric_card(metrics, "Clientes", "0", 0)
        self.metric_contas = self._create_metric_card(metrics, "Contas", "0", 1)
        self.metric_saldo = self._create_metric_card(metrics, "Saldo total", "R$ 0,00", 2)

        content = ttk.Frame(wrapper, style="App.TFrame")
        content.pack(fill="both", expand=True)
        content.columnconfigure(0, weight=1)
        content.columnconfigure(1, weight=1)
        content.rowconfigure(1, weight=1)

        self._build_client_form(content)
        self._build_account_form(content)
        self._build_transaction_form(content)
        self._build_lists(content)

        status_bar = ttk.Frame(wrapper, style="Card.TFrame", padding=(16, 12))
        status_bar.pack(fill="x", pady=(18, 0))
        ttk.Label(status_bar, textvariable=self.status_var, style="CardText.TLabel").pack(
            side="left", anchor="w"
        )
        ttk.Button(
            status_bar,
            text="Sair",
            style="Accent.TButton",
            command=self._handle_logout,
        ).pack(side="right")

        self._refresh_all()

    def _build_login(self):
        self._clear_root()

        wrapper = ttk.Frame(self.root, style="App.TFrame", padding=24)
        wrapper.pack(fill="both", expand=True)
        wrapper.columnconfigure(0, weight=1)
        wrapper.rowconfigure(0, weight=1)

        card = ttk.Frame(wrapper, style="Card.TFrame", padding=28)
        card.grid(row=0, column=0)

        ttk.Label(card, text="Acesso Administrativo", style="Title.TLabel").pack(
            anchor="w"
        )
        ttk.Label(
            card,
            text="Entre com uma conta interna para acessar o painel operacional.",
            style="Subtitle.TLabel",
        ).pack(anchor="w", pady=(4, 18))

        self._create_labeled_entry(card, "Usuario", self.login_user_var)
        self._create_labeled_entry(card, "Senha", self.login_password_var, show="*")

        ttk.Label(
            card,
            text="Credenciais demo: consultor / 1234",
            style="CardText.TLabel",
        ).pack(anchor="w", pady=(0, 10))
        ttk.Label(card, textvariable=self.status_var, style="CardText.TLabel").pack(
            anchor="w", pady=(0, 10)
        )

        ttk.Button(
            card,
            text="Entrar",
            style="Accent.TButton",
            command=self._handle_login,
        ).pack(anchor="e")

    def _create_metric_card(self, parent, title, value, column):
        card = ttk.Frame(parent, style="Card.TFrame", padding=18)
        card.grid(row=0, column=column, sticky="nsew", padx=(0, 12 if column < 2 else 0))
        parent.columnconfigure(column, weight=1)

        ttk.Label(card, text=title, style="CardText.TLabel").pack(anchor="w")
        value_label = ttk.Label(card, text=value, style="CardTitle.TLabel")
        value_label.pack(anchor="w", pady=(8, 0))
        return value_label

    def _build_client_form(self, parent):
        card = ttk.Frame(parent, style="Card.TFrame", padding=18)
        card.grid(row=0, column=0, sticky="nsew", padx=(0, 12), pady=(0, 12))

        ttk.Label(card, text="Novo cliente", style="CardTitle.TLabel").pack(anchor="w")
        ttk.Label(
            card,
            text="Registre um correntista com os dados principais.",
            style="CardText.TLabel",
        ).pack(anchor="w", pady=(4, 14))

        self.nome_var = tk.StringVar()
        self.nascimento_var = tk.StringVar()
        self.cpf_var = tk.StringVar()
        self.endereco_var = tk.StringVar()

        self._create_labeled_entry(card, "Nome completo", self.nome_var)
        self._create_labeled_entry(card, "Data de nascimento", self.nascimento_var)
        self._create_labeled_entry(card, "CPF", self.cpf_var)
        self._create_labeled_entry(card, "Endereco", self.endereco_var)

        ttk.Button(
            card,
            text="Cadastrar cliente",
            style="Accent.TButton",
            command=self._handle_criar_cliente,
        ).pack(anchor="e", pady=(10, 0))

    def _build_account_form(self, parent):
        card = ttk.Frame(parent, style="Card.TFrame", padding=18)
        card.grid(row=0, column=1, sticky="nsew", pady=(0, 12))

        ttk.Label(card, text="Nova conta", style="CardTitle.TLabel").pack(anchor="w")
        ttk.Label(
            card,
            text="Abra uma conta corrente para um cliente ja cadastrado.",
            style="CardText.TLabel",
        ).pack(anchor="w", pady=(4, 14))

        self.cpf_conta_var = tk.StringVar()
        self._create_labeled_entry(card, "CPF do cliente", self.cpf_conta_var)

        ttk.Button(
            card,
            text="Criar conta",
            style="Accent.TButton",
            command=self._handle_criar_conta,
        ).pack(anchor="e", pady=(10, 18))

        ttk.Separator(card, orient="horizontal").pack(fill="x", pady=4)

        ttk.Label(card, text="Extrato rapido", style="CardTitle.TLabel").pack(
            anchor="w", pady=(14, 0)
        )
        ttk.Label(
            card,
            text="Consulte o historico de uma conta no painel abaixo.",
            style="CardText.TLabel",
        ).pack(anchor="w", pady=(4, 12))

        self.extrato_var = tk.StringVar()
        self._create_labeled_entry(card, "Numero da conta", self.extrato_var)

        ttk.Button(
            card,
            text="Carregar extrato",
            style="Accent.TButton",
            command=self._handle_extrato,
        ).pack(anchor="e", pady=(10, 0))

    def _build_transaction_form(self, parent):
        card = ttk.Frame(parent, style="Card.TFrame", padding=18)
        card.grid(row=1, column=0, sticky="nsew", padx=(0, 12))

        ttk.Label(card, text="Movimentacoes", style="CardTitle.TLabel").pack(anchor="w")
        ttk.Label(
            card,
            text="Realize depositos e saques com atualizacao imediata no painel.",
            style="CardText.TLabel",
        ).pack(anchor="w", pady=(4, 14))

        self.transacao_conta_var = tk.StringVar()
        self.valor_var = tk.StringVar()

        self._create_labeled_entry(card, "Numero da conta", self.transacao_conta_var)
        self._create_labeled_entry(card, "Valor", self.valor_var)

        actions = ttk.Frame(card, style="Card.TFrame")
        actions.pack(fill="x", pady=(10, 0))

        ttk.Button(
            actions,
            text="Depositar",
            style="Accent.TButton",
            command=self._handle_deposito,
        ).pack(side="left")
        ttk.Button(
            actions,
            text="Sacar",
            style="Accent.TButton",
            command=self._handle_saque,
        ).pack(side="left", padx=10)

        self.resultado_extrato = tk.Text(
            card,
            height=14,
            bg="#fffdf9",
            fg="#22302d",
            relief="flat",
            font=("Consolas", 10),
            padx=12,
            pady=12,
        )
        self.resultado_extrato.pack(fill="both", expand=True, pady=(18, 0))

    def _build_lists(self, parent):
        card = ttk.Frame(parent, style="Card.TFrame", padding=18)
        card.grid(row=1, column=1, sticky="nsew")
        card.rowconfigure(1, weight=1)

        ttk.Label(card, text="Resumo operacional", style="CardTitle.TLabel").pack(
            anchor="w"
        )
        ttk.Label(
            card,
            text="Acompanhe clientes e contas ativas em tempo real.",
            style="CardText.TLabel",
        ).pack(anchor="w", pady=(4, 14))

        notebook = ttk.Notebook(card)
        notebook.pack(fill="both", expand=True)

        aba_clientes = ttk.Frame(notebook, style="Card.TFrame", padding=4)
        aba_contas = ttk.Frame(notebook, style="Card.TFrame", padding=4)
        notebook.add(aba_clientes, text="Clientes")
        notebook.add(aba_contas, text="Contas")

        self.tree_clientes = ttk.Treeview(
            aba_clientes,
            columns=("cpf", "nome", "nascimento"),
            show="headings",
        )
        for coluna, titulo, largura in (
            ("cpf", "CPF", 140),
            ("nome", "Nome", 220),
            ("nascimento", "Nascimento", 120),
        ):
            self.tree_clientes.heading(coluna, text=titulo)
            self.tree_clientes.column(coluna, width=largura, anchor="w")
        self.tree_clientes.pack(fill="both", expand=True)

        self.tree_contas = ttk.Treeview(
            aba_contas,
            columns=("numero", "titular", "saldo"),
            show="headings",
        )
        for coluna, titulo, largura in (
            ("numero", "Conta", 100),
            ("titular", "Titular", 220),
            ("saldo", "Saldo", 120),
        ):
            self.tree_contas.heading(coluna, text=titulo)
            self.tree_contas.column(coluna, width=largura, anchor="w")
        self.tree_contas.pack(fill="both", expand=True)

    def _create_labeled_entry(self, parent, label, variable, show=None):
        field = ttk.Frame(parent, style="Card.TFrame")
        field.pack(fill="x", pady=(0, 10))
        ttk.Label(field, text=label, style="CardText.TLabel").pack(anchor="w")
        ttk.Entry(field, textvariable=variable, show=show).pack(fill="x", pady=(4, 0))

    def _handle_login(self):
        sucesso, mensagem, _ = self.auth.login(
            self.login_user_var.get().strip(),
            self.login_password_var.get(),
        )
        self._set_status(mensagem)
        if sucesso:
            self.login_password_var.set("")
            self._build_layout()

    def _handle_logout(self):
        self.auth.logout()
        self.status_var.set("Sessao encerrada com seguranca.")
        self._build_login()

    def _handle_criar_cliente(self):
        if not all(
            [
                self.nome_var.get().strip(),
                self.nascimento_var.get().strip(),
                self.cpf_var.get().strip(),
                self.endereco_var.get().strip(),
            ]
        ):
            self._set_status("Preencha todos os campos do cliente.")
            return

        sucesso, mensagem = self.banco.criar_cliente(
            self.nome_var.get().strip(),
            self.nascimento_var.get().strip(),
            self.cpf_var.get().strip(),
            self.endereco_var.get().strip(),
        )
        if sucesso:
            self.nome_var.set("")
            self.nascimento_var.set("")
            self.cpf_var.set("")
            self.endereco_var.set("")

        self._set_status(mensagem)
        self._refresh_all()

    def _handle_criar_conta(self):
        cpf = self.cpf_conta_var.get().strip()
        if not cpf:
            self._set_status("Informe o CPF para abrir a conta.")
            return

        sucesso, mensagem = self.banco.criar_conta(cpf)
        if sucesso:
            self.cpf_conta_var.set("")

        self._set_status(mensagem)
        self._refresh_all()

    def _handle_deposito(self):
        self._executar_transacao("deposito")

    def _handle_saque(self):
        self._executar_transacao("saque")

    def _executar_transacao(self, tipo):
        try:
            numero_conta = int(self.transacao_conta_var.get().strip())
            valor = float(self.valor_var.get().strip())
        except ValueError:
            self._set_status("Informe numero da conta e valor validos.")
            return

        if tipo == "deposito":
            sucesso, mensagem = self.banco.depositar(numero_conta, valor)
        else:
            sucesso, mensagem = self.banco.sacar(numero_conta, valor)

        if sucesso:
            self.valor_var.set("")
            self._render_extrato(numero_conta)

        self._set_status(mensagem)
        self._refresh_all()

    def _handle_extrato(self):
        try:
            numero_conta = int(self.extrato_var.get().strip())
        except ValueError:
            self._set_status("Informe um numero de conta valido para consultar o extrato.")
            return

        sucesso, mensagem, _ = self.banco.obter_extrato(numero_conta)
        if sucesso:
            self._render_extrato(numero_conta)

        self._set_status(mensagem)

    def _render_extrato(self, numero_conta):
        sucesso, _, extrato = self.banco.obter_extrato(numero_conta)
        if not sucesso:
            return

        conta = extrato["conta"]
        linhas = [
            f"Agencia: {conta.agencia}",
            f"Conta: {conta.numero}",
            f"Titular: {conta.cliente.nome}",
            "-" * 40,
        ]

        if extrato["transacoes"]:
            for transacao in extrato["transacoes"]:
                linhas.append(
                    f"{transacao['data']} | {transacao['tipo']} | R$ {transacao['valor']:.2f}"
                )
        else:
            linhas.append("Nenhuma movimentacao registrada.")

        linhas.extend(["-" * 40, f"Saldo atual: R$ {extrato['saldo']:.2f}"])

        self.resultado_extrato.delete("1.0", tk.END)
        self.resultado_extrato.insert("1.0", "\n".join(linhas))

    def _refresh_all(self):
        self.metric_clientes.config(text=str(len(self.banco.clientes)))
        self.metric_contas.config(text=str(len(self.banco.contas)))
        saldo_total = sum(conta.saldo for conta in self.banco.contas)
        self.metric_saldo.config(text=f"R$ {saldo_total:.2f}".replace(".", ","))

        for item in self.tree_clientes.get_children():
            self.tree_clientes.delete(item)
        for cliente in self.banco.clientes:
            self.tree_clientes.insert(
                "",
                "end",
                values=(self._mask_cpf(cliente.cpf), cliente.nome, cliente.data_nascimento),
            )

        for item in self.tree_contas.get_children():
            self.tree_contas.delete(item)
        for conta in self.banco.contas:
            self.tree_contas.insert(
                "",
                "end",
                values=(conta.numero, conta.cliente.nome, f"R$ {conta.saldo:.2f}"),
            )

    def _set_status(self, message):
        self.status_var.set(message)

    def _mask_cpf(self, cpf):
        if len(cpf) < 4:
            return cpf
        return f"{'*' * max(len(cpf) - 4, 0)}{cpf[-4:]}"

    def _clear_root(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def run(self):
        self.root.mainloop()


def main():
    app = BankApp()
    app.run()
