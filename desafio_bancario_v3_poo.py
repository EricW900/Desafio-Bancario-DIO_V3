from dataclasses import dataclass, field
from typing import List

@dataclass
class PessoaFisica:
    cpf: str
    nome: str
    data_nascimento: str


@dataclass
class Cliente(PessoaFisica):
    endereco: str
    contas: List['Conta']

    def adicionar_conta(self, conta: 'Conta'):
        self.contas.append(conta)
        print(f'Conta {conta.numero} adicionada para o cliente {self.nome}')


@dataclass
class Transacao:
    def registrar(self, conta: 'ContaCorrente'):
        ...


@dataclass
class Deposito(Transacao):
    valor: float

    def registrar(self, conta: 'ContaCorrente'):
        if self.valor >= 0 and self.valor <= 3000:
            conta.saldo_conta += self.valor
            conta.historico.adicionar_transacao(self)
        elif self.valor > 3000:
            print(f'O seu limite atual é de R$3000! E o valor inserido foi maior')
        else:
            print('Insira um valor positivo!')


@dataclass
class Saque(Transacao):
    valor: float

    def registrar(self, conta: 'ContaCorrente'):
        if self.valor > 0:
            if conta.limite_saques > 0:
                if conta.saldo_conta >= self.valor:
                    conta.saldo_conta -= self.valor
                    conta.historico.adicionar_transacao(self)
                    conta.limite_saques -= 1
                    print(f'Saque realizado no valor de R${self.valor}')
                else:
                    print('Saldo insuficiente!')
            else:
                print('Você atingiu seu limite diário de saques! Tente amanhã.')
        else:
            print('O valor de saque deve ser positivo!')


@dataclass
class Historico:
    transacoes: list[Transacao] = field(default_factory = list)

    def adicionar_transacao(self, transacao: Transacao):
        self.transacoes.append(transacao)


@dataclass
class Conta:
    saldo_conta: float
    numero: int
    agencia: str
    cliente: Cliente
    historico: Historico

    def saldo(self) -> float:
        return self.saldo_conta


    def sacar(self, valor: float) -> bool:
        ...


    def depositar(self, valor: float) -> bool:
        ...


@dataclass
class ContaCorrente(Conta):
    limite: float
    limite_saques: int


