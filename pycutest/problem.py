import numpy as np
from pycutest import tools
from pycutest.compiler import SIFCompiler


class PycutestProblem():
    def __init__(self, problem_name=None):
        # module properties
        self._cutest_problem = None     # @property
        self._module_name = None        # @property
        self._module_dir_path = None    # @property

        # recored function calls
        self.record_fg = False
        self.record_h = False
        self.history_fg = []
        self.history_h = []

        # problem properties
        self.problem_name = problem_name
        self._is_bounded = None         # @property
        self._is_constraint = None      # @property
        self._var_init = None           # @property
        self._num_var = None            # @property
        self._num_const = None          # @property
        self._var_bounds_l = None       # @property
        self._var_bounds_u = None       # @property
        self._multipliers_init = None   # @property
        self._is_const_linear = None    # @property
        self._is_const_equality = None  # @property
        self._const_bounds_l = None     # @property
        self._const_bounds_u = None     # @property
        # self._is_const_bounded = None   # @property

    def _build(self, problem_name=None, module_dir_path=None, verbose=False):
        if problem_name:
            self.problem_name = problem_name
        if module_dir_path:
            self.module_dir_path = module_dir_path
        SIFCompiler().buildModule(self.problem_name,
                                  self.module_dir_path,
                                  verbose)
        return self

    def _load(self, module_name=None, module_dir_path=None):
        '''loads precompiled problem as module'''

        if module_name:
            self.module_name = module_name
        if module_dir_path:
            self.module_dir_path = module_dir_path
        self._cutest_problem = tools.loadCutestProblem(self.module_name,
                                                       self.module_dir_path)

        p = self.cutest_problem.getProperties()
        self.__dict__.update({'_{}'.format(k): v for k, v in p.items()})
        return self

    def fg(self, x):
        if not self.is_constraint:
            f, g = self.cutest_problem.cutest_uofg(x)
        else:
            f, g = self.cutest_problem.cutest_cofg(x)
        if self.record_fg:
            self.history_fg.append((np.copy(x), np.copy(f), np.copy(g)))
        return f, g

    def h(self, x, y=None):
        if y is None:
            H = self.cutest_problem.cutest_udh(x)
        else:
            H = self.cutest_problem.cutest_cdh(x, y)
        if self.record_h:
            self.history_h.append((np.copy(x), H))
        return H

    def c2(self, x):
        return self.cutest_problem.cutest_cfn(x)

    def c(self, x, grad=False):
        return self.cutest_problem.cutest_ccfg(x, grad=grad)

    def cjprod(self, x, v, transpose=False):
        y = self.cutest_problem.cutest_cjprod(x, v, transpose)
        return y

    # @property
    # def is_const_bounded(self):
    #     if self._is_const_bounded is None:
    #         bl = False
    #         bu = False
    #         if len(self.const_bounds_l):
    #             bl = (self.const_bounds_l != -np.inf).any()
    #         if len(self.const_bounds_u):
    #             bu = (self.const_bounds_u != np.inf).any()
    #         self._is_const_bounded = bool(bl or bu)
    #     return self._is_const_bounded

    # @is_const_bounded.setter
    # def is_const_bounded(self, is_const_bounded):
    #     self._is_const_bounded = is_const_bounded

    @property
    def const_bounds_u(self):
        if self._const_bounds_u is None:
            self._load()
        return self._const_bounds_u

    @const_bounds_u.setter
    def const_bounds_u(self, const_bounds_u):
        self._const_bounds_u = const_bounds_u

    @property
    def const_bounds_l(self):
        if self._const_bounds_l is None:
            self._load()
        return self._const_bounds_l

    @const_bounds_l.setter
    def const_bounds_l(self, const_bounds_l):
        self._const_bounds_l = const_bounds_l

    @property
    def is_const_equality(self):
        if self._is_const_equality is None:
            self._load()
        return self._is_const_equality

    @is_const_equality.setter
    def is_const_equality(self, is_const_equality):
        self._is_const_equality = is_const_equality

    @property
    def is_const_linear(self):
        if self._is_const_linear is None:
            self._load()
        return self._is_const_linear

    @is_const_linear.setter
    def is_const_linear(self, is_const_linear):
        self._is_const_linear = is_const_linear

    @property
    def multipliers_init(self):
        if self._multipliers_init is None:
            self._load()
        return self._multipliers_init

    @multipliers_init.setter
    def multipliers_init(self, multipliers_init):
        self._multipliers_init = multipliers_init

    @property
    def var_bounds_u(self):
        if self._var_bounds_u is None:
            self._load()
        return self._var_bounds_u

    @var_bounds_u.setter
    def var_bounds_u(self, var_bounds_u):
        self._var_bounds_u = var_bounds_u

    @property
    def var_bounds_l(self):
        if self._var_bounds_l is None:
            self._load()
        return self._var_bounds_l

    @var_bounds_l.setter
    def var_bounds_l(self, var_bounds_l):
        self._var_bounds_l = var_bounds_l

    @property
    def num_const(self):
        if self._num_const is None:
            self._load()
        return self._num_const

    @num_const.setter
    def num_const(self, num_const):
        self._num_const = num_const

    @property
    def num_var(self):
        if self._num_var is None:
            self._load()
        return self._num_var

    @num_var.setter
    def num_var(self, num_var):
        self._num_var = num_var

    @property
    def is_constrait(self):
        if self._is_constraint is None:
            self._is_constraint = self.num_const > 0
        return self._is_constraint

    @is_constrait.setter
    def is_constraint(self, is_constrait):
        self._is_constraint = is_constrait

    @property
    def var_init(self):
        if self._var_init is None:
            self._load()
        return self._var_init

    @var_init.setter
    def var_init(self, var_init):
        self._var_init = var_init

    @property
    def is_bounded(self):
        if self._is_bounded is None:
            bl = (self.var_bounds_l != -np.inf).any()
            bu = (self.var_bounds_u != np.inf).any()
            self._is_bounded = bool(bl | bu)

        return self._is_bounded

    @is_bounded.setter
    def is_bounded(self, is_bounded):
        self._is_bounded = is_bounded

    @property
    def cutest_problem(self):
        if not self._cutest_problem:
            self._load()
        return self._cutest_problem

    @cutest_problem.setter
    def cutest_problem(self, cutest_problem):
        self._cutest_problem = cutest_problem

    @property
    def module_name(self):
        if not self._module_name:
            self._module_name = tools.getModuleName(self.problem_name)
        return self._module_name

    @module_name.setter
    def module_name(self, module_name):
        self._module_name = module_name

    @property
    def module_dir_path(self):
        if not self._module_dir_path:
            self.module_dir_path = tools.getModuleDirPath(self.problem_name)
        return self._module_dir_path

    @module_dir_path.setter
    def module_dir_path(self, module_dir_path):
        self._module_dir_path = module_dir_path

    def __hash__(self):
        pass

    def __str__(self):
        return ("PycutestProblem('{}',"
                "bounded={},"
                "constraint={},"
                "num_var={},"
                "num_const={})").format(self.problem_name,
                                        self.is_bounded,
                                        self.is_constraint,
                                        self.num_var,
                                        self.num_const)

    __repr__ = __str__
