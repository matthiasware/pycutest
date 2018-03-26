from pycutest.meta import PycutestMeta
from pycutest.meta import SolveResult
import pycutest
import numpy as np
from timeit import default_timer as timer
from scipy.optimize import minimize

meta = PycutestMeta()
conditions = {"isbounded": False, "isconstraint": False, "num_var": (1, 2)}
problems = meta.getProperties(problems=["AKIVA"]).keys()

results = {}
for i, problem in enumerate(problems):
    print("{}/{} - {}:".format(i, len(problems), problem), end='', flush=True)
    pycutstProblem = pycutest.PycutestProblem(problem, record=True)
    start = timer()
    res = minimize(pycutstProblem.fg, x0=pycutstProblem.var_init,
                   method='L-BFGS-B', jac=True,
                   options={'maxiter': 10000, 'disp': False})
    end = timer()
    elapsed = end - start
    print("success: {}, ellapsed: {}".format(res.success, elapsed))
    result = SolveResult(name=problem,
                         package="scipy",
                         method="L-BFGS-B",
                         solved=res.success,
                         elapsed=elapsed,
                         fvalue=res.fun,
                         gnorm=np.linalg.norm(res.jac, np.inf),
                         iterations=res.nit,
                         history=pycutstProblem.history)
    results[problem] = result
    meta.addResult(problem, result)
