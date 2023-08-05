from enum import Enum
import copy

Action = Enum('Action', ['LEFT', 'RIGHT', 'DOWN', 'UP', 'SUCK'])


def env_trans(env, action):
    res = copy.deepcopy(env)
    if action == Action.UP and not at_the_top_border(env) and not blocked_from_above(env):
        res = move_up(env)
    elif action == Action.DOWN and not at_the_bottom_border(env) and not blocked_from_below(env):
        res = move_down(env)
    elif action == Action.RIGHT and not at_the_right_border(env) and not blocked_from_right(env):
        res = move_right(env)
    elif action == Action.LEFT and not at_the_left_border(env) and not blocked_from_left(env):
        res = move_left(env)
    elif action == Action.SUCK:
        res['clean'][res['position'][0], res['position'][1]] = 1.0
    elif blocked_from_above(env):
        res['agent blocked'][env['position'][0] + 1][env['position'][1]] = 0
    elif blocked_from_below(env):
        res['agent blocked'][env['position'][0] - 1][env['position'][1]] = 0
    elif blocked_from_right(env):
        res['agent blocked'][env['position'][0]][env['position'][1] + 1] = 0
    elif blocked_from_left(env):
        res['agent blocked'][env['position'][0]][env['position'][1] - 1] = 0
    return res


def at_the_top_border(env):
    return env['position'][0] == env['rows'] - 1


def at_the_bottom_border(env):
    return env['position'][0] == 0


def at_the_left_border(env):
    return env['position'][1] == 0


def at_the_right_border(env):
    return env['position'][1] == env['columns'] - 1


def blocked_from_above(env):
    return not at_the_top_border(env) and env['blocked'][env['position'][0] + 1, env['position'][1]]


def blocked_from_below(env):
    return not at_the_bottom_border(env) and env['blocked'][env['position'][0] - 1, env['position'][1]]


def blocked_from_right(env):
    return not at_the_right_border(env) and env['blocked'][env['position'][0], env['position'][1] + 1]


def blocked_from_left(env):
    return env['blocked'][env['position'][0], env['position'][1] - 1]


def change_pos(env, action):
    res = copy.deepcopy(env)
    action(res['position'])
    return res


def move_up(env):
    def f(x):
        x[0] += 1
    return change_pos(env, f)


def move_down(env):
    def f(x):
        x[0] -= 1
    return change_pos(env, f)


def move_right(env):
    def f(x):
        x[1] += 1
    return change_pos(env, f)


def move_left(env):
    def f(x):
        x[1] -= 1
    return change_pos(env, f)


def always_up(env):
    return Action.UP


def simulate(env, strategy, n_turn=1000):
    res = []
    for i in range(n_turn):
        env = env_trans(env, strategy(env))
        res.append(env)
    return res


def performance(path):
    return sum([x['clean'].sum() for x in path])

