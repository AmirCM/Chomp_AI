import random


class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        self.items.append(item)
        return self.items

    def dequeue(self):
        item = self.items[0]
        self.items.remove(item)
        return item

    def __iter__(self):
        return self.items.__iter__()

    def empty(self):
        if len(self.items):
            return False
        return True

    def get_items(self):
        return self.items

    def get_key_values(self, key):
        l = []
        for item in self.items:
            l.append(item[key])
        return l


class PriorityQueue(object):
    def __init__(self):
        self.queue = []

    def __str__(self):
        return ' '.join([str(i) for i in self.queue])

        # for checking if the queue is empty

    def empty(self):
        if len(self.queue):
            return False
        return True

        # for inserting an element in the queue

    def enqueue(self, data):
        for i in range(len(self.queue)):
            if self.queue[i]['node'] == data['node']:
                if data['f'] < self.queue[i]['f']:
                    self.queue[i]['f'] = data['f']
                    return True
                return False
        self.queue.append(data)
        return True
        # for popping an element based on Priority

    def dequeue(self):
        try:
            min_index = 0
            for i in range(len(self.queue)):
                if self.queue[i]['f'] < self.queue[min_index]['f']:
                    min_index = i
            item = self.queue[min_index]
            del self.queue[min_index]
            return item
        except IndexError:
            print()
            exit()


class Maze:
    height = None
    width = None
    board = None

    def __init__(self, height, width, walls=None):
        self.height = height + 2
        self.width = width + 2
        self.board = [
            [1 if x in (0, width + 1) or y in (0, height + 1) else 0 for x in range(self.width)]
            for y in range(self.height)
        ]
        if walls:
            walls_number = walls
        else:
            walls_number = int((height * width) * 40 / 100)

        self.board[3][4] = 1
        for i in range(walls_number):
            x = random.randint(1, height)
            y = random.randint(1, width)
            self.board[x][y] = 1

    def print_board(self):
        for i in self.board:
            print(i)


def is_valid_action(board, point):
    try:
        if board[point['row']][point['column']]:
            return False
        return True
    except IndexError as e:
        print("***Failed: " + str(e))


def get_neighbours(board, point):
    row_moves = [-1, 0, 1, 0]
    column_moves = [0, -1, 0, 1]

    neighbours = []
    point_row_num = point['row']
    point_column_num = point['column']

    for i in range(4):
        new_point = {
            'row': point_row_num + row_moves[i],
            'column': point_column_num + column_moves[i]
        }

        if is_valid_action(board, new_point):
            neighbours.append(new_point)

    return neighbours


def breadth_first_search(board, start, end):
    path_cost = 0
    visited_nodes_num = 0

    if start == end:
        return {'result': True, 'solution': [start, ], 'path_cost': path_cost,
                "visited_nodes_number": visited_nodes_num}

    frontier_queue = Queue()
    explored_queue = Queue()
    path_list = []
    frontier_queue.enqueue(start)

    while True:
        if frontier_queue.empty():
            return {'result': False, 'solution': None, "path_cost": None, "visited_nodes_number": visited_nodes_num}
        point = frontier_queue.dequeue()
        explored_queue.enqueue(point)
        visited_nodes_num += 1
        neighbours = get_neighbours(board, point)
        for neighbour in neighbours:
            if neighbour not in iter(frontier_queue) and neighbour not in explored_queue:
                if neighbour == end:
                    path_list.append({
                        'current': neighbour,
                        'previous': point
                    })
                    current = end
                    solution_list = [current, ]
                    while True:
                        for itm in path_list:
                            if current == itm['current']:
                                solution_list.append(itm['previous'])
                                current = itm['previous']
                                break
                        if current == start:
                            break
                    solution_list.reverse()
                    return {'result': True, 'solution': solution_list, "path_cost": len(solution_list),
                            "visited_nodes_number": visited_nodes_num}
                frontier_queue.enqueue(neighbour)
                path_list.append({
                    'current': neighbour,
                    'previous': point
                })


def iterative_deepening_depth_first_search(board, start, end, max_depth=None):
    if not max_depth:
        max_depth = 10
    path_list = []
    visited_nodes_num = [0]
    for i in range(max_depth):
        if depth_limited_search(board, start, end, i, path_list, visited_nodes_num):
            path_list.append(start)
            path_list.reverse()
            return {'result': True, 'solution': path_list, "path_cost": len(path_list),
                    "visited_nodes_number": visited_nodes_num[0]}
    return {'result': False, 'solution': None, "path_cost": None, "visited_nodes_number": visited_nodes_num[0]}


def depth_limited_search(board, start, end, max_depth, path_list, visited_nodes_num):
    visited_nodes_num[0] += 1

    if start == end:
        return True

    if max_depth <= 0:
        return False

    for child in get_neighbours(board, start):
        if depth_limited_search(board, child, end, max_depth - 1, path_list, visited_nodes_num):
            path_list.append(child)
            return True
    return False


def a_star_search(board, start, end):
    path_cost = 0
    visited_nodes_num = 0
    g = 0
    h = heuristic(start, end)
    relations = []

    if start == end:
        return {'result': True, 'solution': [start, ], 'path_cost': path_cost,
                "visited_nodes_number": visited_nodes_num}

    node = start
    frontier_queue = PriorityQueue()
    explored_queue = Queue()
    frontier_queue.enqueue({'node': node, 'f': g + h})

    while True:
        if frontier_queue.empty():
            return {'result': False, 'solution': None, "path_cost": None, "visited_nodes_number": visited_nodes_num}
        node = frontier_queue.dequeue()['node']
        explored_queue.enqueue(node)
        g += 1
        visited_nodes_num += 1
        if node == end:
            current = end
            solution_list = [current, ]
            while True:
                for itm in relations:
                    if current == itm['current']:
                        solution_list.append(itm['previous'])
                        current = itm['previous']
                        break
                if current == start:
                    break
            solution_list.reverse()
            return {'result': True, 'solution': solution_list, "path_cost": len(solution_list),
                    "visited_nodes_number": visited_nodes_num}

        neighbours = get_neighbours(board, node)
        for neighbour in neighbours:
            h = heuristic(neighbour, end)
            if neighbour not in explored_queue.get_items():
                if frontier_queue.enqueue({'node': neighbour, 'f': g + h}):
                    exist = False
                    for relation in relations:
                        if relation['current'] == neighbour:
                            relation['previous'] = node
                            exist = True
                    if not exist:
                        relations.append({'current': neighbour, 'previous': node})


# Euclidean Distance
def heuristic(current_node, end_node):
    d_row = abs(current_node['row'] - end_node['row'])
    d_column = abs(current_node['column'] - end_node['column'])
    return (d_row ** 2) + (d_column ** 2)
    # return d_row + d_column


if __name__ == '__main__':
    maze = Maze(20, 20)

    maze.print_board()
    start = {
        'row': 2,
        'column': 2
    }
    end = {
        'row': 5,
        'column': 5
    }
    print("*******BFS")
    result = breadth_first_search(maze.board, start, end)
    print(result)
    print(result['path_cost'])
    print(result['visited_nodes_number'])
    print("*******DFS")
    result = iterative_deepening_depth_first_search(maze.board, start, end)
    print(result)
    print(result['path_cost'])
    print(result['visited_nodes_number'])
    print("*******A STAR")
    result = a_star_search(maze.board, start, end)
    print(result)
    print(result['path_cost'])
    print(result['visited_nodes_number'])
