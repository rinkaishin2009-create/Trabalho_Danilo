from datetime import datetime, timedelta

# Configurações do sistema / Regras de negócio
LIMITE_LIVROS_POR_USUARIO = 2
VALOR_MULTA_DIARIA = 2.50  # Valor por dia de atraso

# Estrutura de dados inicial do acervo
acervo = [
    {
        'id': 1,
        'titulo': 'Python Básico',
        'disponivel': False,
        'emprestado_para': None,
        'data_devolucao_prevista': None
    },
    {
        'id': 2,
        'titulo': 'Estruturas de Dados em Python',
        'disponivel': True,
        'emprestado_para': None,
        'data_devolucao_prevista': None
    },
    {
        'id': 3,
        'titulo': 'Engenharia de Software',
        'disponivel': True,
        'emprestado_para': None,
        'data_devolucao_prevista': None
    }
]

def consultar_acervo():
    """Lista todos os títulos e a situação dos exemplares."""
    print("\n--- ACERVO DA BIBLIOTECA ---")
    for livro in acervo:
        status = "Disponível" if livro['disponivel'] else f"Emprestado para {livro['emprestado_para']}"
        print(f"ID: {livro['id']} | Título: {livro['titulo']} | Status: {status}")
    print("-" * 30)

def contar_livros_emprestados(usuario):
    """Retorna a quantidade de livros atualmente com o usuário."""
    return sum(1 for livro in acervo if livro['emprestado_para'] == usuario)

def emprestar_livro(id_livro, usuario, dias_emprestimo=7):
    """Verifica a disponibilidade do exemplar e o limite do usuário antes de realizar o empréstimo."""
    livro = next((l for l in acervo if l['id'] == id_livro), None)
    
    if not livro:
        print("Erro: Livro não encontrado.")
        return

    # Regra 1: Permitir empréstimo somente de exemplar disponível
    if not livro['disponivel']:
        print(f"Erro: O livro '{livro['titulo']}' já está emprestado!")
        return

    # Regra 2: Controlar o limite de livros por usuário
    if contar_livros_emprestados(usuario) >= LIMITE_LIVROS_POR_USUARIO:
        print(f"Erro: O usuário '{usuario}' atingiu o limite de {LIMITE_LIVROS_POR_USUARIO} livros emprestados.")
        return

    # Realizar empréstimo e atualizar status
    livro['disponivel'] = False
    livro['emprestado_para'] = usuario
    livro['data_devolucao_prevista'] = datetime.now() + timedelta(days=dias_emprestimo)
    print(f"Sucesso: O livro '{livro['titulo']}' foi emprestado para '{usuario}'. (Devolução prevista: {livro['data_devolucao_prevista'].strftime('%d/%m/%Y')})")

def devolver_livro(id_livro, dias_de_atraso=0):
    """Altera o status do exemplar e calcula multa diária em caso de atraso."""
    livro = next((l for l in acervo if l['id'] == id_livro), None)

    if not livro:
        print("Erro: Livro não encontrado.")
        return

    if livro['disponivel']:
        print(f"Erro: O livro '{livro['titulo']}' não consta como emprestado.")
        return

    # Calcular multa diária para devoluções atrasadas
    multa = 0.0
    if dias_de_atraso > 0:
        multa = dias_de_atraso * VALOR_MULTA_DIARIA
        print(f"Atenção: Livro devolvido com {dias_de_atraso} dia(s) de atraso. Multa a pagar: R$ {multa:.2f}")
    else:
        print("Devolução realizada dentro do prazo. Sem multa.")

    # Atualizar status do exemplar
    livro['disponivel'] = True
    livro['emprestado_para'] = None
    livro['data_devolucao_prevista'] = None
    print(f"Sucesso: O livro '{livro['titulo']}' foi devolvido e está novamente disponível.")

def menu():
    """Menu interativo do sistema."""
    while True:
        print("\n--- MENU ---")
        print("1 - Consultar acervo")
        print("2 - Emprestar livro")
        print("3 - Devolver livro")
        print("0 - Sair")
        
        opcao = input("Escolha uma opção: ").strip()

        if opcao == '1':
            consultar_acervo()
        elif opcao == '2':
            try:
                id_livro = int(input("ID do livro: "))
                usuario = input("Nome do usuário: ").strip()
                emprestar_livro(id_livro, usuario)
            except ValueError:
                print("Entrada inválida. Digite um número de ID válido.")
        elif opcao == '3':
            try:
                id_livro = int(input("ID do livro: "))
                atraso = int(input("Dias de atraso na devolução (0 para no prazo): "))
                devolver_livro(id_livro, dias_de_atraso=atraso)
            except ValueError:
                print("Entrada inválida. Digite números válidos para ID e atraso.")
        elif opcao == '0':
            print("Encerrando o programa...")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()