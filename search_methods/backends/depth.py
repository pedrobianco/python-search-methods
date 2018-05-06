from search_methods.base import SearchAbstract
import numpy as np
from PIL import Image
import time
import sys

visited = []
marked = []
result = []
num_of_states_visited = 0


class Search(SearchAbstract):
    NAME = 'Depth'

def load_image(infilename):
    img = Image.open(infilename)
    impixels = img.load()
    data = np.asarray(img, dtype="int32")
    return data


def save_image(npdata, outfilename):
    img = Image.fromarray(np.asarray(np.clip(npdata, 0, 255), dtype="uint8"), "RGBA")
    img.save(outfilename)


def find_entry(data):
    for index, x in enumerate(data[0]):
        if x[0] == 0:
            return 0, index


def find_exit(data):
    wd, hd, sd = data.shape
    for index, x in enumerate(data[-1]):
        if x[0] == 0:
            return wd - 2, index

        

def find_dir(data, l, c, block=2):
    right = 0
    left = 0
    top = 0
    down = 0
    wd, hd, sd = data.shape
    # right
    if c < wd - block and data[l][c + block][0] == 0:
        right = block
    # left
    if c > block and (data[l][c - block][0] == 0 or data[l + 1][c - block][0] == 0):
        left = block
        # down
    if l < hd - block and data[l + block][c][0] == 0:
        down = block
    # top
    if l > block and (data[l - block][c][0] == 0 or data[l - block][c + 1][0] == 0):
        top = block
    return right, down, left, top


class Graph_state:
    def __init__(self, line, column, start=False):
        self.line = line
        self.column = column
        self.start = start
        self.children = []
        self.parent = None
        self.goal = False

    def isgoal(self, objective):
        if (objective[0] == self.line) and (objective[1] == self.column):
            self.goal = True

    def add(self, child):
        child.parent = self
        self.children.append(child)

    def __str__(self):
        repre = "(%d,%d)" % (self.line, self.column)
        return repre


def marcar(data, estado_pai):
    estado_inicio = estado_pai
    for estado in reversed(result):
        if estado == estado_pai:
            continue
        estado_final = estado
        colorir(data, estado_inicio, estado_final)
        estado_inicio = estado_final


def colorir(data, act_state, objective):
    if act_state.column == objective.column:
        distancia_estado = objective.line - act_state.line
        if distancia_estado < 0:
            for x in range(abs(distancia_estado)):
                data[act_state.line - x][act_state.column] = [255, 0, 0, 255]
        else:
            for x in range(distancia_estado):
                data[x + act_state.line][act_state.column] = [255, 0, 0, 255]
    elif act_state.line == objective.line:
        distancia_estado = objective.column - act_state.column
        if distancia_estado < 0:
            for y in range(abs(distancia_estado)):
                data[act_state.line][act_state.column - y] = [255, 0, 0, 255]
        else:
            for y in range(distancia_estado):
                data[act_state.line][y + act_state.column] = [255, 0, 0, 255]


def find_next_intersection(data, act_state, vector, objective):
    wd, hd, sd = data.shape
    if vector[0] != 0:
        # go right
        for x in range(act_state.column + vector[0], wd, vector[0]):
            right, down, left, top = find_dir(data, act_state.line, x)
            if right == 0:  # found an edge
                new_state = Graph_state(act_state.line, x)
                new_state.isgoal(objective)
                act_state.add(new_state)
                find_next_intersection(data, new_state, (0, down, 0, top), objective)
                break
            if down != 0 or top != 0:
                new_state = Graph_state(act_state.line, x)
                new_state.isgoal(objective)
                act_state.add(new_state)
                find_next_intersection(data, new_state, (0, down, 0, top), objective)
    if vector[1] != 0:
        # go down
        for y in range(act_state.line + vector[1], hd, vector[1]):
            right, down, left, top = find_dir(data, y, act_state.column)
            if down == 0:  # found an edge
                new_state = Graph_state(y, act_state.column)
                new_state.isgoal(objective)
                act_state.add(new_state)
                find_next_intersection(data, new_state, (right, 0, left, 0), objective)
                break
            if right != 0 or left != 0:
                new_state = Graph_state(y, act_state.column)
                new_state.isgoal(objective)
                act_state.add(new_state)
                find_next_intersection(data, new_state, (right, 0, left, 0), objective)
    if vector[2] != 0:
        # go left
        for x in range(act_state.column - vector[2], 0, -vector[2]):
            right, down, left, top = find_dir(data, act_state.line, x)
            if left == 0:  # found an edge
                new_state = Graph_state(act_state.line, x)
                new_state.isgoal(objective)
                act_state.add(new_state)
                find_next_intersection(data, new_state, (0, down, 0, top), objective)
                break
            if down != 0 or top != 0:
                new_state = Graph_state(act_state.line, x)
                new_state.isgoal(objective)
                act_state.add(new_state)
                find_next_intersection(data, new_state, (0, down, 0, top), objective)
    if vector[3] != 0:
        # go up
        for y in range(act_state.line - vector[3], 0, -vector[3]):
            right, down, left, top = find_dir(data, y, act_state.column)
            if top == 0:  # found an edge
                new_state = Graph_state(y, act_state.column)
                new_state.isgoal(objective)
                act_state.add(new_state)
                find_next_intersection(data, new_state, (right, 0, left, 0), objective)
                break
            if right != 0 or left != 0:
                new_state = Graph_state(y, act_state.column)
                new_state.isgoal(objective)
                act_state.add(new_state)
                find_next_intersection(data, new_state, (right, 0, left, 0), objective)


def count_state(root_state, count):
    for s in root_state.children:
        count += 1
        count += count_state(s, 0)
    return count


def search_widht(data, estado_pai):
    global visited
    global marked
    global result
    global num_of_states_visited

    visited.append(estado_pai)
    num_of_states_visited += 1

    for estado_filho in estado_pai.children:
        if not estado_filho in marked and not estado_filho in visited:
            search_widht(data, estado_filho)

    if estado_pai.goal:
        data[estado_pai.line][estado_pai.column] = [255, 0, 0, 255]
        result.append(estado_pai)

    for estado_filho in estado_pai.children:

        if estado_filho in result:
            result.append(estado_pai)


t0 = time.time()
img_data = load_image('./source/image.png')

sys.setrecursionlimit(10000)

l_entrada, c_entrada = find_entry(img_data)
lex, cex = find_exit(img_data)
objective = (lex, cex)
start_point = Graph_state(l_entrada, c_entrada, True)
start_point.isgoal(objective)
find_next_intersection(img_data, start_point, find_dir(img_data, l_entrada, c_entrada), objective)
total_state = count_state(start_point, 1)

search_widht(img_data, start_point)
marcar(img_data, start_point)

def get_search_response_payload(self):
    self.print("Método de busca em profundidade! ")
    self.print("Total de estados percorridos: %d" % total_state)
    self.print("Numero de estados visitados: %d" % num_of_states_visited)
    self.print("Tempo de processamento dos estados: %2.5f sec" % (time.time() - t0))

def get_problem_image_solution(self):
    self.save_image(img_data, './response/depth.png')
