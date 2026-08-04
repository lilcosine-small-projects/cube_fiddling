import copy
from collections import deque
import random

starting_state = [[0,0],[1,0],[2,0],[3,0],[4,0],[5,0],[6,0],[7,0]]

MOVE_MAP = {
  "U": [(0,1), (1,2), (2,3), (3,0)],
  # "D": [(4,7), (7,6), (6,5), (5,4)],
  # "L": [(1,5), (5,6), (6,2), (2,1)],
  "R": [(0,3), (3,7), (7,4), (4,0)],
  "F": [(0,4), (4,5), (5,1), (1,0)],
  # "B": [(3,2), (2,6), (6,7), (7,3)],
  "U'": [(0,3), (1,0), (2,1), (3,2)],
  # "D'": [(4,5), (5,6), (6,7), (7,4)],
  # "L'": [(1,2), (2,6), (6,5), (5,1)],
  "R'": [(0,4), (4,7), (7,3), (3,0)],
  "F'": [(0,1), (1,5), (5,4), (4,0)],
  # "B'": [(2,3), (3,7), (7,6), (6,2)],
  "U2": [(0,2), (1,3), (2,0), (3,1)],
  # "D2": [(4,6), (5,7), (6,4), (7,5)],
  # "L2": [(1,6), (2,5), (5,2), (6,1)],
  "R2": [(0,7), (3,4), (4,3), (7,0)],
  "F2": [(0,5), (5,0), (1,4), (4,1)],
  # "B2": [(2,7), (7,2), (3,6), (6,3)],
}

ORIENT_MAP = {
    "U": [0, 2, 1],
    "D": [0, 2, 1],
    "L": [2, 1, 0],
    "R": [2, 1, 0],
    "F": [1, 0, 2],
    "B": [1, 0, 2],
    "U'": [0, 2, 1],
    "D'": [0, 2, 1],
    "L'": [2, 1, 0],
    "R'": [2, 1, 0],
    "F'": [1, 0, 2],
    "B'": [1, 0, 2],
    "U2": [0, 1, 2],
    "D2": [0, 1, 2],
    "L2": [0, 1, 2],
    "R2": [0, 1, 2],
    "F2": [0, 1, 2],
    "B2": [0, 1, 2],
}

ROT_MAP = {
  "X": [
    (0,3), (3,7), (4,0), (7,4),
    (1,2), (2,6), (6,5), (5,1)
  ],
  "X'": [
    (0,4), (4,7), (7,3), (3,0),
    (2,1), (1,5), (5,6), (6,2)
  ],
  "Y": [
    (0,1), (1,2), (2,3), (3,0),
    (4,5), (5,6), (6,7), (7,4)
  ],
  "Y'": [
    (0,3), (1,0), (2,1), (3,2),
    (4,7), (7,6), (6,5), (5,4)
  ],
  "Z": [
    (1,0), (5,1), (6,2), (2,3),
    (0,4), (4,5), (7,6), (3,7)
  ],
  "Z'": [
    (0,1), (3,2), (4,0), (7,3),
    (5,4), (1,5), (2,6), (6,7)
  ],
}

ROT_ORIENT_MAP = {
    "X": [2, 1, 0],
    "X'": [2, 1, 0],
    "Y": [0, 2, 1],
    "Y'": [0, 2, 1],
    "Z": [1, 0, 2],
    "Z'": [1, 0, 2],
}

WHITE_ORIENT= [(1, 2, 1), (2, 1, 1), (2, 0, 2), (3, 1, 0), (1, 1, 2), (4, 0, 0), (1, 0, 3), (1, 3, 0), (3, 0, 1), (2, 2, 0)]
YELLOW_ORIENT = [(1, 2, 1), (2, 1, 1), (3, 0, 1), (2, 0, 2), (0, 3, 1), (0, 0, 4), (0, 1, 3), (3, 1, 0), (0, 4, 0), (4, 0, 0), (1, 1, 2), (1, 0, 3), (1, 3, 0), (0, 2, 2), (2, 2, 0)]

def make_rotate(cube_state, rot):
  rot = rot.upper()
  if rot not in ROT_MAP:
      return cube_state

  out = copy.deepcopy(cube_state)

  for src, dst in ROT_MAP[rot]:
      piece, ori = cube_state[src]
      out[dst] = [piece, ROT_ORIENT_MAP[rot][ori]]

  return out

