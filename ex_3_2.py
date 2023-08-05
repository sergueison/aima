from copy import deepcopy
from dataclasses import dataclass
from enum import auto, Enum
from typing import Any

import numpy as np

from algorithms.search import breadth_first_search


@dataclass
class Problem:
    initial: Any

    def action_cost(self, new_state, action, old_state):
        return 1


@dataclass
class GlassBoxes(Problem):

    def actions(self, state):
        return [i + 1 for (i, unlocked) in list(enumerate(state))[:-1] if unlocked]

    def result(self, state, action):
        my_state = list(state)
        my_state[action] = True
        return tuple(my_state)

    def is_goal(self, state):
        return state[5]


class Sequence(Problem):

    @staticmethod
    def actions(state):
        return [i for i in range(len(state) - 1)
                if state[i: i + 2] in ['AC', 'AB', 'BB'] or state[i] == 'E']

    @staticmethod
    def result(self, state, action):
        if state[action: action + 2] in ['AC', 'BB']:
            return state[:action] + 'E' + state[action + 2:]
        elif state[action: action + 2] == 'AB':
            return state[:action] + 'BC' + state[action + 3:]
        else:
            return state[:action] + state[action + 1:]

    @staticmethod
    def is_goal(self, state):
        return state == 'E'


class Paint:
    pass


class Direction(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()


@dataclass
class Move:
    direction: Direction


def move_position(position, direction):
    if direction == Direction.UP:
        res = position[0] + 1, position[1]
    elif direction == Direction.DOWN:
        res = position[0] - 1, position[1]
    elif direction == Direction.LEFT:
        res = position[0], position[1] - 1
    else:
        res = position[0], position[1] + 1
    return res


@dataclass
class GridState:

    painted: np.ndarray
    position: tuple[int]

    def can_move(self, direction, grid_size, pit):
        candidate_position = move_position(self.position, direction)
        return (0 <= candidate_position[0] < grid_size  and 0 <= candidate_position[1] < grid_size and
                not pit[candidate_position])

    def __hash__(self):
        return hash((self.painted.tobytes(), self.position))


@dataclass
class Grid(Problem):

    pit: np.ndarray
    grid_size: int = 0

    def __post_init__(self):
        assert len(self.pit.shape) == 2
        assert self.pit.shape[0] == self.pit.shape[1]
        self.grid_size = self.pit.shape[0]

    def actions(self, state):
        return [Paint()] + [Move(direction) for direction in Direction if
                            state.can_move(direction, self.grid_size, self.pit)]

    @staticmethod
    def result(state, action):
        res = deepcopy(state)
        if isinstance(action, Paint):
            res.painted[state.position] = True
        else:
            position = list(state.position)
            if action.direction == Direction.UP:
                position[0] += 1
            elif action.direction == Direction.DOWN:
                position[0] -= 1
            elif action.direction == Direction.LEFT:
                position[1] -= 1
            else:
                position[1] += 1
            res.position = tuple(position)
        return res

    def is_goal(self, state):
        return np.all(np.logical_or(self.pit, state.painted))


@dataclass
class ContainerShipState:

    remaining_containers: np.ndarray = np.ones((13, 13)) * 5


class ContainerShip(Problem):
    pass


if __name__ == '__main__':
    # glass_boxes = GlassBoxes((True,) + (False,) * 5)
    # solution = breadth_first_search(glass_boxes)
    # solution = breadth_first_search(Sequence('ABABAECC'))
    solution = breadth_first_search(
        Grid(pit=np.array([[False, True], [True, False]]),
             initial=GridState(painted=np.array([[True, False], [False, False]]), position=(0, 0))))
    n = solution
    if n:
        print(n.state)
        while n.parent:
            print(n.action)
            n = n.parent
            print(n.state)
    else:
        print('No solution.')

