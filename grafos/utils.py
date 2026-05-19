"""
Módulo Utilitário de I/O (Entrada/Saída)
Trabalho de Estrutura de Dados 2

Este arquivo é responsável por isolar a lógica de leitura de arquivos em disco.
Ele atua como uma "Fábrica" (Factory Pattern), lendo o arquivo de texto bruto,
interpretando o formato padronizado e devolvendo um objeto Grafo instanciado e 
pronto para uso em memória.
"""

import os
from grafos.estrutura import GrafoListaAdjacencia

class LeitorArquivo:
    """
    Classe utilitária para leitura e sanitização de arquivos.
    
    Não armazena estado interno, por isso seus métodos podem ser chamados 
    diretamente através da classe (métodos estáticos), sem a necessidade de 
    instanciar um objeto LeitorArquivo.
    """
    
    @staticmethod
    def ler_grafo(caminho_arquivo):
        """
        Lê um arquivo .txt e constrói o grafo correspondente.
        
        O arquivo deve seguir estritamente o contrato:
        - Linha 1: [num_vertices] [0 para não-ponderado, 1 para ponderado]
        - Linha N: [vertice_u] [vertice_v] [peso_opcional] # comentários
        
        Retorna:
            GrafoListaAdjacencia: Objeto instanciado com os dados lidos do arquivo.
            
        Exceções:
            FileNotFoundError: Se o arquivo especificado não existir no caminho.
            ValueError: Se o arquivo estiver completamente vazio.
        """
        # 1. Validação de pré-condição: garante que o arquivo existe antes de tentar abrir.
        # Isso evita que o programa quebre com erros genéricos do sistema operacional.
        if not os.path.exists(caminho_arquivo):
            raise FileNotFoundError(f"Erro: O arquivo '{caminho_arquivo}' não foi encontrado.")

        # 2. Abertura segura do arquivo utilizando o context manager 'with'.
        # O 'with' garante que o arquivo será fechado corretamente e a memória liberada
        # mesmo que ocorra um erro durante a leitura.
        with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
            linhas = arquivo.readlines()

        # 3. Limpeza dos dados lidos (Sanitização)
        # Utiliza list comprehension para remover espaços em branco do início/fim das linhas 
        # e descarta linhas que sejam apenas espaços ou quebras de linha puras.
        linhas = [linha.strip() for linha in linhas if linha.strip()]

        if not linhas:
            raise ValueError("Erro: O arquivo está vazio.")

        # 4. Processamento do Cabeçalho (Linha 1 do arquivo)
        # O split() divide a string por espaços em branco de forma inteligente.
        # Ex: "5 0 #comentário" se transforma na lista ["5", "0", "#comentário"]
        header = linhas[0].split()
        num_vertices = int(header[0])
        
        # Avaliação Booleana: O número 1 vira True (ponderado), o 0 vira False (não ponderado)
        ponderado = int(header[1]) == 1

        # Instanciação: Cria o objeto da subclasse concreta de Grafo.
        # A vantagem da arquitetura é que, se o trabalho exigisse Matriz de Adjacência no futuro,
        # bastaria trocar a classe importada e instanciada aqui, sem mexer no resto do programa.
        grafo = GrafoListaAdjacencia(num_vertices, ponderado)

        # 5. Processamento das Arestas (Laço iterando a partir da Linha 2 até o final)
        for linha in linhas[1:]:
            dados = linha.split()
            
            # Tratamento de Comentários: Se a linha for apenas um comentário (inicia com #)
            # ou estiver vazia após o split, o comando 'continue' pula para a próxima iteração do laço.
            if not dados or dados[0].startswith('#'):
                continue

            # Mapeamento dos vértices que formam a aresta
            u = int(dados[0])
            v = int(dados[1])

            if ponderado:
                # Em grafos ponderados, o terceiro argumento da lista é obrigatoriamente o peso
                peso = float(dados[2])
                grafo.inserir_aresta(u, v, peso)
            else:
                # Em grafos não-ponderados, a classe GrafoListaAdjacencia 
                # assumirá automaticamente o peso padrão definido em seu método (1.0).
                grafo.inserir_aresta(u, v)

        return grafo