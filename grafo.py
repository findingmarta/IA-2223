from queue import Queue
import math

# Definição da classe grafo:
# Um nodo inicial start
# Uma lista com as coordenadas dos nodos finais
# Uma matriz com o circuito
# Uma lista de tuplos que representa as velocidades que podem ser associadas a um nodo 
# Um dicionário: nome_nodo -> lista de tuplos (nome_nodo, vel_nodo, peso)
# A largura do circuito
# A altura do circuito 
class Graph:
    ########################
    # Construtor da classe #
    ########################
    def __init__(self, partida, fim, circuito, tipo_procura):
        self.start = partida
        self.end = fim
        self.circuito = circuito
        self.possibilidades = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,0),(0,1),(1,-1),(1,0),(1,1)]
        self.grafo = self.gera_Grafo(partida,(0,0),tipo_procura)
        self.largura = len(circuito[0])
        self.altura = len(circuito)


    ######################################
    # Escrever o grafo no formato String #
    ######################################
    def __str__(self):
        out = ""
        for key in self.grafo.keys():
            out = out + "node " + str(key) + ": " + str(self.grafo[key]) + "\n"
        return out


    #######################################
    #             Criar grafo             #
    #######################################
    def gera_Grafo(self, coord, vel_inicial, tipo_procura: int):
        # porVisitar é a variavel que guarda numa lista de tuplos as coordenadas e a velocidade de todas as posiçoes que ainda nao foram visitadas
        porVisitar = [(coord, vel_inicial)]
        grafo = {}
        while porVisitar != []:
            # Enquanto existirem peças por visitar fazemos pop de uma peça de cada vez
            coordenadas, vel = porVisitar.pop(0)
            if coordenadas not in grafo.keys():
                # Se para uma certa peça esta não constar nas peças já passadas (grafo) então adicionamos 
                # a mesma sabendo previamente que a partir desta teremos um conjunto de outras para procurar
                grafo[coordenadas] = set()
            # Aqui consideram-se todas as aceleracoes permitidas na horizontal e na vertical
            for possibilidade in self.possibilidades:
                if tipo_procura in [2,3]:
                    # A próxima posiçã e a próxima velocidade são calculadas tendo em conta uma aceleração (0,0)
                    proxPos, proxVel = self.nao_informada(coordenadas, possibilidade)            
                else:
                    # A próxima posiçã e a próxima velocidade são calculadas tendo em conta uma aceleração que varia
                    proxPos, proxVel = self.informada(coordenadas, vel, possibilidade)
                if proxPos not in grafo.keys():
                    if self.validaNodo(coordenadas[0], coordenadas[1], proxPos[0], proxPos[1]):
                        # Se o nodo filho (proxPos) não foi ainda visitado e não é uma parede adiciona-se ao conjunto dos filhos do nodo atual com peso de 1 unidade
                        grafo[coordenadas].add((proxPos, proxVel, 1))
                        # se o filho ainda não foi visitado é adicionado à lista para se visitar posteriormente
                        if (proxPos,proxVel) not in porVisitar:
                            porVisitar.append((proxPos, proxVel))
                    else:
                        # Se o nodo é uma parede adicionamos ao conjunto de nodos filhos para visitar posteriormente com peso de 25 unidades
                        grafo[coordenadas].add((proxPos, proxVel, 25))
        # Retorna o grafo do circuito
        return grafo


    ##########################################################
    #        Criar grafo de uma procura não informada        #
    ##########################################################
    def nao_informada(self, coordenadas, velocidade):
        # Para cada velocidade é calculado o valor do próximo nodo e da próxima velocidade
        proxPos, proxVel = self.calculaPosicao(coordenadas,velocidade,(0,0)), self.calculaVelocidade(velocidade,(0,0))
        return proxPos, proxVel


    ######################################################
    #        Criar grafo de uma procura informada        #
    ######################################################
    def informada(self, coordenadas, velocidade, aceleracao):
        # Para cada aceleracao é calculado o valor do próximo nodo e da próxima velocidade
        proxPos, proxVel = self.calculaPosicao(coordenadas,velocidade,aceleracao), self.calculaVelocidade(velocidade,aceleracao)
        return proxPos, proxVel


    #########################
    #       Procura DFS     #
    #########################
    def procuraDFS(self, start, start_vel, end, path=[], visited=set()):
        # Adiciona ao caminho o ponto inicial
        path.append((start, start_vel))
        # Adiciona o inicial aos visitados
        visited.add((start, start_vel))
        
        # Verifica se a procura chegou ao fim
        if start in end:
            # Calcula o custo do caminho quando terminar a procura
            custoT = self.calculaCusto(path)
            # Retorna o caminho e o custo do mesmo
            return (path, custoT)
        
        # Se o nodo atual fizer parte das chaves do grafo...
        if start in self.grafo.keys():
            # Vamos analisar os seus filhos
            for adjacente, adjacente_vel, peso in self.grafo[start]:
                # Para cada adjacente verifica se já foi visitado e repetimos o algoritmo
                if (adjacente, adjacente_vel) not in visited:
                    resultado = self.procuraDFS(adjacente, adjacente_vel, end, path, visited)
                    # Retornamos o resultado da procura caso este não seja vazio
                    if resultado != ([],0):
                        return resultado
        
        # Retiramos do caminho o último nodo
        path.pop()
        return ([], 0)


    #######################################
    #             Procura BFS             #
    #######################################
    def procuraBFS(self, start, start_vel, end):
        # Conjunto de nodos já navegados
        visited = set()
        # Fila de nodos pelos quais passaremos até encontrar o ponto Final 
        fila = Queue()

        # Adicionar o nodo inicial à fila e aos visitados
        fila.put((start, start_vel))
        visited.add((start, start_vel))

        parent = dict()
        # Define-se que o nodo P do qual o circuito se inicia não tem pais
        parent[(start, start_vel)] = (None, None)

        # Esta flag é usada para verificar se chegamos a um ponto F do circuito
        fim = False
        
        while not fila.empty() and fim == False:
            # Enquanto a fila tiver elementos extraímo-los um a um com o método get e designamo-los por nodo_atual sobre a possibilidade
            # de ser o nodo que pretendemos encontrar no final
            (nodo_atual, vel_atual) = fila.get()
            if nodo_atual in end:
                # Procuramos saber se estamos já no nodo final se assim for a flag passa a True
                fim = True
            else:
                # Se não estamos no nodo final procuramos saber se o nodo em que estamos está presente no grafo
                if nodo_atual in self.grafo.keys():
                    for adjacente, adjacente_vel, peso in self.grafo[nodo_atual]:
                        # Para cada nodo adjacente adicionamo-lo à fila de procura e indicamos que o pai desse adjacente é o atual em que estamos.
                        # Por fim colocamo-lo nos já visitados para escapar de procuras repetidas
                        if (adjacente, adjacente_vel) not in visited:
                            fila.put((adjacente, adjacente_vel))
                            parent[(adjacente, adjacente_vel)] = (nodo_atual, vel_atual)
                            visited.add((adjacente, adjacente_vel))
        # Por fim falta apenas inverter a lista para obtermos o caminho
        path = []
        if fim:
            path.append((nodo_atual, vel_atual))
            while parent[(nodo_atual, vel_atual)] != (None, None):
                path.append(parent[(nodo_atual, vel_atual)])
                (nodo_atual, vel_atual) = parent[(nodo_atual, vel_atual)]
            path.reverse()
            # Funçao que calcula o custo do caminho
            custo = self.calculaCusto(path)
        else:
            print("Caminho do algoritmo BFS não encontrado...")    
            custo = 0
        return (path, custo)


    ########################################
    #                Greedy                # 
    ########################################
    def greedy(self, start, start_vel, end):
        # open_list é uma lista com tuplos de nodos por visitar e as velocidades no nodo atual
        open_list = set([(start, start_vel)])
        # closed_list é uma lista de nodos já visitados    
        closed_list = set([])

        # parents é um dicionário que mantém o antecessor de um nodo
        parents = {}
        parents[(start, start_vel)] = (start, start_vel)

        # Enquanto existir elementos na open_list...
        while len(open_list) > 0:
            (nodo_atual, vel_atual) = (None, None)
            # Define o nodo com a melhor heurísitca, isto é, aquele com a menor distância euclidiana ao ponto final
            for (v, v_vel) in open_list:
                if nodo_atual == None or self.calculaMenorDistancia(v) < self.calculaMenorDistancia(nodo_atual):  
                    (nodo_atual, vel_atual) = (v, v_vel)

            # Verifica-se se o caminho existe
            if (nodo_atual, vel_atual) == (None, None):
                print("Caminho do algoritmo Greedy não encontrado...")
                return ([], 0)

            # Se o nodo corrente é o destino reconstroi-se o caminho a partir desse nodo até ao (start, start_vel) seguindo o antecessor
            if nodo_atual in end:
                reconst_path = []
                while parents[(nodo_atual, vel_atual)] != (nodo_atual, vel_atual):
                    reconst_path.append((nodo_atual, vel_atual))
                    (nodo_atual, vel_atual) = parents[(nodo_atual, vel_atual)]
                reconst_path.append((start, start_vel))
                reconst_path.reverse()
                return (reconst_path, self.calculaCusto(reconst_path))

            # Caso contrário, verifica-se se o nodo atual existe no grafo
            if nodo_atual in self.grafo.keys():
                # E para todos os vizinhos do nodo atual...
                for adjacente, adjacente_vel, peso in self.grafo[nodo_atual]:
                    # Verificamos se não está na closed_list, na open_list e se não é uma parede, ou seja, o peso é diferente de 25
                    if (adjacente,adjacente_vel) not in open_list and (adjacente,adjacente_vel) not in closed_list and peso != 25: 
                        # Se estas condições verificarem-se, adicionamos o vizinho à open_list e guardamos o nodo antecessor (nodo atual)
                        open_list.add((adjacente,adjacente_vel))
                        parents[(adjacente,adjacente_vel)]  = (nodo_atual, vel_atual)
            # Por fim transferimos o nodo da open_list para a closed_list
            open_list.remove((nodo_atual, vel_atual))
            closed_list.add((nodo_atual, vel_atual))

        print("Caminho do algoritmo Greedy não encontrado...")
        return ([], 0)


    ########################################
    #                  A*                  #
    ########################################
    def AEstrela(self, velocidade):
        # Cria duas listas uma para elementos que faltam pesquisar e outra para elementos já visitados
        # A open_list é uma lista de tuplos que guarda:
            # um tuplo com as coordenadas a sua velocidade de um nodo
            # a heurística do mesmo tuplo, isto é, do ponto atual
            # uma lista com o caminho efetuado até ao ponto atual
        open_list = [((self.start, velocidade), self.calculaHeuristica([(self.start, velocidade)]), [(self.start, velocidade)])]
        closed_list = [(self.start, velocidade)]

        while len(open_list) > 0:
            # Inicialização da variável best responsável por guardar o nodo com melhor heuristica, a heuristica e caminho 
            best = (((0, 0), (0, 0)), math.inf)

            # Enquanto há elementos para pesquisar escolhemos aquele com melhor heurística colocando-o como best
            for nodo_vel, heuristica, path in open_list:
                if heuristica < best[1]:
                    best = (nodo_vel, heuristica, path)

            # Removemos o best da open_list
            if (open_list.__contains__(best)):
                open_list.remove(best)

            # Se terminamos a procura no best devolve o custo da procura até este
            if best[0][0] in self.end:
                if best[2] != []:
                    return best[2], self.calculaCusto(best[2])
                else:
                    print("Caminho do algoritmo A* não encontrado...")
                    return ([], 0)

            # Caso contrário ...
            if best[0][0] in self.grafo.keys():
                # Para cada nodo filho do best vamos analisá-lo
                for adjacente, adjacente_vel, peso in self.grafo[best[0][0]]:
                    if peso != 25:
                        # Se o peso deste nodo for diferente de 25, ou seja, não é parede adicionamos ao caminho feito até agora
                        pathUntilNow = best[2].copy()
                        # E vamos por fim:
                        # Renovar o nosso caminho
                        # Colocar o adjacente na lista dos nodos já visitados
                        # Colocar na open_list o tuplo do adjacente com a sua heurística e o caminho até ele
                        if (adjacente, adjacente_vel) not in closed_list:
                            pathUntilNow.append((adjacente, adjacente_vel))
                            closed_list.append((adjacente, adjacente_vel))
                            open_list.append(((adjacente, adjacente_vel), self.calculaHeuristica(pathUntilNow), pathUntilNow))
                    else:
                        # Se o nodo for uma parede colocámo-lo logo como se fosse um nodo já visitado
                        closed_list.append((adjacente, adjacente_vel))
        print("Caminho do algoritmo A* não encontrado...")
        return ([], 0)


    ##################################
    # Devolver o custo de uma aresta #
    ##################################
    def getCustoArco(self, node1, node2):
         # Lista de arestas para aquele nodo
        for nodo, vel, custo in self.grafo[node1]:
            if nodo == node2:
                return custo
        # Retorna o custo entre dois nodos adjacentes
        custo = 0
        return custo


    ##################################################
    # Dado um caminho calcula o custo de o percorrer #
    ##################################################
    def calculaCusto(self, caminho):
        # O caminho são todos os nodos pelos quais ataravessamos e onde foi possível chegar ao destino F a partir de P
        custo = 0
        i = 0
        while i + 1 < len(caminho):
            custo += self.getCustoArco(caminho[i][0], caminho[i+1][0])
            i += 1
        # Retorna o custo de navegar pelo caminho mais curto
        return custo


    ##############################################################################
    # Calcula a posicao do proximo nodo tendo em conta a velocidade e aceleração #
    ##############################################################################
    def calculaPosicao(self,coord,vel,ac):
        (pL,pC) = coord
        (vL,vC) = vel
        (aL,aC) = ac
        retPL = pL + vL + aL
        retPC = pC + vC + aC
        # Retorna o valor das coords seguintes dado um conjunto de parametros necessarios para esse calculo
        return (retPL,retPC)


    ###############################################################################
    # Calcula a proxima velocidade tendo em conta a velocidade atual e aceleração #
    ###############################################################################
    def calculaVelocidade(self,vel,acel):
        (vl,vc) = vel
        (al,ac) = acel
        retVL = vl + al
        retVC = vc + ac
        # Retorna o valor da proxima velocidade dado um conjunto de parametros necessarios para esse calculo
        return (retVL,retVC)


    #####################################################
    # Verifica se as coordenadas de um nodo são válidas #
    # quando o mesmo encontra-se na mesma linha/coluna  #
    #                  que o anterior                   #
    #####################################################
    def validaNodo_aux(self, x1, y1, x2, y2):
        # Estão na mesma linha
        if x1 == x2:
            # Vai ver coluna a coluna se existem paredes
            if y1 > y2:
                while y1 != y2 - 1:
                    if self.circuito[x1][y1] == 'X':
                        return False
                    y1 -= 1
            elif y1 < y2:
                while y1 != y2 + 1:
                    if self.circuito[x1][y1] == 'X':
                        return False
                    y1 += 1
        # Estão na mesma coluna
        elif y1 == y2:
            # Vai ver linha a linha se existem paredes
            if x1 > x2:
                while x1 != x2 - 1:
                    if self.circuito[x1][y1] == 'X':
                        return False
                    x1 -= 1
            elif x1 < x2:
                while x1 != x2 + 1:
                    if self.circuito[x1][y1] == 'X':
                        return False
                    x1 += 1
        return True

    #####################################################
    # Verifica se as coordenadas de um nodo são válidas #
    #####################################################
    def validaNodo(self, x1, y1, x2, y2):
        # Verifica se o próximo nodo (x2,y2) está nos limites do circuito e se não é uma parede
        if (0 <= x2 < len(self.circuito) and 0 <= y2 < len(self.circuito[0]) and self.circuito[x2][y2] != 'X'):
            # Verifica a existência de paredes para nodos que estão na mesma linha / coluna
            if x1==x2 or y1==y2:
                return self.validaNodo_aux(x1, y1, x2, y2)
            # Verifica a existência de paredes na diagonal entre os nodos
            mapa = self.circuito
            # Calcula o declive da reta
            declive = (y1 - y2) / (x1 - x2)
            # Calcula a equação que define a reta entre os dois nodos
            m = y1 - (declive * x1)
            if (x1 > x2):
                aux = x1
                x1 = x2
                x2 = aux
            if (y1 > y2):
                aux = y1
                y1 = y2
                y2 = aux
            # Verifica se existe alguma parede entre os dois pontos
            for i in range(x1 + 1, x2):
                j1 = math.floor(declive * i + m)
                j2 = math.ceil(declive * i + m)
                if (mapa[i][j1] == "X"): return False
                if (mapa[i][j2] == "X"): return False
            for j in range(y1 + 1, y2):
                i1 = math.floor((j - m) / declive)
                i2 = math.ceil((j - m) / declive)
                if (mapa[i1][j] == "X"): return False
                if (mapa[i2][j] == "X"): return False
            # Retorna False se não existir paredes entre os nodos
            return True
        # Retorna False se existir alguma parede entre os nodos
        return False


    ######################################################################
    # Calcula a menor distância desde um dado ponto até a um ponto final #
    ######################################################################
    def calculaMenorDistancia(self, coords):
        (x, y) = coords
        dist = math.inf
        for x1,y1 in self.end:
            # Calcula a menor distania ate ao final através do método euclidiano
            dist_prov = math.sqrt((math.pow(x1 - x, 2) + math.pow(y1 - y, 2)))
            # Caso a distância provisória seja menor do que a distância atual, esta assume o valor da primeira   
            if(dist_prov < dist):
                dist = dist_prov
        return dist


    ######################################################################
    # Calcula a menor distância desde um dado ponto até a um ponto final #
    #       tendo em conta o caminho percorrido até esse dado ponto      #
    ######################################################################
    def calculaHeuristica(self, path):
        i = len(path) - 1

        # Último nodo do caminho
        ultimo = path[i][0]

        # O valor melhor_dist é inicializado com a distancia em linha
        # reta entre o último nodo do caminho e o final
        melhor_dist = self.calculaMenorDistancia(path[i][0])
        
        i -= 1
        # Calcula o custo do caminho a partir no nodo final (não inclusive)
        while i >= 0 :
            for nodo, vel, peso in self.grafo[path[i][0]]:
                    if nodo == ultimo:
                        # Vamos adicionando à melhor distância até ao final o custo do caminho para trás
                        melhor_dist += peso
            ultimo = path[i][0]
            i -= 1
        return melhor_dist


