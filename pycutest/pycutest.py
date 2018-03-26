from pycutest import meta
from pycutest import tools
# pycutest problem:
# - src id
# - setup.py check if previpus installation source changed
# - get properties from meta
# - load library only on demand
# - pycutest problems have a meta state + loaded library
# - instead of AKIVA.fg make AKIVA.get_fg().fg()
# - instead of AKIVA.h make AKIVA.get_h()
# - instead of AKIVA...
# - during setup delete meta?
# - during setup delete compiled code?
# - unittest

# todo
# - setup.py provide compile function
# - remake todo
# - setup.py provide compile meta macro
# - setup.py provide check version and pycutest.pxy source change
#   which is important for recompilation
#   setup.py verify_existing_build -> prints "outdated",
#   recompile or "uptodate"
# - setup.py provide create meta macto
# - in setup, coppy metafile to location
# - else warn user to create it himself
# - compile on demand

# bug with is_bounded

# AUTOCOMPILE FUNCTION !!!!


class Pycutest:
    _state = {}

    def __init__(self):
        self.__dict__ = self._state

        if "_meta" not in self.__dict__:
            self._meta = meta.Meta()
        if "_pycutest_problems" not in self.__dict__:
            self._pycutest_problems = self._meta.load()

    def getProblems(self,
                    problem_names=None,
                    bounded=None,
                    constraint=None,
                    num_var=None,
                    num_const=None,
                    aslist=False):
        if isinstance(problem_names, str):
            problem_names = [problem_names]
        if problem_names is None:
            problem_names = tools.getProblemNames(use_sloths=False)
        problems = [] if aslist else {}
        for name in problem_names:
            obj = self._pycutest_problems[name]
            if bounded is not None:
                if not obj.is_bounded == bounded:
                    continue
            if constraint is not None:
                if not obj.is_constraint == constraint:
                    continue
            if num_var is not None:
                if not obj.num_var == num_var:
                    continue
            if num_const is not None:
                if not obj.num_const == num_const:
                    continue
            if aslist:
                problems.append(obj)
            else:
                problems[name] = obj
        return problems
