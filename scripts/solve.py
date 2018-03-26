import pycutest
from scipy.optimize import minimize

# requires previous compilation
pyc = pycutest.Pycutest()
AKIVA = pyc.getProblems("AKIVA")["AKIVA"]

res = minimize(AKIVA.fg, x0=AKIVA.var_init, method='Newton-CG', jac=True,
               hess=AKIVA.h, options={'maxiter': 1000, 'disp': False})
print(res)
