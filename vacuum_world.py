class Environment:

    def __init__(self, dirtyA, dirtyB, location):
        self.dirtyA = dirtyA
        self.dirtyB = dirtyB
        self.location = location
        self.history = []

    def update(self, action):
        self.history.append((self.dirtyA, self.dirtyB, action))
        if self.location == 'A':
            if action == 'Right':
                self.location = 'B'
            elif action == 'Suck':
                self.dirtyA &= False
        if self.location == 'B':
            if action == 'Left':
                self.location = 'A'
            elif action == 'Suck':
                self.dirtyB &= False

    def performance(self):
        len = 0
        for x in self.history:
            if not (x[0] or x[1]) or len == -2:
                break
            len -= 1
        return len


def simple_reflex_agent(state):
    if state.location == 'A' and state.dirtyA or state.location == 'B' and state.dirtyB:
        return 'Suck'
    elif state.location == 'A':
        return 'Right'
    return 'Left'


def main():
    for dirtyA in [True, False]:
        for dirtyB in [True, False]:
            for location in ['A', 'B']:
                env = Environment(dirtyA, dirtyB, location)
                for i in range(3):
                    env.update(simple_reflex_agent(env))
                print(env.performance())