##########################################################################
# Fórmula que determina a velocidade de um jogador num determinado ponto # 
##########################################################################
def velocidade(vel):
    (v1,v2) = vel
    # Retorna a velocidade de um jogador calculada através do método euclidiano
    return math.sqrt((math.pow(v1, 2) + math.pow(v2, 2)))


##################################################################
# Analisa se há jogadores no mesmo sitio ao mesmo tempo e decide # 
#              a qual deles deve incrementar o custo             #                
##################################################################
def colisao (jogadores: list):
    # A definição deste método segue a seguinte lógica:
    # para cada posição onde mais que um jogador entra verifica quais
    # aqueles com uma mesma velocidade máxima no nodo de onde vieram, imediatamente, antes,
    # os que tiverem velocidade inferior a esta incrementa o custo em 25 unidades,
    # para os restantes que estejam na mesma peça à velocidade máxima de onde partiram, anteriormente,
    # penaliza ordenando-os para penalizar mais aqueles que até então têm já um custo menor efetuado
    iteracoes = {}

    # Coloca no dicionario cada coordenada do caminho de cada jogador
    # Associado a esse cordenada temos um tuplo com o jogador e com o momento em que ele passou naquela coordenada  
    for jogador in jogadores:
        for i in range(1, len(jogador.path)):
            coord = jogador.path[i][0] 
            if coord not in iteracoes.keys():
                iteracoes[coord] = set()              
            iteracoes[coord].add((jogador, i))
    
    # Vai percorrer o dicionario e ver, para cada chave, isto é, cada coordenada se há jogadores com 
    # a mesma iteracao -> caso haja significa que jogadores diferentes passaram pelo mesmo sitio ao mesmo tempo
    for key in iteracoes.keys():
        visitados = set()
        repetidos = []

        for jog, ite in iteracoes[key]:
            # Se ainda não houver tuplos com a iteracao ite...
            if [x for (x, y) in visitados if y == ite] == []:
                # Adicionamos a visitados o tuplo
                visitados.add((jog, ite))
            else:
                # Se houver então calculamos a velocidade do jogador e adicionamos à lista repetidos
                vel = velocidade(jog.path[ite][1])    
                repetidos.append((jog, vel, ite))

                # Para além disso, adicionamos a repetidos o elemento que está em visitados (caso ainda não esteja em repetidos)
                jog_vis = [x for (x, y) in visitados if y == ite][0]
                vel_vis = velocidade(jog_vis.path[ite][1])    
                if (jog_vis, vel_vis, ite) not in repetidos:
                    repetidos.append((jog_vis, vel_vis, ite))

        # Caso haja 2 ou mais jogadores no mesmo sitio ao mesmo tempo vamos ter que comparar as velocidades de cada um nesse sitio;
        # Caso repetidos, neste ponto, seja diferente de vazio, vamos buscar o elemento com a maior velocidade e removê-lo da lista
        # Desta forma ficamos apenas com os jogadores que têm que alterar o custo
        if repetidos != []:
            # Ordenamos a lista de acordo com o custo associado a cada jogador
            # Assim, caso os jogadores tenham a mesma velocidade, a velocidade máxima 
            # irá pertencer ao jogador com menor custo
            repetidos = sorted(repetidos, key=lambda x : x[0].cost)
            
            # Vamos buscar o jogador com a velocidade máxima naquele ponto
            player_with_vel_max = max(repetidos, key=lambda x: x[1])
            # Retira o jogador da lista
            repetidos.remove(player_with_vel_max)

        # Aquele(s) jogador(es) com a(s) velocidad(es) mais baixa(s) deve(m) aumentar o custo em 25
        for jog, ite, vel in repetidos:
            # Vamos buscar à lista de jogadores o jogador jog
            update_jogador = jogadores[jogadores.index(jog)]
            # Removemos jog (original) da lista
            jogadores.remove(jog)
            # Atualiza o custo do jog e voltamos a adicioná-lo à lista de jogadores
            next_cost =  int(0.1 * update_jogador.cost)
            if  next_cost == 0:
                next_cost = 1
            update_jogador.cost += next_cost
            jogadores.append(update_jogador)
    return jogadores
 

#####################################################################
# Executa o(s) algoritmo(s) de procura do(s) jogador(es) a competir # 
#####################################################################
def fazProcura(start, end: list, jogadores: list):
    for player in jogadores:
        if player.algorithm == 0:
            (player.path, player.cost) = player.graph.AEstrela((0,0))
        if player.algorithm == 1:
            (player.path, player.cost) = player.graph.greedy(start, (0,0), end)
        if player.algorithm == 2:
            (player.path, player.cost) = player.graph.procuraBFS(start, (0,0), end)
        if player.algorithm == 3:
            (player.path, player.cost) = player.graph.procuraDFS(start, (0,0), end, path = [], visited = set())
    return jogadores