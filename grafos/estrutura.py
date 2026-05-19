"""
Módulo de Estruturas de Dados para Grafos
Trabalho de Estrutura de Dados 2

Este arquivo contém a modelagem orientada a objetos que representa o grafo na memória.
A arquitetura utiliza uma classe abstrata (Interface) para definir o contrato base e
uma subclasse concreta que implementa o armazenamento via Lista de Adjacência.
"""

from abc import ABC, abstractmethod

class NoAdjacencia:
    """
    Classe auxiliar para representar a ligação entre vértices (o 'pair').
    Garante o encapsulamento dos dados de uma aresta, armazenando o vértice 
    de destino e o peso associado a essa conexão.
    """
    def __init__(self, destino, peso=1.0):
        self.destino = destino
        self.peso = peso


class Grafo(ABC):
    """
    Superclasse abstrata que define o 'contrato' (Interface) para qualquer grafo.
    
    Independentemente de como o grafo armazene seus dados internamente (Lista, Matriz, etc.),
    ele obrigatoriamente terá as propriedades e métodos definidos aqui.
    """
    def __init__(self, num_vertices, ponderado):
        # Quantidade total de vértices no grafo
        self.num_vertices = num_vertices
        # Flag booleana indicando se as arestas possuem pesos diferentes de 1
        self.ponderado = ponderado
        # Contador de arestas (inicia em 0 e cresce conforme a inserção)
        self.num_arestas = 0

    @abstractmethod
    def inserir_aresta(self, u, v, peso):
        """Método abstrato: Obriga as subclasses a implementarem a lógica de inserção."""
        pass

    def info(self):
        """
        Calcula e imprime as estatísticas básicas do grafo.
        Como essa lógica matemática é universal para grafos não direcionados,
        ela já é implementada na superclasse para evitar repetição de código.
        """
        print(f"n = {self.num_vertices}")
        print(f"m = {self.num_arestas}")
        
        # Fórmula do grau médio para grafos não direcionados: (2 * número de arestas) / número de vértices
        d_medio = (2 * self.num_arestas) / self.num_vertices
        print(f"d_medio = {d_medio:.1f}")

    @abstractmethod
    def print_grafo(self):
        """Método abstrato: Obriga as subclasses a implementarem a impressão visual do grafo."""
        pass

    @abstractmethod
    def get_vizinhos(self, u):
        """Método abstrato: Obriga as subclasses a retornarem os vizinhos de um vértice."""
        pass


class GrafoListaAdjacencia(Grafo):
    """
    Subclasse concreta que herda de Grafo e implementa o armazenamento
    dos dados utilizando uma Lista de Adjacência.
    """
    def __init__(self, num_vertices, ponderado):
        # Inicializa as variáveis base chamando o construtor da superclasse
        super().__init__(num_vertices, ponderado)
        
        # Utiliza um dicionário (Map) do Python para representar a lista de adjacência.
        # A chave é o vértice (de 1 a N) e o valor é uma lista de objetos NoAdjacencia.
        # O uso de dicionário evita problemas de índice (já que os vértices começam em 1 e não em 0).
        self.lista_adj = {i: [] for i in range(1, num_vertices + 1)}

    def inserir_aresta(self, u, v, peso=1.0):
        """
        Insere uma aresta não direcionada no grafo instanciando objetos NoAdjacencia.
        """
        # Como o grafo é não direcionado (mão dupla), precisamos adicionar a ida e a volta
        self.lista_adj[u].append(NoAdjacencia(v, peso))
        self.lista_adj[v].append(NoAdjacencia(u, peso))
        
        # Incrementa o contador total de arestas da superclasse
        self.num_arestas += 1

    def print_grafo(self):
        """
        Imprime a lista de adjacência formatada conforme os requisitos do trabalho.
        """
        # Percorre todos os vértices possíveis (1 até N)
        for vertice in range(1, self.num_vertices + 1):
            vizinhos = self.lista_adj[vertice]
            
            if self.ponderado:
                # Se ponderado, formata exibindo destino(peso). Ex: 2(4) 3(2)
                # O tratamento int(no.peso) if no.peso.is_integer() remove o '.0' de pesos inteiros
                str_vizinhos = " ".join([f"{no.destino}({int(no.peso) if no.peso.is_integer() else no.peso})" for no in vizinhos])
            else:
                # Se não ponderado, exibe apenas os vértices de destino. Ex: 2 3
                str_vizinhos = " ".join([str(no.destino) for no in vizinhos])
                
            print(f"{vertice} : {str_vizinhos}")

    def get_vizinhos(self, u):
        """
        Retorna a lista completa de vizinhos (objetos NoAdjacencia) de um vértice específico.
        Essencial para a execução dos algoritmos de Busca e Árvore Geradora Mínima.
        """
        return self.lista_adj[u]