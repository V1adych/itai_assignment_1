import random
from itertools import product


def moore_distance(x1, y1, x2, y2):
    return max(abs(x1 - x2), abs(y1 - y2))


def manhattan_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


class Environment:
    def __init__(self, agent_perception_range=1):
        self.agent_perception_range = agent_perception_range
        self.grid_size = 9
        self.grid = [[0] * self.grid_size for _ in range(self.grid_size)]
        self.taken_positions = []

        self.keymaker_position = self.place_entity("K")
        self.agent_position = (0, 0)
        self.grid[0][0] = "N"
        self.taken_positions.append(self.agent_position)

        self.n_agents = random.randint(3, 3)
        for _ in range(self.n_agents):
            agent_position = self.place_entity(
                "A", distance_check=moore_distance, min_distance=1
            )
            self.mark_surroundings(agent_position, "P", moore=True)

        self.place_entity("S", distance_check=manhattan_distance, min_distance=1)
        self.sentinel_position = self.taken_positions[-1]
        self.mark_surroundings(self.taken_positions[-1], "P", moore=False)

        self.place_entity("B", distance_check=manhattan_distance, min_distance=1)

    def place_entity(self, entity, distance_check=None, min_distance=0):
        x, y = self.get_random_position()
        while distance_check and any(
            distance_check(x, y, pos[0], pos[1]) <= min_distance
            for pos in self.taken_positions
        ):
            x, y = self.get_random_position()
        self.grid[x][y] = entity
        position = (x, y)
        self.taken_positions.append(position)
        return position

    def get_random_position(self):
        return random.randint(0, self.grid_size - 1), random.randint(
            0, self.grid_size - 1
        )

    def mark_surroundings(self, position, mark, moore):
        x, y = position
        directions = (
            product(range(-1, 2), range(-1, 2))
            if moore
            else [(0, 1), (0, -1), (1, 0), (-1, 0)]
        )
        for dx, dy in directions:
            if (dx, dy) == (0, 0):
                continue
            if (
                0 <= x + dx < self.grid_size
                and 0 <= y + dy < self.grid_size
                and self.grid[x + dx][y + dy] == 0
            ):
                self.grid[x + dx][y + dy] = mark
                
                

    def step(self, new_agent_position):
        if manhattan_distance(*new_agent_position, *self.agent_position) > 1:
            raise ValueError

        self.move_agent(new_agent_position)
        x, y = new_agent_position
        obs = self.get_obs((x, y))
        return obs
    
    def get_obs(self, pos):
        x, y = pos
        obs = []
        for dx, dy in product(range(-1, 2), range(-1, 2)):
            if 0 <= x + dx < self.grid_size and 0 <= y + dy < self.grid_size and self.grid[x + dx][y + dy] != 0 and (dx != 0 or dy != 0): 
                obs.append([x + dx, y + dy, self.grid[x + dx][y + dy]])
                
        return obs

    def reset(self):
        self.__init__()
        return self.get_obs((0, 0))

    def move_agent(self, new_agent_position):
        x, y = self.agent_position
        self.grid[x][y] = 0
        self.agent_position = new_agent_position
        new_x, new_y = new_agent_position

        if self.grid[new_x][new_y] in ["P", "S", "A"]:
            raise ValueError

        if self.grid[new_x][new_y] == "B":
            self.remove_agents()
            self.extend_sentinel_perception()

        self.grid[new_x][new_y] = "N"

    def remove_agents(self):
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                if self.grid[x][y] in ["A", "P"]:
                    self.grid[x][y] = 0

    def extend_sentinel_perception(self):
        sent_x, sent_y = self.sentinel_position
        for pos in [
            (sent_x - 1, sent_y),
            (sent_x + 1, sent_y),
            (sent_x, sent_y - 1),
            (sent_x, sent_y + 1),
        ]:
            if 0 <= pos[0] < self.grid_size and 0 <= pos[1] < self.grid_size:
                self.mark_surroundings(pos, "P", moore=False)

    def display(self):
        print("-"*17)
        for row in self.grid:
            print(" ".join(map(str, row)))
        print("-"*17)
