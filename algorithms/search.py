from dataclasses import dataclass
from queue import Queue
from typing import Any


@dataclass
class Node:
    state: Any
    parent: Any = None
    action: Any = None
    path_cost: float = 0


def expand(problem, node):
    s = node.state
    for action in problem.actions(s):
        my_s = problem.result(s, action)
        cost = node.path_cost + problem.action_cost(s, action, my_s)
        yield Node(my_s, node, action, cost)


def breadth_first_search(problem):
    node = Node(problem.initial)
    if problem.is_goal(node.state):
        return node
    frontier = Queue()
    frontier.put(node)
    reached = {hash(problem.initial)}
    while not frontier.empty():
        node = frontier.get()
        for child in expand(problem, node):
            s = child.state
            if problem.is_goal(s):
                return child
            if hash(s) not in reached:
                reached.add(hash(s))
                frontier.put(child)



