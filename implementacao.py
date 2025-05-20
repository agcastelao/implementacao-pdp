from multiprocessing import Process, Pipe
import math

# Dicionário de operações disponíveis:
# Escreva abaixo a função que você deseja criar, por exemplo, a de adição:
# def soma(n): return n + 10
def potencia(n):
    return n ** 2


OPERACOES = {
    "potencia": potencia,
    # "soma": soma,
}

# Processo consumidor
def consumidor(conn):
    print("[Consumidor] Aguardando dados do produtor...\n")
    while True:
        pacote = conn.recv()  # Espera um dicionário com 'numero' e 'operacao'

        if pacote == "FIM":
            print("[Consumidor] Encerrando processo.")
            break

        numero = pacote.get("numero")
        operacao = pacote.get("operacao")

        if operacao not in OPERACOES:
            print(f"[Consumidor] Operação '{operacao}' não reconhecida.")
            continue

        funcao = OPERACOES[operacao]
        resultado = funcao(numero)

        print(f"[Consumidor] Recebeu número {numero} com operação '{operacao}' → Resultado: {resultado}")

    conn.close()

# Processo produtor (main interativo)
if __name__ == '__main__':
    produtor_conn, consumidor_conn = Pipe()
    p = Process(target=consumidor, args=(consumidor_conn,))
    p.start()

    print("=== Sistema de Operações com Pipe ===")
    print("Digite 'sair' como operação para encerrar.")
    print("Operações disponíveis: ", list(OPERACOES.keys()))
    print()

    while True:
        entrada = input("Digite um número inteiro: ")
        if not entrada.isdigit():
            print("Entrada inválida. Digite apenas números inteiros.")
            continue

        numero = int(entrada)

        operacao = input("Escolha uma operação: ").lower()

        if operacao == 'sair':
            produtor_conn.send("FIM")
            break

        pacote = {
            "numero": numero,
            "operacao": operacao
        }

        print(f"[Produtor] Enviando número {numero} com operação '{operacao}'...\n")
        produtor_conn.send(pacote)

    produtor_conn.close()
    p.join()
