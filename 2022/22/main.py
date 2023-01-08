from os.path import join, dirname
import re
import math

directions = ['RIGHT', 'DOWN', 'LEFT', 'UP']

def parse(grid_str, path_str):
    grid = [list(row) for row in grid_str.splitlines()]
    max_width = max(len(row) for row in grid)
    for idx in range(len(grid)):
        current_width = len(grid[idx])
        grid[idx] += [' ' for _ in range(max_width - current_width)]

    grid_t = [*zip(*grid)]

    path = re.findall(r'[A-Z]|\d+', path_str)
    start_col = next(i for i, v in enumerate(grid[0]) if v == '.')
    return grid, grid_t, path, start_col

def cube_size(grid):
    nb_elements = sum(elem != ' ' for row in grid for elem in row)
    return round(math.sqrt(nb_elements/6))

def create_faces_dict(grid, size):
    face_from_coord = {}
    coord_from_face = {}
    face_num = 0
    for i in range(0, len(grid), size):
        for j in range(0, len(grid[0]), size):
            if grid[i][j] != ' ':
                face_from_coord[(i, j)] = face_num
                coord_from_face[face_num] = (i, j)
                face_num += 1
    return face_from_coord, coord_from_face

def get_face(faces, size, i, j):
    return faces[(i//size*size, j//size*size)]

def is_border(grid, position):
    i, j = position
    if i < 0 or i >= len(grid):
        return True
    if j < 0 or j >= len(grid[i]):
        return True
    if grid[i][j] == ' ':
        return True
    return False

def get_next_position(grid, grid_t, position, facing):
    i, j = position
    vectors = {
        'RIGHT': (0, 1),
        'LEFT': (0, -1),
        'UP': (-1, 0),
        'DOWN': (1, 0),
    }
    di, dj = vectors[facing]
    i1 = i + di
    j1 = j + dj
    if is_border(grid, (i1, j1)):
        i1, j1 = get_otherside(grid, grid_t, position, facing)
    if grid[i1][j1] == '.':
        return (i1, j1)
    elif grid[i1][j1] == '#':
        return (i, j)

def change_facing(facing, turn):
    index = directions.index(facing)
    new_index = index + 1 if turn == "R" else index - 1
    new_facing = directions[new_index%len(directions)]
    return new_facing

def move(grid, grid_t, path, facing, position):
    for idx, val in enumerate(path):
        # print('*********** NEW COMMAND', val)
        if idx%2 == 0:
            for _ in range(int(val)):
                position = get_next_position(grid, grid_t, position, facing)
                # print('position', position, facing)
        else:
            facing = change_facing(facing, val)
            # print('CHANGE FACING', facing)
    return position, facing

def get_otherside(grid, grid_t, position, facing):
    i, j = position
    i1, j1 = i, j
    if facing == 'RIGHT':
        j1 = next(k for k, v in enumerate(grid[i]) if v != ' ')
    elif facing == 'LEFT':
        j1 = next(c for c in range(len(grid[i])-1, -1, -1) if grid[i][c] != ' ')
    elif facing == 'DOWN':
        i1 = next(k for k, v in enumerate(grid_t[j]) if v != ' ')
    elif facing == 'UP':
        i1 = next(c for c in range(len(grid_t[j])-1, -1, -1) if grid_t[j][c] != ' ')
    return i1, j1

def solve_part_1(grid, grid_t, path, start_col):
    facing = 'RIGHT'
    position = (0, start_col)
    position, facing = move(grid, grid_t, path, facing, position)
    total = 1000 * (position[0]+1) + 4 * (position[1]+1) + directions.index(facing)
    return total

with open(join(dirname(__file__), 'data.txt')) as f:
    grid_str, path_str = f.read().split('\n\n')
grid, grid_t, path, start_col = parse(grid_str, path_str)

# print('PART_1', solve_part_1(grid, grid_t, path, start_col))

size = cube_size(grid)
print('size', size)
face_from_coord, coord_from_face = create_faces_dict(grid, size)
print('face_from_coord', face_from_coord)
print('coord_from_face', coord_from_face)
# print(get_face(face_from_coord, size, 1, 9))

rotations = {
    0: {
        "RIGHT": [5, 2],
        "LEFT": [2, -1],
        "UP": [1, 2],
    },
    1: {

    }
}


"""
rotations = {
    face_num: {
        RIGHT: [other_face_num, nb_rotation clockwise]
    }
}
"""