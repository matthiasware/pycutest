import pycutest
import os

# Compile and Load Problem
# binaries are stored in /tmp
AGG = pycutest.PycutestProblem()
AGG.compileAndLoad("AGG")

# Compiles and loads problem, path is provided
# s.t. we dont need to recompile it the next time
path = os.path.join("/tmp", "AKIVA")

AKIVA = pycutest.PycutestProblem()
AKIVA.compileAndLoad("AKIVA", path)

# in the next session, you can use it without a preceding compilation
AKIVA = pycutest.PycutestProblem("AKIVA", path)
