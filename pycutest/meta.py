from pycutest.problem import PycutestProblem
from pycutest import tools
from pycutest import settings
from pycutest.sloth import SLOTHS
import os
import json


class Meta:
    _properties = {'problem_name', 'num_var',
                   'num_const', 'is_bounded',
                   'is_constraint'}

    def __init__(self):
        self.path = tools.getEnvironmentVariable(settings.env_mypycutest)
        self.path = os.path.join(self.path, settings.file_meta)

    def dump(self, pycutest_problems, overwrite=False):
        problems = self._loadJSON() if not overwrite else {}
        for name, prob in pycutest_problems.items():
            jp = {prop: getattr(prob, prop) for prop in self._properties}
            problems[prob.problem_name] = jp
        with open(self.path, "w") as file:
            json.dump(problems, file)

    def load(self):
        if os.path.exists(self.path):
            pycutest_problems = self._loadProblemsFromJSON()
        else:
            pycutest_problems = self._loadProblemsFromSIF()
            self.dump(pycutest_problems, True)
        return pycutest_problems

    def _loadProblemsFromJSON(self):
        jsonProblems = self._loadJSON()
        pycutest_problems = {}
        for k, v in jsonProblems.items():
            problem = PycutestProblem()
            for prop in self._properties:
                setattr(problem, prop, v[prop])
            pycutest_problems[k] = problem
        return pycutest_problems

    def _loadJSON(self):
        with open(self.path, "r") as file:
            data = json.load(file)
        return data

    def _loadProblemsFromSIF(self):
        problem_names = tools.getProblemNames()
        if settings.exclude_sloth:
            problem_names = [p for p in problem_names if p not in set(SLOTHS)]
        return {name: PycutestProblem(name) for name in problem_names}
