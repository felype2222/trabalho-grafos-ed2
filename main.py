"""
Arquivo Principal (Ponto de Entrada) - Sistema de Algoritmos em Grafos
Trabalho de Estrutura de Dados 2

Este arquivo é responsável por fazer a interface com o usuário (CLI - Command Line Interface).
Ele coordena a leitura inicial do arquivo de texto e exibe um menu interativo para que 
o usuário possa executar os algoritmos de Busca em Profundidade e Árvore Geradora Mínima.
"""

import sys
import os

# Importações dos módulos que criamos para manter a arquitetura Orientada a Objetos
from grafos.utils import LeitorArquivo
from grafos.buscas import BuscaProfundidade
from grafos.arvores_minimas import AGMPrim

def exibir_menu():
    """
    Exibe as opções do sistema na tela e captura a escolha do usuário.
    Retorna a string correspondente à opção digitada.
    """
    print("\n" + "="*30)
    print("       MENU DE GRAFOS")
    print("="*30)
    print("1. Info()  - Resumo do Grafo")
    print("2. Print() - Imprimir Adjacências")
    print("3. Busca() - Busca em Profundidade")
    print("4. MST()   - Árvore Geradora Mínima")
    print("0. Sair")
    print("="*30)
    return input("Escolha uma opção: ")

def main():
    """
    Função principal que orquestra o fluxo do programa.
    1. Solicita o arquivo de entrada.
    2. Delega a leitura para a classe utilitária (LeitorArquivo).
    3. Mantém o usuário em um loop de menu até que ele decida sair.
    """
    print("Bem-vindo ao Sistema de Grafos!")
    
    # Captura o caminho do arquivo fornecido pelo usuário (ex: grafo_teste.txt)
    caminho_arquivo = input("Digite o caminho do arquivo do grafo (ex: grafo.txt): ")
    
    # Bloco de tratamento de erros (try-except) para garantir que o programa não 
    # feche abruptamente se o usuário digitar o nome do arquivo errado.
    try:
        # A classe LeitorArquivo lê o txt e devolve um objeto GrafoListaAdjacencia pronto
        grafo = LeitorArquivo.ler_grafo(caminho_arquivo)
        print("\n[SUCESSO] Grafo carregado com sucesso na memória!")
    except FileNotFoundError as e:
        print(f"\n[ERRO] {e}")
        print("Dica: Verifique se o nome do arquivo está correto e se ele está na mesma pasta.")
        sys.exit(1) # Encerra o programa com código de erro 1
    except Exception as e:
        print(f"\n[ERRO INESPERADO] {e}")
        sys.exit(1)

    # Loop infinito que mantém o menu ativo. Só é quebrado quando a opção for '0' (break).
    while True:
        opcao = exibir_menu()

        if opcao == '1':
            # Chama o método info() herdado da superclasse Grafo
            print("\n--- Informações do Grafo ---")
            grafo.info()
            
        elif opcao == '2':
            # Chama o método print_grafo() implementado na subclasse GrafoListaAdjacencia
            print("\n--- Representação do Grafo ---")
            grafo.print_grafo()
            
        elif opcao == '3':
            # Executa a Busca em Profundidade (DFS)
            print("\n--- Busca em Profundidade ---")
            try:
                # Pede a raiz e tenta converter para inteiro. Se o usuário digitar
                # uma letra, o ValueError é capturado para não quebrar o programa.
                raiz = int(input("Digite o vértice raiz para iniciar a busca: "))
                
                # Instancia a classe de busca passando o grafo (Associação/Injeção de Dependência)
                busca = BuscaProfundidade(grafo)
                busca.executar(raiz)
            except ValueError:
                print("[ERRO] Por favor, digite um número inteiro válido.")
            
        elif opcao == '4':
            # Executa o algoritmo de Prim para encontrar a Árvore Geradora Mínima (MST)
            print("\n--- Árvore Geradora Mínima (Prim) ---")
            
            # Instancia a classe passando o grafo atual na memória
            mst = AGMPrim(grafo)
            # Aciona o cálculo que internamente usa a Fila de Prioridade (Min-Heap)
            mst.calcular()
            
        elif opcao == '0':
            # Quebra o loop 'while', finalizando o script com sucesso
            print("\nEncerrando o programa. Até logo!")
            break
            
        else:
            # Tratamento caso o usuário digite um número fora das opções
            print("\n[AVISO] Opção inválida. Tente novamente.")

# O padrão idiomático do Python que garante que a função main() só será
# executada se este arquivo for rodado diretamente no terminal (e não importado)
if __name__ == "__main__":
    main()