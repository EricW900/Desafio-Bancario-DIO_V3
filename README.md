# Projeto Bancário em Python

Este é um projeto simples de simulação de um sistema bancário em Python, que permite o gerenciamento de clientes, contas bancárias e transações como depósitos, saques e consultas de extrato. O sistema simula funcionalidades básicas de um banco, onde os clientes podem possuir múltiplas contas, e realizar transações com limites de saque e depósito.

## Funcionalidades

- **Cadastro de Clientes**: Permite o cadastro de novos clientes com informações como CPF, nome, data de nascimento e endereço.
- **Criação de Contas**: Cada cliente pode ter uma ou mais contas correntes associadas, com limites de saldo e saques diários.
- **Depósitos**: Realiza depósitos em uma conta do cliente, com um limite máximo por transação.
- **Saques**: Permite que o cliente realize saques, respeitando o saldo disponível e o limite diário de saques.
- **Extrato**: Exibe o saldo atual e o histórico de transações (saques e depósitos) para cada conta.
- **Histórico de Transações**: Cada conta mantém um histórico detalhado das transações realizadas.

## Estrutura do Projeto

O projeto foi construído utilizando o paradigma de programação orientada a objetos. As principais classes e suas responsabilidades são:

- **PessoaFisica**: Representa os dados pessoais de um cliente (nome, CPF, data de nascimento).
- **Cliente**: Herda de `PessoaFisica` e adiciona a capacidade de gerenciar múltiplas contas.
- **Conta**: Representa uma conta bancária, contendo saldo, número da conta, agência e histórico de transações.
- **ContaCorrente**: Herda de `Conta` e adiciona um limite de saque e de saldo.
- **Transacao**: Classe base para representar uma transação financeira (depósito ou saque).
- **Deposito**: Herda de `Transacao` e implementa a lógica para realizar depósitos.
- **Saque**: Herda de `Transacao` e implementa a lógica para realizar saques, incluindo o controle de limite de saques diários.
- **Historico**: Armazena o histórico de transações de uma conta.

## Como Executar

1. Clone o repositório:

    ```bash
    git clone https://github.com/EricW900/Desafio-Bancario-DIO_V3.git
    ```

2. Navegue até o diretório do projeto:

    ```bash
    cd Desafio-Bancario-DIO_V3
    ```

3. Execute o arquivo principal:

    ```bash
    python desafio_bancario_v3_poo.py
    ```

4. Siga as instruções no menu interativo para realizar operações como depósito, saque, consulta de extrato, etc.

## Exemplo de Uso

O menu principal permite realizar as seguintes operações:

- `[d]` Depositar
- `[s]` Sacar
- `[e]` Extrato
- `[nu]` Novo usuário (Cliente)
- `[nc]` Nova conta
- `[q]` Sair

Por exemplo, para fazer um depósito:
1. Selecione a opção "d".
2. Informe o CPF do cliente.
3. Escolha a conta (caso o cliente tenha mais de uma).
4. Insira o valor a ser depositado.

O sistema validará o valor e aplicará o depósito à conta selecionada.

## Contribuição

Sinta-se à vontade para fazer um fork do projeto e contribuir com melhorias. Para contribuir:

1. Faça um fork do projeto.
2. Crie uma branch para a sua feature (`git checkout -b feature/nova-feature`).
3. Commit suas alterações (`git commit -m 'Adiciona nova feature'`).
4. Faça o push para a branch (`git push origin feature/nova-feature`).
5. Abra um Pull Request.
