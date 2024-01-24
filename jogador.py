import grafo

# Definição da classe player:
# Um nome
# Um algortimo escolhido pelo utilizador
# Um grafo criado de acordo com o algoritmo escolhido
# Um custo calculado pelo algoritmo escolhido numa travessia individual (Singleplayer) 
# Um caminho calculado pelo algoritmo escolhido numa travessia individual (Singleplayer)
class Player:
    ########################
    # Construtor da classe #
    ########################
    def __init__(self, nome: str, algoritmo: int, grafo: grafo.Graph, custo: int, caminho = list):
        self.name = nome
        self.algorithm = algoritmo
        self.graph = grafo
        self.cost = custo
        self.path = caminho

    ########################################
    # Escrever o jogador no formato String #
    ########################################
    def __str__(self):
        str_path = ""
        # Imprime apenas os tuplos que correspondem às coordenadas, 
        # ignorando aqueles que correspondem às velocidades
        for elem in self.path:
            str_path += str(elem[0]) + " "
        # A lista n_algorithm apenas nos ajuda a imprimir textualmente o nome do algoritmo
        # de cada jogador em vez do número pelo qual identificamos o seu algoritmo
        n_algorithm = list()
        n_algorithm.append("A*")
        n_algorithm.append("Greedy")
        n_algorithm.append("BFS")
        n_algorithm.append("DFS")
        out = "Nome: " + self.name + "\n" + "Algoritmo: " + str(n_algorithm[self.algorithm]) + "\n" + "Caminho: " + str_path + "\n" + "Custo: " + str(self.cost) + "\n"        
        #out = "Nome: " + self.name + "\n" + "Algoritmo: " + str(self.algorithm) + "\n" + "Caminho: " + str(self.path) + "\n" + "Custo: " + str(self.cost) + "\n"
        return out
