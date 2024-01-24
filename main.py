from time import sleep
import jogador
import grafo
import sys
import os

#######################################
#         Leitura do ficheiro         #
#######################################
def parse_ficheiro(file_circuito, start, end: list):
    circuito = []
    with open(file_circuito,"r") as file:
        data = file.readlines()
    x = 0
    for line in data:
        split_line = line.strip("\n")
        y = 0
        for char in split_line:
            # Armazena o ponto inicial
            if char == 'P':
                start[0] = x
                start[1] = y
                start = tuple(start)
            # Armazena o(s) ponto(s) da meta
            elif char == 'F':
                end.append((x,y))
            y+=1
        if(x == len(split_line)):
            break
        x+=1
        circuito.append(split_line)
    # Retorna a matriz que corresponde ao circuito, as coordenadas do nodo inicial e a lista com as coordenadas dos nodos finais
    return circuito, start, end


######################################################
# Atualiza um circuito de acordo com um dado caminho #
######################################################
def atualizaCircuito(circuito: list, caminho: list, prioridade: chr):
    chars = ['1','2','3','4','C']
    for posicao, vel in caminho:
        if circuito[posicao[0]][posicao[1]] != 'P':
            list_prov = list(circuito[posicao[0]])
            if circuito[posicao[0]][posicao[1]] not in chars:
                list_prov[posicao[1]] = prioridade
            else:
                list_prov[posicao[1]] = 'C'
            circuito[posicao[0]] = ''.join(list_prov)
    return circuito


#######################################
#           Função Principal          #
#######################################
def main():
    # Circuito_file é o nome do ficheiro que contém o circuito
    if len(sys.argv) != 2:
        print("Input inválido...")
        return 1
    circuito_file = sys.argv[1]

    # op será a variavel de input para as diferentes opções do utilizador
    op = -1

    # Chamada da função que executa o parse do ficheiro com o circuito
    start_list = [-1,-1]
    circuito, start, end = parse_ficheiro(circuito_file, start = start_list, end = [])

    # Validação do ponto de partida
    if(start == (-1,-1)):
        print("Circuito inválido, a partida não existe!")
        return 1 

    # Validação do(s) ponto(s) de chegada    
    if (end == []):
        print("Circuito inválido, a meta não existe!")
        return 1

    # Define o número de jogadores que irão participar no circuito
    nJogadores = int(input("Insira o número de jogadores: "))
    if nJogadores > 4:
        print("O número máximo de jogadores é 4!")
        return 1

    # Cria uma lista de jogadores
    # e uma com os algoritmos possiveis
    jogadores = []
    algoritmos_validos = [0,1,2,3]

    # Enquanto houverem jogadores a serem configurados...
    while nJogadores != 0:
        # Flag para garantir a inexistência de algoritmos repetidos ou inválidos
        flag = False
        # Limpar o terminal
        os.system('cls')
        print("=== Insira um nome ===")
        name = input("Nome: ")
        os.system('cls')
        
        while flag == False:
            print("=== Escolha um algortimo de procura ===")
            print("0-A*")
            print("1-Greedy")
            print("2-BFS")
            print("3-DFS")
            # Escolha do algoritmo
            algorithm = int(input("Algoritmo: ")) # 0 1 2 3
            if algorithm in algoritmos_validos:
                algoritmos_validos.remove(algorithm)
                flag = True
            else:
                print("Algoritmo inválido ou já escolhido! Tenta novamente...")
                sleep(1)
                os.system('cls')
        # Define para cada jogado, um nome, um algoritmo de procura,
        # o grafo que representa o caminho percorrido e o algoritmo escolhido para a corrida por jogador
        g = grafo.Graph(start, end, circuito, algorithm)
        player = jogador.Player(name, algorithm, g, -1)
        jogadores.append(player)
        nJogadores -= 1

    # De acordo com o input dado pelo utilizador:
    # 0 - Sair
    # 1 - Devolve o desenho do circuito
    # 2 - Imprime o circuito efetudado pelos jogadores
    while op != 0:
        os.system('cls')
        print("=== Menu ===")
        print("1-Imprimir Circuito")
        print("2-Corrida")
        print("0-Saír")
        op = int(input("Opcao ====> "))
        os.system('cls')
        if op == 0:
            print("A sair...")

        # Print do circuito escolhido
        while op == 1:
            print("\n=== Este é o circuito ===\n")
            for line in circuito:
                print(line)
            next_op = int(input("\nVoltar para trás ====> 0\n"))
            if next_op == 0:
                op = -1

        # Execução do(s) algortimo(s) 
        while op == 2:
            # Ordenar os jogadores tendo em conta cada algoritmo
            jogadores.sort(key=lambda x : x.algorithm)

            # Efetua a procura de cada jogador como se estes fizessem corridas individuais (Singleplayer)
            jogadores = grafo.fazProcura(start, end, jogadores)

            # A lista de jogadores é alterada evocando a função colisao         
            jogadores = grafo.colisao(jogadores)

            # Ordenar os jogadores tendo em conta o custo de cada algoritmo
            jogadores.sort(key=lambda x : x.cost)
            for i in range(0, len(jogadores)):
                # Atualiza o circuito com o caminho resultante do algoritmo
                icon = chr(i + 49)
                circuito = atualizaCircuito(circuito, jogadores[i].path, icon)
        
            # Fazer print dos caminhos resultantes (do circuito)
            for line in circuito:
                print(line)

            # Fazer print dos resultados finais de cada jogador
            for resultado in jogadores:
                print(resultado)

            next_op = int(input("Voltar para trás ====> 0\n"))
            if next_op == 0:
                op = -1
        if op not in [-1,0,1,2,3]:
            print("Comando não permitido!\n")
            input("Enter para continuar...\n")
    return 0

if __name__ == "__main__":
    main()
