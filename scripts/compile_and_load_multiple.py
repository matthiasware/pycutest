import pycutest

path = "/tmp"
problems = ["AKIVA", "AGG", "3PK", "A0ENDNDL"]

# compiles problems to path
pycutest.compile(problems, path=path, verbose=True, parallel=True)

# load compiled problems
pycutestProblems = pycutest.loadProblems(problems, path)
