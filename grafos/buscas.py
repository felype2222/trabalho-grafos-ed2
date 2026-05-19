"""
Módulo de Algoritmos de Busca em Grafos
Trabalho de Estrutura de Dados 2

Este arquivo contém a arquitetura para os algoritmos de travessia (busca) no grafo.
A estrutura utiliza Orientação a Objetos para garantir que diferentes tipos de busca
(como Profundidade ou Largura) possam ser implementados seguindo o mesmo contrato.
"""

from abc import ABC, abstractmethod

class Busca(ABC):
    """
    Superclasse abstrata que define a interface padrão para qualquer algoritmo de busca.
    
    Implementa o conceito de Associação: a classe de busca não possui os dados do grafo,
    mas recebe uma instância de Grafo no construtor para poder consultá-lo. Isso
    desacopla a lógica de busca da lógica de armazenamento de dados.
    """
    def __init__(self, grafo):
        # A busca "conhece" o grafo onde vai operar
        self.grafo = grafo

    @abstractmethod
    def executar(self, raiz):
        """Método obrigatório para iniciar a busca a partir de um vértice raiz."""
        pass


class BuscaProfundidade(Busca):
    """
    Subclasse concreta que implementa a Busca em Profundidade (DFS - Depth-First Search).
    
    A DFS explora o grafo indo o mais "fundo" possível em cada ramo antes de retroceder 
    (backtracking). Essa implementação utiliza chamadas recursivas, aproveitando a 
    Pilha de Execução (Call Stack) do próprio Python para gerenciar o retrocesso.
    """
    def __init__(self, grafo):
        super().__init__(grafo)
        # Conjunto para buscas em tempo O(1) dos nós já visitados
        self.visitados = set()
        # Dicionário para rastrear a árvore gerada (quem descobriu quem)
        self.pai = {}
        # Dicionário para rastrear a distância (em arestas) da raiz até o nó
        self.nivel = {}

    def executar(self, raiz):
        """
        Método de preparação. Inicializa o estado do algoritmo e dispara a recursão.
        """
        # Limpa as estruturas para garantir que buscas consecutivas não interfiram umas nas outras
        self.visitados.clear()
        
        # Inicializa o array de pais com 'x' (indicando ausência de pai, conforme a especificação)
        self.pai = {i: 'x' for i in range(1, self.grafo.num_vertices + 1)}
        
        # Inicializa todos os níveis com 0
        self.nivel = {i: 0 for i in range(1, self.grafo.num_vertices + 1)}

        # Dispara o método recursivo privado começando pela raiz no nível 0
        self._dfs_recursivo(raiz, 0)

        # Após a recursão terminar, a árvore estará montada. Imprimimos o resultado.
        self._imprimir_resultado()

    def _dfs_recursivo(self, u, nivel_atual):
        """
        Lógica central do algoritmo DFS.
        
        Complexidade de Tempo: O(V + E), onde V é o número de vértices e E o número de arestas,
        pois como usamos uma Lista de Adjacência, visitamos cada vértice e exploramos 
        cada aresta exatamente uma vez.
        """
        # 1. Marca o vértice atual 'u' como visitado para evitar loops infinitos
        self.visitados.add(u)
        
        # 2. Registra o nível em que este vértice foi encontrado
        self.nivel[u] = nivel_atual

        # 3. Explora todos os vizinhos conectados ao vértice 'u'
        for no in self.grafo.get_vizinhos(u):
            v = no.destino # O vértice vizinho de destino
            
            # Se o vizinho 'v' ainda não foi descoberto, nós "mergulhamos" nele
            if v not in self.visitados:
                # O pai do vizinho 'v' passa a ser o vértice atual 'u' que o encontrou
                self.pai[v] = u 
                
                # Chamada recursiva: movemos para o vizinho 'v' e descemos um nível na árvore
                self._dfs_recursivo(v, nivel_atual + 1)

    def _imprimir_resultado(self):
        """
        Método auxiliar para imprimir a árvore de busca no formato exato 
        exigido pela especificação do trabalho.
        """
        # Itera sobre todos os vértices possíveis do grafo
        for v in range(1, self.grafo.num_vertices + 1):
            # Imprime apenas os vértices que foram alcançados pela árvore de busca atual
            if v in self.visitados:
                print(f"No {v}; Pai {self.pai[v]}; Level {self.nivel[v]};")