"""
@Auth ： shuo tang
@Email:  tansh643@student.otago.ac.nz
@Time ： 2024/8/5 20:44
"""
import unittest

from my_agent import GameHandler


class TestCalculator(unittest.TestCase):

    def test_binding_on_positive(self):
        self.handler = GameHandler(2, [1, 2, 3], [1, 2, 3], 2, [1, 2, 3], config_dic={
            "enable_search_limit": False,
            "enable_alpha_beta_pruning": False,
            "search_limit_num": 1})
        self.assertEqual(self.handler.compute_score(100, 10), 2)
        self.assertEqual(self.handler.compute_score(10, 100), -2)
        self.assertEqual(self.handler.compute_score(0, 100), -2)
        self.assertEqual(self.handler.compute_score(100, 0), 2)
        self.assertEqual(self.handler.compute_score(100, 100), 0)
        self.assertEqual(self.handler.compute_score(0, 0), 0)

    def test_binding_on_negative(self):
        self.handler = GameHandler(-2, [1, 2, 3], [1, 2, 3], 2, [1, 2, 3], config_dic={
            "enable_search_limit": False,
            "enable_alpha_beta_pruning": False,
            "search_limit_num": 1})
        self.assertEqual(self.handler.compute_score(100, 10), 2)
        self.assertEqual(self.handler.compute_score(10, 100), -2)
        self.assertEqual(self.handler.compute_score(0, 100), -2)
        self.assertEqual(self.handler.compute_score(100, 0), 2)
        self.assertEqual(self.handler.compute_score(100, 100), 0)
        self.assertEqual(self.handler.compute_score(0, 0), 0)


if __name__ == '__main__':
    unittest.main()
