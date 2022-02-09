from heapq import heappop, heappush

class Node:

	deleted = -1
	unknown = 0
	closed = 1
	open = 2

	def __init__(self, pos):
		self.pos = pos
		self.status = Node.unknown
		self.previous = None
		self.cost = 0
		self.est_remaining_cost = 0

	def get_total_cost(self):
		return self.cost + self.est_remaining_cost

	def __lt__(self, other):
		return self.get_total_cost() < other.get_total_cost()

	def __repr__(self):
		return f"{self.pos} {self.cost} {self.get_total_cost()}"

class OpenList:
	def __init__(self):
		self.list = []

	def is_empty(self):
		return len(self.list) == 0

	def push(self, node):
		heappush(self.list, node)

	def pop(self):
		while len(self.list) > 0:
			node = heappop(self.list)
			if node.status != Node.deleted:
				return node
		return None

def init_pos(matrix, depth):
    arr = []
    for j in [3,5,7,9]:
        i = len(matrix) - 2
        # while matrix[i][j] != '.':
        for i1 in range(depth):
            arr.append(matrix[i-i1][j])
    start_pos = ''.join(arr + matrix[1][1:-1])
    return start_pos

def dist(depth, p1, p2):
    distance = 0
    entry1, entry2 = p1, p2
    room1, room2 = None, None
    if p1 < 4*depth:
        distance += depth - p1%depth
        room1 = p1 // depth
        entry1 = 4*depth + 2 + room1*2
    if p2 < 4*depth:
        distance += depth - p2%depth
        room2 = p2 // depth
        entry2 = 4*depth + 2 + room2*2
    if room1 is not None and room2 is not None and room1 == room2:
        return abs(p2 - p1)
    distance += abs(entry2 - entry1)
    return distance

def make_move(pos, start, target):
    new_pos = list(pos)
    new_pos[target] = pos[start]
    new_pos[start] = '.'
    return ''.join(new_pos)

def heuristic_distance(pos, depth):
    total_distance = 0
    for pod in range(4):
        ind = pod*4
        letter = 'ABCD'[pod]
        indexes = []
        targets = range(ind, ind+depth)
        for _ in range(depth):
            ind = (2*pos).index(letter, ind) % len(pos)
            indexes.append(ind)
            ind += 1
        print('indexes', indexes)
        pods_dist = sum(dist(depth, index, target) for index, target in zip(indexes, targets))
        total_distance += pods_dist * energy[letter]
    return total_distance

def get_path(node):
	# Returns the path used to get to the given node.
	path = []
	while node != None:
		path.append((node.pos, node.cost))
		node = node.previous
	return list(reversed(path))

def find_path_astar(start, end, depth):
	# Finds the path from start to end.
	nodes = {}
	open_list = OpenList()

	node = Node(start)
	node.status = Node.open
	nodes[start] = node
	open_list.push(node)

	while not open_list.is_empty():
		node = open_list.pop()
		if node is None:
			break
		nodes[node.pos].status = Node.closed

		if node.pos == end:
			return get_path(node), node.cost

		for next, next_cost in find_moves(node.pos, depth):
			next_node = nodes.get(next, Node(next))
			if next_node.status == Node.closed:
				continue

			cost = node.cost + next_cost
			if next_node.status != Node.open:
				est_cost = heuristic_distance(next_node.pos, end)
				next_node.cost = cost
				next_node.est_remaining_cost = est_cost
				next_node.previous = node
				next_node.status = Node.open
				nodes[next] = next_node
				open_list.push(next_node)
			elif cost < next_node.cost:
				updated_node = Node(next)
				updated_node.status = next_node.status
				updated_node.previous = node
				updated_node.cost = cost
				updated_node.est_remaining_cost = next_node.est_remaining_cost
				nodes[next] = updated_node
				next_node.status = Node.deleted
				open_list.push(updated_node)
	return None, -1

def find_moves(pos, depth):
    moves = []
    for room in range(0, 4):
        for room_cell in range(0, depth):
            start_cell = room * depth + room_cell
            pod = pos[start_cell]
            if pod == '.':
                continue

            cost_to_hall = cost_from_room_to_hall(pos, room, room_cell)
            if cost_to_hall is None:
                continue

            enter_hall_cell = 4*depth + 2 + 2*room
            find_moves_to_room(moves, pos, pod, start_cell, room, cost_to_hall,
                            enter_hall_cell)
            find_moves_to_hall(moves, pos, pod, start_cell, cost_to_hall,
                            enter_hall_cell)

    for start_cell in hall_cells:
        pod = pos[start_cell]
        if pod == '.':
            continue
        find_moves_to_room(moves, pos, pod, start_cell, None, 0, start_cell)

    return sorted(moves, key=lambda x: x[1])

def is_valid_room_target(pos, start, target, depth):
    assert (target < 4*depth)
    


with open("23/data.txt") as f:
    puzzles = f.read().split('\n\n')
puzzles = [[[char for char in line] for line in puzzle.splitlines()] for puzzle in puzzles]
# print(puzzles[0])

energy = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}

matrix = puzzles[1]
depth = len(matrix) - 3
hall_cells = [4*depth + i for i in [0,1,3,5,7,9,10]]
start_pos = init_pos(matrix, depth)
end_pos = ''.join([e*depth for e in 'ABCD']) + 11*'.'

print(start_pos, depth)
print(end_pos)
# find_path_astar(start_pos, end_pos, depth)

is_valid_room_target(start_pos, start_pos, 3, depth)
