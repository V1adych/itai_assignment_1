import heapq
from itertools import product


class AStarAgent:
    def __init__(self, keymaker_position):
        self.keymaker_position = keymaker_position
        self.key_position = None
        self.danger_zones = set()
        self.current_position = (0, 0)
        self.n_moves = 0

    # this method is called on each iteration to read observations
    def read_obs(self):
        n_obs = int(input())
        for _ in range(n_obs):
            line = input().split()
            if len(line) >= 3:
                y = int(line[0])
                x = int(line[1])
                obj = line[2]
                # we treat all types of enemy as danger zones
                if obj in ["P", "A", "S"]:
                    self.danger_zones.add((x, y))
                # write position of the key if it is found
                if obj == "B":
                    self.key_position = (x, y)

    # this method calculates Manhattan distance between two points
    def get_distance(self, start, target):
        return abs(start[0] - target[0]) + abs(start[1] - target[1])

    # this method returns all legal moves from the current position
    # that are not in the danger zone and not visited
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

    # implementation of A* algorithm
    # uses Manhattan distance as heuristic
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

    # this method is used to get agent move based on results of A* search
    def make_move(self):
        self.read_obs()
        next_move = self.a_star(self.keymaker_position)
        if self.current_position == self.keymaker_position:
            return f"e {self.n_moves}"
        if next_move is None:
            return "e -1"
        self.current_position = next_move
        self.n_moves += 1
        return f"m {next_move[1]} {next_move[0]}"


def main():
    # read initial input
    obs_type = input()
    keymaker_y, keymaker_x = map(int, input().split())
    agent = AStarAgent((keymaker_x, keymaker_y))
    print("m 0 0")
    # while agents is not done, make moves
    while True:
        move = agent.make_move()
        print(move)
        if move.startswith("e"):
            break


if __name__ == "__main__":
    main()
