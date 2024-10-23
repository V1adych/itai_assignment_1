import heapq
from itertools import product


class AStarAgent:
    def __init__(self):
        self.keymaker_position = None
        self.key_position = None
        self.danger_zones = set()
        self.current_position = (0, 0)
        self.n_moves = 0

    def initialize(self, env):
        self.keymaker_position = env.keymaker_position
        self.key_position = None
        self.danger_zones = set()
        self.current_position = (0, 0)
        self.n_moves = 0

    def read_obs(self, obs):
        for i in range(len(obs)):
            line = obs[i]
            if len(line) >= 3:
                x = int(line[0])
                y = int(line[1])
                obj = line[2]
                if obj in ["P", "A", "S"]:
                    self.danger_zones.add((x, y))
                if obj == "B":
                    self.key_position = (x, y)

    def get_distance(self, start, target):
        return abs(start[0] - target[0]) + abs(start[1] - target[1])

    def get_legal_moves(self, position, visited):
        moves = []
        for i, j in product([-1, 0, 1], repeat=2):
            if abs(i) + abs(j) > 1:
                continue
            new_position = (position[0] + i, position[1] + j)
            if new_position in self.danger_zones:
                continue
            if new_position[0] < 0 or new_position[1] < 0:
                continue
            if new_position[0] > 8 or new_position[1] > 8:
                continue
            if new_position in visited:
                continue
            moves.append(new_position)
        return moves

    def a_star(self, target):
        visited = set()
        if self.current_position == target:
            return None
        queue = [
            (
                self.get_distance(self.current_position, target),
                0,
                self.get_distance(self.current_position, target),
                self.current_position,
                [],
            )
        ]

        while queue:
            _, cur_len, _, pos, path = heapq.heappop(queue)
            visited.add(pos)
            if pos == target:
                return path[0]

            for move in self.get_legal_moves(pos, visited):
                heapq.heappush(
                    queue,
                    (
                        cur_len + 1 + self.get_distance(move, target),
                        cur_len + 1,
                        self.get_distance(move, target),
                        move,
                        path + [move],
                    ),
                )

        return None

    def step(self, obs):
        self.read_obs(obs)
        next_move = self.a_star(self.keymaker_position)
        if self.current_position == self.keymaker_position:
            return f"e {self.n_moves}"
        if next_move is None:
            return "e -1"
        self.current_position = next_move
        self.n_moves += 1
        return next_move
