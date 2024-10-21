from a_star import AStarAgent
from backtracking import BacktrackingAgent
from map_env import Environment
import time
import signal
import pandas as pd


class TimeoutException(Exception):
    pass


def timeout(seconds):
    def decorator(func):
        def _handle_timeout(signum, frame):
            raise TimeoutException(
                f"Function {func.__name__} timed out after {seconds} seconds"
            )

        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result

        return wrapper

    return decorator


def mean(lst):
    return sum(lst) / len(lst)


def var(lst):
    m = mean(lst)
    return sum([(x - m) ** 2 for x in lst]) / len(lst)


def std(lst):
    return var(lst) ** 0.5


@timeout(1)
def run_experiment(agent, env):
    obs = env.reset()
    agent.initialize(env)
    done = False
    n_moves = 0
    start_t = time.time()
    try:
        while not done:
            action = agent.step(obs)
            n_moves += 1
            done = type(action) is str
            if done:
                break
            else:
                obs = env.step(action)
    except Exception:
        action = "e -1"
    end_t = time.time()

    exec_time = end_t - start_t
    if action.endswith("-1"):
        win = 0
    else:
        win = 1

    return exec_time, win, n_moves


def run_experiments(exp_id, agent, env, n_experiments):
    exec_times = []
    wins = []
    moves_count = []
    for _ in range(n_experiments):
        exec_time, win, n_moves = run_experiment(agent, env)
        wins.append(win)
        exec_times.append(exec_time)
        moves_count.append(n_moves)

    return {
        "exp_id": exp_id,
        "mean_exec_time": mean(exec_times),
        "std_exec_time": std(exec_times),
        "var_exec_time": var(exec_times),
        "mean_moves": mean(moves_count),
        "std_moves": std(moves_count),
        "var_moves": var(moves_count),
        "win_fraction": mean(wins),
    }


def main():
    env = Environment()
    a_star_agent = AStarAgent()
    backtracking_agent = BacktrackingAgent()

    a_star_data = run_experiments("a_star", a_star_agent, env, 1000)
    backtracking_data = run_experiments("backtracking", backtracking_agent, env, 1000)

    df = pd.DataFrame([a_star_data, backtracking_data]).T
    df.to_csv("results.csv", index=True, header=False)


if __name__ == "__main__":
    main()
