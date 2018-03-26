import pycutest as pyc
import unittest
import expectations
import os
import numpy as np


# goto tmp
# todo clean repository


class PycutestProblem(unittest.TestCase):
    # unbound unconstraint
    # bounded unconstraint
    # unbounded constraint
    # bounded constraint
    # take values from ipopt for
    # var_init
    # h
    # f,g
    # bounds
    # ...

    def __init__(self, *args, **kwargs):
        super(PycutestProblem, self).__init__(*args, **kwargs)
        self.path_wd = os.getcwd()
        self.path_tmp = "/tmp"
        self.snail = expectations.snail

    def setUp(self):
        os.chdir(self.path_tmp)

    def tearDown(self):
        os.chdir(self.path_wd)

    def test_uu_snail(self):
        p = pyc.problem.PycutestProblem()
        p.problem_name = "SNAIL"
        p.module_dir_path = self.path_tmp

        # build problem
        p._build(verbose=True)

        # load problem
        p._load()

        # check properties
        self.assertEqual(p.num_var, 2)
        self.assertEqual(p.num_const, 0)
        self.assertEqual(p.is_bounded, self.snail.is_bounded)
        self.assertEqual(p.is_constraint, self.snail.is_constraint)
        np.testing.assert_allclose(p.var_init, self.snail.x0)
        f, g = p.fg(p.var_init)
        np.testing.assert_almost_equal(f, self.snail.fx0, 5)
        np.testing.assert_allclose(g, self.snail.gx0)
        h = p.h(p.var_init)
        np.testing.assert_allclose(h, self.snail.hx0)
        np.testing.assert_array_equal(p.var_bounds_l, self.snail.var_bounds_l)
        np.testing.assert_array_equal(p.var_bounds_u, self.snail.var_bounds_u)


if __name__ == '__main__':
    unittest.main()
