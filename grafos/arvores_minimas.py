"""
Módulo de Árvores Geradoras Mínimas (MST - Minimum Spanning Tree)
Trabalho de Estrutura de Dados 2

Este arquivo contém a arquitetura para o cálculo da Árvore Geradora Mínima.
Utilizamos Orientação a Objetos com uma superclasse abstrata para definir o 
contrato e uma subclasse concreta que implementa o Algoritmo de Prim.
"""

import heapq
from abc import ABC, abstractmethod

class ArvoreGeradoraMinima(ABC):
    """
    Superclasse abstrata que define a interface para qualquer algoritmo de MST.
    
    Demonstra o conceito de Associação (ou Injeção de Dependência): 
    A classe não constrói o grafo, ela recebe um grafo já montado por parâmetro,
    permitindo que o algoritmo funcione independentemente de como o grafo foi lido.
    """
    def __init__(self, grafo):
        self.grafo = grafo

    @abstractmethod
    def calcular(self):
        """Método obrigatório que as subclasses devem implementar."""
        pass


class AGMPrim(ArvoreGeradoraMinima):
    """
    Subclasse concreta que implementa o Algoritmo de Prim.
    
    O Algoritmo de Prim constrói a MST de forma gulosa (greedy). Ele começa em um 
    vértice arbitrário e, a cada passo, escolhe a aresta mais barata que conecta 
    um vértice já visitado a um vértice não visitado, até que todos os nós estejam conectados.
    """
    def __init__(self, grafo):
        super().__init__(grafo)
        # Variáveis de estado para guardar o resultado final
        self.custo_total = 0.0
        self.arestas_mst = []

    def calcular(self):
        """
        Executa o Algoritmo de Prim utilizando uma Fila de Prioridade (Min-Heap).
        O uso do Heap otimiza a busca pela aresta mais barata, resultando em
        uma complexidade de tempo de O(m log n).
        """
        num_v = self.grafo.num_vertices
        
        # Conjunto (Set) para registrar os vértices já incluídos na MST.
        # A busca em sets no Python é O(1), o que é ideal para verificar ciclos.
        visitados = set()
        
        # A Fila de prioridade (Min-Heap) guardará as arestas descobertas.
        # Guardaremos tuplas no formato: (peso, vértice_origem, vértice_destino).
        # O heapq do Python sempre ordenará a lista pelo primeiro elemento da tupla (o peso).
        min_heap = []
        
        # Reinicializa as variáveis de resultado caso a função seja chamada mais de uma vez
        self.custo_total = 0.0
        self.arestas_mst.clear()

        # O algoritmo pode começar de qualquer vértice. Escolhemos arbitrariamente o 1.
        vertice_inicial = 1
        visitados.add(vertice_inicial)

        # Passo inicial: Coloca todas as arestas vizinhas da raiz na fila de prioridade
        for no in self.grafo.get_vizinhos(vertice_inicial):
            heapq.heappush(min_heap, (no.peso, vertice_inicial, no.destino))

        # O laço roda até que todos os vértices estejam na árvore ou não existam mais arestas alcançáveis.
        # len(visitados) < num_v garante que paramos assim que todos os nós forem conectados.
        while min_heap and len(visitados) < num_v:
            
            # Extrai a aresta mais barata (menor peso) disponível no momento
            peso, u, v = heapq.heappop(min_heap)

            # Prevenção de Ciclos: Se o destino 'v' já está na árvore (visitados),
            # significa que adicionar esta aresta criaria um ciclo fechado.
            # Portanto, ignoramos e pulamos para a próxima.
            if v in visitados:
                continue

            # Se 'v' ainda não foi visitado, é seguro adicioná-lo à nossa MST.
            visitados.add(v)
            self.custo_total += peso
            self.arestas_mst.append((u, v, peso))

            # Expansão: Agora que 'v' faz parte da árvore, todas as arestas que saem
            # dele para nós não visitados tornam-se opções válidas. Adicionamos todas ao Heap.
            for no in self.grafo.get_vizinhos(v):
                if no.destino not in visitados:
                    heapq.heappush(min_heap, (no.peso, v, no.destino))

        # Ao final do cálculo, formata e imprime os resultados na tela
        self._imprimir_resultado()

    def _imprimir_resultado(self):
        """
        Método auxiliar para imprimir a MST no formato exato exigido pela especificação.
        Trata a estética removendo casas decimais caso os pesos sejam números inteiros puros.
        """
        # Se o peso total for 12.0, o is_integer() será True e converterá para 12 (int).
        peso_total_fmt = f"{int(self.custo_total)}" if self.custo_total.is_integer() else f"{self.custo_total}"
        print(f"Peso total : {peso_total_fmt}")
        
        # Itera sobre a lista de arestas finais e imprime respeitando o modelo do trabalho
        for u, v, peso in self.arestas_mst:
            peso_aresta_fmt = f"{int(peso)}" if peso.is_integer() else f"{peso}"
            print(f"Aresta {u}-{v}; peso {peso_aresta_fmt}")