import pycutest
import numpy as np

problem_name = "DANWOOD"
pyc = pycutest.Pycutest()

p = pyc.getProblems(problem_name)[problem_name]
# p._build(verbose=True)

x = np.array([-0.06298852, 3.78519558])
# print(x, p.c(x))
# x = np.array([1, -3.7])
# print(x, p.c(x))
print("x", "c(x)")
print(x, p.c2(x))
print(-1 * x, p.c(-1 * x))
z = np.copy(x)
z[0] *= -1
print(z, p.c(x))
z = np.copy(x)
z[1] *= -1
print(z, p.c(x))
