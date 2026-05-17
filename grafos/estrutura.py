# grafos/estrutura.py
from abc import ABC, abstractmethod

class NoAdjacencia:
    """
    Classe para representar o 'pair' solicitado pela professora.
    Guarda o vértice de destino e o peso da aresta.
    """
    def __init__(self, destino, peso=1.0):
        self.destino = destino
        self.peso = peso


class Grafo(ABC):
    """
    Superclasse abstrata que define o 'contrato' de como qualquer
    grafo deve se comportar no nosso sistema.
    """
    def __init__(self, num_vertices, ponderado):
        self.num_vertices = num_vertices
        self.ponderado = ponderado
        self.num_arestas = 0

    @abstractmethod
    def inserir_aresta(self, u, v, peso):
        pass

    def info(self):
        print(f"n = {self.num_vertices}")
        print(f"m = {self.num_arestas}")
        d_medio = (2 * self.num_arestas) / self.num_vertices
        print(f"d_medio = {d_medio:.1f}")

    @abstractmethod
    def print_grafo(self):
        pass

    @abstractmethod
    def get_vizinhos(self, u):
        pass


class GrafoListaAdjacencia(Grafo):
    """
    Subclasse concreta utilizando Lista de Adjacência.
    """
    def __init__(self, num_vertices, ponderado):
        super().__init__(num_vertices, ponderado)
        self.lista_adj = {i: [] for i in range(1, num_vertices + 1)}

    def inserir_aresta(self, u, v, peso=1.0):
        """
        Insere a aresta instanciando a nova classe NoAdjacencia
        para respeitar a regra de Orientação a Objetos.
        """
        self.lista_adj[u].append(NoAdjacencia(v, peso))
        self.lista_adj[v].append(NoAdjacencia(u, peso))
        self.num_arestas += 1

    def print_grafo(self):
        """
        Imprime o grafo no formato especificado no trabalho.
        """
        for vertice in range(1, self.num_vertices + 1):
            vizinhos = self.lista_adj[vertice]
            
            if self.ponderado:
                # Acessa os atributos do objeto NoAdjacencia
                str_vizinhos = " ".join([f"{no.destino}({int(no.peso) if no.peso.is_integer() else no.peso})" for no in vizinhos])
            else:
                str_vizinhos = " ".join([str(no.destino) for no in vizinhos])
                
            print(f"{vertice} : {str_vizinhos}")

    def get_vizinhos(self, u):
        return self.lista_adj[u]