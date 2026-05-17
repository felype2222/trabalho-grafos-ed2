# grafos/arvores_minimas.py
import heapq
from abc import ABC, abstractmethod

class ArvoreGeradoraMinima(ABC):
    """
    Superclasse abstrata para algoritmos de Árvore Geradora Mínima.
    Demonstra a Associação com a classe Grafo.
    """
    def __init__(self, grafo):
        self.grafo = grafo

    @abstractmethod
    def calcular(self):
        """Método principal a ser implementado pelas subclasses."""
        pass


class AGMPrim(ArvoreGeradoraMinima):
    """
    Subclasse concreta que implementa o Algoritmo de Prim 
    utilizando uma Fila de Prioridade (Min-Heap).
    """
    def __init__(self, grafo):
        super().__init__(grafo)
        self.custo_total = 0.0
        self.arestas_mst = []

    def calcular(self):
        """
        Executa o Algoritmo de Prim para encontrar a MST do grafo.
        """
        num_v = self.grafo.num_vertices
        visitados = set()
        
        # Fila de prioridade (Min-Heap) para buscar sempre a aresta mais barata disponível.
        # Guardará tuplas no formato: (peso, origem, destino)
        min_heap = []
        
        # Reinicializa as variáveis de resultado
        self.custo_total = 0.0
        self.arestas_mst.clear()

        # Começamos arbitrariamente pelo vértice 1
        vertice_inicial = 1
        visitados.add(vertice_inicial)

        # Coloca todas as arestas que saem do vértice inicial na fila de prioridade
        for no in self.grafo.get_vizinhos(vertice_inicial):
            heapq.heappush(min_heap, (no.peso, vertice_inicial, no.destino))

        # O algoritmo roda até conectar todos os vértices ou a fila esvaziar
        while min_heap and len(visitados) < num_v:
            # Extrai a aresta com o menor peso da fila
            peso, u, v = heapq.heappop(min_heap)

            # Se o vértice de destino 'v' já foi visitado, ignoramos para evitar ciclos
            if v in visitados:
                continue

            # Caso contrário, expandimos a nossa árvore para incluir o vértice 'v'
            visitados.add(v)
            self.custo_total += peso
            self.arestas_mst.append((u, v, peso))

            # Adiciona as novas arestas do vértice recém-visitado 'v' na fila
            for no in self.grafo.get_vizinhos(v):
                if no.destino not in visitados:
                    heapq.heappush(min_heap, (no.peso, v, no.destino))

        # Imprime o resultado final no formato exigido pela especificação
        self._imprimir_resultado()

    def _imprimir_resultado(self):
        """
        Formata e imprime a saída conforme os requisitos do trabalho.
        """
        # Remove casas decimais inúteis se o peso for inteiro (ex: 12.0 vira 12)
        peso_total_fmt = f"{int(self.custo_total)}" if self.custo_total.is_integer() else f"{self.custo_total}"
        print(f"Peso total : {peso_total_fmt}")
        
        # Lista as arestas selecionadas na ordem em que foram descobertas
        for u, v, peso in self.arestas_mst:
            peso_aresta_fmt = f"{int(peso)}" if peso.is_integer() else f"{peso}"
            print(f"Aresta {u}-{v}; peso {peso_aresta_fmt}")