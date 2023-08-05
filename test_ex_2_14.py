from unittest import TestCase
import numpy
import ex_2_14


class Test(TestCase):

    def setUp(self) -> None:
        self.env = {'columns': 2, 'rows': 2, 'blocked': numpy.zeros((2, 2)), 'clean': numpy.zeros((2, 2)),
                    'agent blocked': numpy.zeros((2, 2))}
        self.env['blocked'][0, 0] = 1

    def test_env_trans_up(self):

        self.env['position'] = [1, 0]
        env = ex_2_14.env_trans(self.env, ex_2_14.Action.UP)
        self.assertEqual(env['position'], [1, 0])

        self.env['position'] = [0, 1]
        env = ex_2_14.env_trans(self.env, ex_2_14.Action.UP)
        self.assertEqual(env['position'], [1, 1])

        self.env['position'] = [0, 1]
        env = ex_2_14.env_trans(self.env, ex_2_14.Action.UP)
        self.assertEqual(env['position'], [1, 1])

    def test_env_trans_down(self):

        self.env['position'] = [0, 1]
        env = ex_2_14.env_trans(self.env, ex_2_14.Action.DOWN)
        self.assertEqual(env['position'], self.env['position'])

        self.env['position'] = [1, 0]
        env = ex_2_14.env_trans(self.env, ex_2_14.Action.DOWN)
        self.assertEqual(env['position'], self.env['position'])

        self.env['position'] = [1, 1]
        env = ex_2_14.env_trans(self.env, ex_2_14.Action.DOWN)
        self.assertEqual(env['position'], [0, 1])

    def test_env_trans_right_at_the_border(self):
        self.env['position'] = [1, 1]
        env = ex_2_14.env_trans(self.env, ex_2_14.Action.RIGHT)
        self.assertEqual(env['position'], self.env['position'])

    def test_env_trans_right_at_the_obstacle(self):
        self.env['blocked'][1, 1] = 1
        self.env['position'] = [1, 0]
        env = ex_2_14.env_trans(self.env, ex_2_14.Action.RIGHT)
        self.assertEqual(env['position'], self.env['position'])
        self.env['blocked'][1, 1] = 0

    def test_env_trans_right_can_move(self):
        self.env['position'] = [1, 0]
        env = ex_2_14.env_trans(self.env, ex_2_14.Action.RIGHT)
        self.assertEqual(env['position'], [1, 1])

    def test_env_trans_left_at_the_border(self):
        self.env['position'] = [1, 0]
        env = ex_2_14.env_trans(self.env, ex_2_14.Action.LEFT)
        self.assertEqual(env['position'], self.env['position'])

    def test_env_trans_left_at_the_obstacle(self):
        self.env['position'] = [0, 1]
        env = ex_2_14.env_trans(self.env, ex_2_14.Action.LEFT)
        self.assertEqual(env['position'], self.env['position'])

    def test_env_trans_left_can_move(self):
        self.env['position'] = [1, 1]
        env = ex_2_14.env_trans(self.env, ex_2_14.Action.LEFT)
        self.assertEqual(env['position'], [1, 0])

    def test_default_action(self):
        self.assertEqual(ex_2_14.always_up(self.env), ex_2_14.Action.UP)

    def test_env(self):
        self.env['position'] = [0, 1]
        path = ex_2_14.simulate(self.env, ex_2_14.always_up, 2)
        self.assertEqual(path[-1]['position'], [1, 1])

    def test_performance(self):
        self.env['position'] = [0, 1]
        path = ex_2_14.simulate(self.env, ex_2_14.always_up, 2)
        self.assertEqual(ex_2_14.performance(path), 0)

    def test_suck(self):
        self.env['position'] = [0, 1]
        env = ex_2_14.env_trans(self.env, ex_2_14.Action.SUCK)
        self.assertEqual((env['clean'][0, 1]), 1.0)

