from PIL import Image

from search_methods.base import SearchAbstract


class Search(SearchAbstract):

    NAME = "Busca em Profundidade"

    def __init__(self, image_array):
        super(Search, self).__init__(image_array)
        self.black_pixels = []

    def get_problem_image_solution(self):
        self.get_all_black_pixels()
        pass

    def get_search_response_payload(self):
        self.get_all_black_pixels()
        pass

    def debug(self, data):
        print("####### DEBUG #######")
        print("{}".format(data))
        print("####### END_DEBUG #######\n\n")

    # Metodo para selecionar os pixels pretos.
    def set_position_black_pixels(self, row, col, up, right, bottom, left):
        # Dicionario contendo as posições da imagem.
        black_pixel_position = {}
        black_pixel_position['row'] = row
        black_pixel_position['col'] = col
        black_pixel_position['up'] = up
        black_pixel_position['right'] = right
        black_pixel_position['bottom'] = bottom
        black_pixel_position['left'] = left
        # Incrementar lista de pixels pretos
        self.black_pixels.append(black_pixel_position)

    # Metodo responsavel por retornar as definicoes conforme a direcao selecionada
    def get_rule_direction(self, direction, row, col):
        directions = {
            'up': {
                'row': row - 1,
                'col': col
            },
            'right': {
                'row': row,
                'col': col + 1
            },
            'bottom': {
                'row': row + 1,
                'col': col
            },
            'left': {
                'row': row,
                'col': col - 1
            },
        }
        return directions[direction]

    # Metodo para verificar se ha caminho para percorrer
    def is_way(self, direction, row, col):
        # Verificar limites do array da imagem
        if (row < len(self.image_array) - 1):
            # Buscar caminho a ser seguido para direcao selecionada
            result = self.get_rule_direction(direction, row, col)
            # Retornar elemento encontrado a partir do caminho selecionado
            return self.image_array[result['row']][result['col']] if result != None else None
        return None
    # Metodo responsavel por contar o numero de pixels acessiveis na direcao selecionada
    def get_count_number_of_pixels(self, direction, row, col):
        # Caminho atual
        result = {'row': row, 'col': col}
        # Implementar contador
        count = 0
        # Verificar se ha caminho disponivel para a proxima selecao selecionada
        while (self.is_way(direction, result['row'], result['col'])[0] != None):
            # Verificar se é uma linha valida
            if (result['row'] < len(self.image_array) - 1):
                # Continuar percorrer novo caminho conforme a direcao
                result = self.get_rule_direction(direction, result['row'], result['col'])
                # Incrementar contador
                count = count + 1
        # Retornar quantidade de pixeis
        self.debug(count)
        exit()
        return count

    # Metodo responsavel por percorrer todos os pixels pretos
    def get_all_black_pixels(self):
        # Percorrer cada linha do matriz da imagem
        for rowIndex, row in enumerate(self.image_array):
            # Percorrer cada coluna da linha
            for colIndex, col in enumerate(row):
                # Verificar se possui algum elemento 0 (zero) pixel preto
                if [0] in col:
                    up = 0
                    right = 0
                    bottom = 0
                    left = 0
                    # Verificar possiveis caminhos
                    if (rowIndex > 0 and self.is_way('up', rowIndex, colIndex) != None):
                        up += self.get_count_number_of_pixels('up', rowIndex, colIndex)
                    if (rowIndex > 0 and self.is_way('right', rowIndex, colIndex) != None):
                        right += self.get_count_number_of_pixels('right', rowIndex, colIndex)
                    if (self.is_way('bottom', rowIndex, colIndex)[0] != None):
                        bottom += self.get_count_number_of_pixels('bottom', rowIndex, colIndex)
                    if (rowIndex > 0 and self.is_way('left', rowIndex, colIndex) != None):
                        left += self.get_count_number_of_pixels('left', rowIndex, colIndex)
                    # Inserir posicao dos pixeis
                    self.set_position_black_pixels(rowIndex, colIndex, up, right, bottom, left)
                    self.debug(self.black_pixels)

    #metodo da busca em profundidade:

    #algoriTMO:
    #para  u ← 1  até  n  faça
    #cor[u] ← branco
    #cor[r] ← cinza
    #P ← Cria-Pilha (r)
    #enquanto  P  não estiver vazia faça
    #u ← Copia-Topo-da-Pilha (P)
    #se  Adj[u]  contém  v  tal que  cor[v] = branco
    #então  cor[v] ← cinza
    #Coloca-na-Pilha (v, P)
    #senão  cor[u] ← preto
    #Tira-da-Pilha (P)
    #devolva  cor[1..n]

    #implementacao:




    def save_image(self):
        img = Image.fromarray(self.image_array)
        img.thumbnail((322,322))
        img.show()
        img.save('/response/depth/solutions.jpeg', 'JPEG')

