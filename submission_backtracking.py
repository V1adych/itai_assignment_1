from collections import deque
from itertools import product


class BacktrackingAgent:
    def __init__(self, keymaker_position):
        self.keymaker_position = keymaker_position
        self.key_position = None
        self.danger_zones = set()
        self.current_position = (0, 0)
        self.n_moves = 0
        self.path = None
        self.path_ptr = 0

    # this method reads the observations from the environment
    def read_obs(self):
        n_obs = int(input())
        for _ in range(n_obs):
            line = input().split()
            if len(line) >= 3:
                y = int(line[0])
                x = int(line[1])
                obj = line[2]
                if obj in ["P", "A", "S"]:
                    self.danger_zones.add((x, y))
                if obj == "B":
                    self.key_position = (x, y)

    # this methods finds all legal moves from the current position
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

    # this method uses BFS to find possible path to the target
    def build_path(self, target):
        visited = set()
        queue = deque([(self.current_position, [])])
        while queue:
            pos, path = queue.popleft()
            if pos == target:
                self.path = path
                self.path_ptr = 0
                return
            visited.add(pos)
            for move in self.get_legal_moves(pos, visited):
                queue.append((move, path + [move]))

        self.path = None
        self.path_ptr = 0

    # this method is called on every new move.
    # it checks if the next move is in the danger zone.
    # if so, it backtracks to the previous position
    # and rebuilds the path
    def backtrack(self, next_move):
        if next_move in self.danger_zones:
            self.build_path(self.keymaker_position)
            return True
        return False

    # returns shorted distance from position (0, 0) to keymaker
    # taking into account all dangers stored in memory
    # uses dijkstra algorithm
    def get_shortest_distance(self):
        queue = deque([(0, (0, 0))])
        visited = set()
        while queue:
            cur_len, pos = queue.popleft()
            visited.add(pos)
            if pos == self.keymaker_position:
                return cur_len
            for move in self.get_legal_moves(pos, visited):
                queue.append((cur_len + 1, move))
        return -1

    # this method returns the next move from the path
    def get_next_move(self):
        if not self.path:
            return None
        if self.path_ptr >= len(self.path):
            return None
        next_move = self.path[self.path_ptr]
        self.path_ptr += 1
        return next_move

    # this method is called on every step
    # it reads the observations, builds the path
    def make_move(self):
        self.read_obs()
        if self.current_position == self.keymaker_position:
            return f"e {self.get_shortest_distance()}"

        if self.path is None:
            self.build_path(self.keymaker_position)

        next_move = self.get_next_move()

        if self.backtrack(next_move):
            next_move = self.get_next_move()
            if next_move is None:
                return "e -1"

        self.current_position = next_move
        self.n_moves += 1
        return f"m {next_move[1]} {next_move[0]}"


def main():
    # read the initial inputs
    obs_type = input()
    keymaker_y, keymaker_x = map(int, input().split())
    agent = BacktrackingAgent((keymaker_x, keymaker_y))
    print("m 0 0")
    # while agent is not done, make moves
    while True:
        move = agent.make_move()
        print(move)
        if move.startswith("e"):
            break


if __name__ == "__main__":
    main()
