# grafos/utils.py
import os
from grafos.estrutura import GrafoListaAdjacencia

class LeitorArquivo:
    """
    Classe utilitária responsável por ler os arquivos .txt e 
    instanciar os objetos do tipo Grafo.
    """
    
    @staticmethod
    def ler_grafo(caminho_arquivo):
        # 1. Verifica se o arquivo realmente existe para evitar que o programa quebre
        if not os.path.exists(caminho_arquivo):
            raise FileNotFoundError(f"Erro: O arquivo '{caminho_arquivo}' não foi encontrado.")

        # 2. Abre o arquivo em modo de leitura ('r')
        with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
            linhas = arquivo.readlines()

        # Remove linhas que sejam completamente vazias (só espaços ou quebras de linha)
        linhas = [linha.strip() for linha in linhas if linha.strip()]

        if not linhas:
            raise ValueError("Erro: O arquivo está vazio.")

        # 3. Processamento do Cabeçalho (Primeira Linha)
        # O split() divide a linha pelos espaços. Ex: "5 0 #coment" -> ["5", "0", "#coment"]
        header = linhas[0].split()
        num_vertices = int(header[0])
        
        # Transforma o 1 em True (ponderado) e o 0 em False (não ponderado)
        ponderado = int(header[1]) == 1

        # Instancia a nossa classe concreta baseada na leitura
        grafo = GrafoListaAdjacencia(num_vertices, ponderado)

        # 4. Processamento das Arestas (Restante das linhas)
        for linha in linhas[1:]:
            dados = linha.split()
            
            # Se a linha for apenas um comentário (começar com #), nós ignoramos
            if not dados or dados[0].startswith('#'):
                continue

            u = int(dados[0])
            v = int(dados[1])

            if ponderado:
                # Se for ponderado, obrigatoriamente pegamos o terceiro item
                peso = float(dados[2])
                grafo.inserir_aresta(u, v, peso)
            else:
                # Se não for ponderado, passamos apenas os vértices. 
                # A nossa classe automaticamente colocará o peso padrão 1.0.
                grafo.inserir_aresta(u, v)

        return grafo