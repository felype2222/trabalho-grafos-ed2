# main.py
import sys
import os
from grafos.utils import LeitorArquivo
from grafos.buscas import BuscaProfundidade
from grafos.arvores_minimas import AGMPrim

def exibir_menu():
    """Imprime as opções do menu na tela."""
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
    print("Bem-vindo ao Sistema de Grafos!")
    
    # Pede o caminho do arquivo de texto para o usuário
    caminho_arquivo = input("Digite o caminho do arquivo do grafo (ex: grafo.txt): ")
    
    # Tenta ler o arquivo e instanciar o grafo
    try:
        grafo = LeitorArquivo.ler_grafo(caminho_arquivo)
        print("\n[SUCESSO] Grafo carregado com sucesso na memória!")
    except FileNotFoundError as e:
        print(f"\n[ERRO] {e}")
        print("Dica: Verifique se o nome do arquivo está correto e se ele está na mesma pasta.")
        sys.exit(1) # Sai do programa com erro
    except Exception as e:
        print(f"\n[ERRO INESPERADO] {e}")
        sys.exit(1)

    # Loop infinito do Menu de opções
    while True:
        opcao = exibir_menu()

        if opcao == '1':
            print("\n--- Informações do Grafo ---")
            grafo.info()
            
        elif opcao == '2':
            print("\n--- Representação do Grafo ---")
            grafo.print_grafo()
            
        elif opcao == '3':
            print("\n--- Busca em Profundidade ---")
            try:
                raiz = int(input("Digite o vértice raiz para iniciar a busca: "))
                busca = BuscaProfundidade(grafo)
                busca.executar(raiz)
            except ValueError:
                print("[ERRO] Por favor, digite um número inteiro válido.")
            
        elif opcao == '4':
            print("\n--- Árvore Geradora Mínima (Prim) ---")
            mst = AGMPrim(grafo)
            mst.calcular()
            
        elif opcao == '0':
            print("\nEncerrando o programa. Até logo!")
            break
            
        else:
            print("\n[AVISO] Opção inválida. Tente novamente.")

# Garante que a função main() só rode se este arquivo for executado diretamente
if __name__ == "__main__":
    main()