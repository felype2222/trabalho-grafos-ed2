# grafos/buscas.py
from abc import ABC, abstractmethod

class Busca(ABC):
    """
    Superclasse abstrata para todos os algoritmos de busca.
    Demonstra a Associação com a classe Grafo.
    """
    def __init__(self, grafo):
        # A busca "conhece" o grafo onde vai operar
        self.grafo = grafo

    @abstractmethod
    def executar(self, raiz):
        """Método principal que deverá ser implementado pelas subclasses."""
        pass


class BuscaProfundidade(Busca):
    """
    Implementação da Busca em Profundidade (DFS) usando recursão.
    """
    def __init__(self, grafo):
        super().__init__(grafo)
        # Estruturas para guardar o estado da busca
        self.visitados = set()
        self.pai = {}
        self.nivel = {}

    def executar(self, raiz):
        """
        Prepara as variáveis e inicia a busca a partir da raiz dada.
        """
        # Limpa as variáveis para garantir que não tenha lixo de uma busca anterior
        self.visitados.clear()
        
        # Inicializa todos os pais como 'x' (formato da professora)
        self.pai = {i: 'x' for i in range(1, self.grafo.num_vertices + 1)}
        
        # Inicializa todos os níveis como 0
        self.nivel = {i: 0 for i in range(1, self.grafo.num_vertices + 1)}

        # Dispara o método recursivo escondido
        self._dfs_recursivo(raiz, 0)

        # Imprime o resultado no exato formato da tabela da professora
        self._imprimir_resultado()

    def _dfs_recursivo(self, u, nivel_atual):
        """
        Método interno e recursivo que realmente faz a caminhada no grafo.
        """
        # Marca o vértice atual como visitado e anota seu nível
        self.visitados.add(u)
        self.nivel[u] = nivel_atual

        # Pega a lista de NoAdjacencia do vértice atual
        for no in self.grafo.get_vizinhos(u):
            v = no.destino # O vértice vizinho
            
            # Se o vizinho ainda não foi visitado, mergulhamos nele!
            if v not in self.visitados:
                # O pai do vizinho 'v' passa a ser quem o descobriu: 'u'
                self.pai[v] = u 
                
                # Chama a própria função passando o vizinho e aumentando o nível em 1
                self._dfs_recursivo(v, nivel_atual + 1)

    def _imprimir_resultado(self):
        """Imprime a árvore de busca gerada."""
        for v in range(1, self.grafo.num_vertices + 1):
            # Só imprime os vértices que foram alcançados pela busca
            if v in self.visitados:
                print(f"No {v}; Pai {self.pai[v]}; Level {self.nivel[v]};")