def main():
    numero_agencia = 1000
    numero_conta = 2000
    clientes = {}

    def mostrar_menu():
        menu = """
        Selecione uma opção:

        [d] Depositar
        [s] Sacar
        [e] Extrato
        [nu] Novo usuário (Cliente)
        [nc] Nova conta
        [q] Sair

        => """
        return input(menu).lower() # Converter opção para minúscula

    # Loop principal
    while True:
        opcao = mostrar_menu()

        # Opção de depósito
        if opcao == 'd':
            valor_deposito = input('Insira um valor a ser depositado: R$: ')

            try:
                valor_deposito = float(valor_deposito)  # Converte para número
                if valor_deposito <= 0:
                    raise ValueError('O valor deve ser maior que zero!')

            except ValueError as e:
                print(f'Erro! {e}')
                continue  # Volta ao menu principal

            cpf = input('Insira o CPF da conta a ser realizada o depósito: ')

            if cpf in clientes:
                cliente = clientes[cpf]

                # Se o cliente tiver mais de uma conta, ele permite a seleção da respectiva conta
                if len(cliente.contas) == 0:
                    print('Cliente não possui contas!')
                    continue  # Volta ao menu principal
                elif len(cliente.contas) == 1:
                    conta = cliente.contas[0]  # Se só tem uma conta, usamos ela
                else:
                    print('Cliente possui múltiplas contas. Selecione uma:')
                    for i, c in enumerate(cliente.contas):
                        print(f"[{i}] Conta {c.numero} - Agência {c.agencia}")
                    try:
                        conta_selecionada = int(input("Escolha o número da conta: "))
                        if conta_selecionada < 0 or conta_selecionada >= len(cliente.contas):
                            print('Erro! Seleção de conta inválida.')
                            continue  # Volta ao menu principal
                        conta = cliente.contas[conta_selecionada]
                    except ValueError:
                        print('Erro! Por favor, insira um número válido.')
                        continue  # Volta ao menu principal

                if valor_deposito > conta.limite:
                    print(f'Não é possível depositar um valor maior que o limite de sua conta! Limite atual R${conta.limite:.2f}')
                else:
                    # Realiza o depósito
                    deposito = Deposito(valor=valor_deposito)
                    deposito.registrar(conta)
                    print(f'Depósito de R${valor_deposito:.2f} realizado com sucesso para a conta {conta.numero}!')

            else:
                print('Erro! Cliente não encontrado.')


        # Opção de saque
        elif opcao == 's':
            valor_saque = input('Insira um valor a ser sacado: R$')

            try:
                valor_saque = float(valor_saque)

                if valor_saque <= 0:
                    print('Erro! O valor deve ser positivo!')
                    continue

            except ValueError:
                print('Erro! Insira um valor numérico válido!')
                continue

            # Solicita o CPF do cliente
            cpf = input('Insira o CPF da conta para realizar o saque: ')

            if cpf in clientes:
                cliente = clientes[cpf]

                # Se o cliente não tiver contas, exibe uma mensagem de erro
                if len(cliente.contas) == 0:
                    print('Cliente não possui contas!')
                elif len(cliente.contas) == 1:
                    conta = cliente.contas[0]
                else:
                    print('Cliente possui múltiplas contas. Selecione uma:')
                    for i, c in enumerate(cliente.contas):
                        print(f"[{i}] Conta {c.numero} - Agência {c.agencia}")
                    conta_selecionada = int(input("Escolha o número da conta: "))
                    conta = cliente.contas[conta_selecionada]

                if conta.limite_saques <= 0:
                    print('Você atingiu o limite diário de saques! Tente amanhã!')

                # else: Realiza o saque
                saque = Saque(valor=valor_saque)
                saque.registrar(conta)

            else:
                print('Erro! Cliente não encontrado.')



        # Opção de extrato
        elif opcao == 'e':
            cpf = input('Insira o CPF para visualizar o extrato: ')

            if cpf in clientes:
                cliente = clientes[cpf]

                # Verifica se o cliente possui alguma conta bancária
                if len(cliente.contas) == 0:
                    print('Cliente não possui contas!')
                elif len(cliente.contas) == 1:
                    conta = cliente.contas[0]
                else:
                    print('Cliente possui múltiplas contas. Selecione uma:')
                    for i, c in enumerate(cliente.contas):
                        print(f"[{i}] Conta {c.numero} - Agência {c.agencia}")
                    conta_selecionada = int(input("Escolha o número da conta: "))
                    conta = cliente.contas[conta_selecionada]

                # Exibe o saldo e o histórico de transações
                print(f"\n=== Extrato da Conta {conta.numero} - Agência {conta.agencia} ===")
                print(f"Saldo atual: R${conta.saldo_conta:.2f}")

                if len(conta.historico.transacoes) == 0:
                    print("Nenhuma transação realizada.")
                else:
                    print("Histórico de transações:")
                    for transacao in conta.historico.transacoes:
                        if isinstance(transacao, Deposito):
                            tipo_transacao = "Depósito"
                        elif isinstance(transacao, Saque):
                            tipo_transacao = "Saque"
                        else:
                            tipo_transacao = "Transação desconhecida"

                        print(f"- {tipo_transacao} de R${transacao.valor:.2f}")

                print("=== Fim do Extrato ===\n")

            else:
                print('Erro! Cliente não encontrado.')


        # Opção para cadastrar novo usuário (cliente)
        elif opcao == 'nu':
            print('=== CADASTRO DE NOVO USUÁRIO ===')

            # Validação do CPF
            while True:
                cpf = input('Insira um CPF (apenas números ou use "." e "-"): ').replace('.', '').replace('-', '')

                while cpf in clientes:
                    cpf = input('Este CPF já está cadastrado! Insira um CPF (apenas números ou use "." e "-"): ').replace('.', '').replace('-', '')

                if cpf.isnumeric() and len(cpf) == 11:
                    break
                else:
                    print('Erro! O CPF deve conter apenas números e ter 11 dígitos.')

            # Validação do nome
            while True:
                nome = input('Insira um nome de usuário: ').strip().capitalize()
                if nome.isalpha():
                    break
                else:
                    print('Erro! O nome deve conter apenas letras.')

            # Inserção do endereço
            endereco = str(input('Insiria um endereço: '))

            # Validação da data de nascimento
            while True:
                data_de_nascimento = input('Insira a data de nascimento (DD/MM/AAAA): ')
                try:
                    dia, mes, ano = map(int, data_de_nascimento.split('/'))
                    if len(data_de_nascimento) == 10 and 1 <= dia <= 31 and 1 <= mes <= 12 and ano > 1900:
                        break
                    else:
                        print('Erro! Insira uma data válida no formato DD/MM/AAAA.')
                except ValueError:
                    print('Erro! Insira uma data válida no formato DD/MM/AAAA.')

            novo_cliente = Cliente(
            cpf=cpf,
            nome=nome,
            data_nascimento=data_de_nascimento,
            endereco=endereco,
            contas=[]
            )

            clientes[cpf] = novo_cliente

            # DEBUG
            print(f"Cliente {nome} cadastrado com sucesso!")
            print(f"Clientes cadastrados: {clientes}")


        # Opção para criar uma nova conta de cliente
        elif opcao == 'nc':
            cpf = str(input('Insira o CPF do cliente: '))

            # Verifica se o cliente existe no dicionário 'clientes'
            if cpf in clientes:
                numero_conta += 1
                numero_agencia += 1

                # Cria a nova conta
                nova_conta = ContaCorrente(
                    limite=3000,
                    limite_saques=3, # Limite diário de saques
                    saldo_conta=0.0,
                    numero=numero_conta,
                    agencia=str(numero_agencia),
                    cliente=clientes[cpf],
                    historico=Historico()  # Criando um novo histórico
                )

                # Adiciona a conta à lista de contas do cliente
                clientes[cpf].adicionar_conta(nova_conta)
                print(f"Conta {numero_conta} criada para o cliente {clientes[cpf].nome}!")
            else:
                print('Cliente não existe!')

        # Opção de sair do sistema
        elif opcao == 'q':
            print('Saindo do banco! Obrigado por nos acessar!')
            break

        # Caso a opção inserida não exista/seja inválida
        else:
            print('Operação inválida! Tente novamente.')


# Cliente
main()