def make_move(cube_state, move):
    move = move.upper()
    if move not in MOVE_MAP:
        return cube_state

    out = copy.deepcopy(cube_state)

    for src, dst in MOVE_MAP[move]:
        piece, ori = cube_state[src]
        out[dst] = [piece, ORIENT_MAP[move][ori]]

    return out

def hash_cube(cube_state):
  return tuple((corner[0], corner[1]) for corner in normalize_cube(cube_state))

def normalize_cube(cube_state):
  normalize_cube_state = copy.deepcopy(cube_state)
  while normalize_cube_state[0] != [0,0]:
    idx = 0
    for i in range(len(normalize_cube_state)):
      if normalize_cube_state[i][0] == 0:
        idx = i
        break
    if idx in [0,3,4,7] and normalize_cube_state[idx][1] == 1:
      normalize_cube_state = make_rotate(normalize_cube_state, "Z'")
    elif idx in [1,2,5,6] and normalize_cube_state[idx][1] == 1:
      normalize_cube_state = make_rotate(normalize_cube_state, "Z")
    elif idx in [0,1,4,5] and normalize_cube_state[idx][1] == 2:
      normalize_cube_state = make_rotate(normalize_cube_state, "X")
    elif idx in [2,3,6,7] and normalize_cube_state[idx][1] == 2:
      normalize_cube_state = make_rotate(normalize_cube_state, "X'")
    elif idx in [1,2,3] and normalize_cube_state[idx][1] == 0:
      normalize_cube_state = make_rotate(normalize_cube_state, "Y")
    elif idx in [4,5,6,7] and normalize_cube_state[idx][1] == 0:
      normalize_cube_state = make_rotate(normalize_cube_state, "X")
      normalize_cube_state = make_rotate(normalize_cube_state, "X")

  return normalize_cube_state

def tree_search(target_state):
  queue = deque([(starting_state, "", 0)])
  visited = set()
  target_hash = hash_cube(target_state)
  while queue:
    state, path, level = queue.popleft()
    if state == target_state:
      return path

    if level > 11:
      continue

    for move in MOVE_MAP:
      next_state = make_move(state, move)
      h = hash_cube(next_state)

      if h not in visited:
        if h == target_hash:
          return path + move
        visited.add(h)
        queue.append((next_state, path + move, level + 1))

def generate_shuffle():
  out = None
  while out is None or len(out) < 4:
    target = copy.deepcopy(starting_state)
    random.shuffle(target)
    for i in range(len(target)):
      target[i][1] = random.randint(0,2)
    if not valid_perm(target) or not valid_orient(target):
      continue
    out = tree_search(target)

  return out

def generate_scrambles(num_scrambles=1):
  out = []
  for _ in range(num_scrambles):
    out.append(generate_shuffle())

def gen_valid_things():
  w = set()
  y = set()
  for _ in range(100000):
    state = copy.deepcopy(starting_state)
    for _ in range(100):
      state = make_move(state, random.choice(list(MOVE_MAP)))

    state = normalize_cube(state)
    wt = [0] * 3
    yt = [0] * 3

    for piece in state:
      if piece[0] < 4:
        wt[piece[1]]+=1
      else:
        yt[piece[1]]+=1
    w.add((wt[0], wt[1], wt[2]))
    y.add((yt[0], yt[1], yt[2]))

  print(w, y)

def test_valid():
  state = copy.deepcopy(starting_state)

  for _ in range(10):
      state = make_move(state, random.choice(list(MOVE_MAP)))
      print(state)
      if not valid_perm(state) or not valid_orient(state):
        print(valid_perm(state), valid_orient(state))

def valid_perm(cube_state):
  return True

def valid_orient(cube_state):
  cube_state = normalize_cube(cube_state)
  wt = [0] * 3
  yt = [0] * 3

  for piece in cube_state:
    if piece[0] < 4:
      wt[piece[1]]+=1
    else:
      yt[piece[1]]+=1

  white = (wt[0], wt[1], wt[2])
  yellow = (yt[0], yt[1], yt[2])

  return white in WHITE_ORIENT and yellow in YELLOW_ORIENT

print(generate_scrambles())
