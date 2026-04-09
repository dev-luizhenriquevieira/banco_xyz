# Sistema Bancario

Projeto em Python com regras de negocio para clientes, contas, saques, depositos e extrato.

## Estrutura

- `bank.py`: entrada da versao em terminal
- `bank_gui.py`: entrada da interface grafica em `tkinter`
- `sistema_bancario/models`: entidades do dominio
- `sistema_bancario/services`: camada de servicos e operacoes
- `sistema_bancario/gui`: interface desktop

## Como executar

### Terminal

```bash
python bank.py
```

### Interface grafica

```bash
python bank_gui.py
```

## Situacao atual

- Arquitetura reorganizada em pacotes
- Interface desktop inicial para operacao bancaria
- Base pronta para evoluir para uma versao hibrida com area do cliente e area administrativa
