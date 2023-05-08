class Environment:

    def __init__(self, dirty_a, dirty_b, location):
        self.dirty_a = dirty_a
        self.dirty_b = dirty_b
        self.location = location
        self.history = []

    def update(self, action):
        self.history.append((self.dirty_a, self.dirty_b, action))
        if self.location == 'A':
            if action == 'Right':
                self.location = 'B'
            elif action == 'Suck':
                self.dirty_a &= False
        if self.location == 'B':
            if action == 'Left':
                self.location = 'A'
            elif action == 'Suck':
                self.dirty_b &= False

    def performance(self):
        time_to_clean = 0
        for x in self.history:
            if not (x[0] or x[1]) or time_to_clean == -2:
                break
            time_to_clean -= 1
        return time_to_clean


def simple_reflex_agent(state):
    if state.location == 'A' and state.dirty_a or state.location == 'B' and state.dirty_b:
        return 'Suck'
    elif state.location == 'A':
        return 'Right'
    return 'Left'


def main():
    for dirty_a in [True, False]:
        for dirty_b in [True, False]:
            for location in ['A', 'B']:
                env = Environment(dirty_a, dirty_b, location)
                for i in range(3):
                    env.update(simple_reflex_agent(env))
                print(env.performance())
