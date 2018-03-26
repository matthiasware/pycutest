import pycutest
from timeit import default_timer as timer
import csv

"""
  This script classifies the CUTEST problems via PROPERTIES
  Does not consider the problems in pycutest.SLOTHS for obvious reasons
"""

PROPERTIES_FILE = "problem_properties.csv"
PROPERTIES = ['name', 'num_var', 'num_const',
              'isconstraint', 'isbounded', 'importtime']


def writePropsToFile(properties, fieldnames, file):
    with open(file, 'w') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        list(map(writer.writerow, properties))


def getProblemProperties(problem, verbose=True):
    start = timer()
    p = pycutest.PycutestProblem(problem)
    end = timer()
    ellapsed = end - start
    properties = {'name': p.name,
                  'num_var': p.num_var,
                  'num_const': p.num_const,
                  'isconstraint': p.isconstraint,
                  'isbounded': p.isbounded,
                  'importtime': ellapsed}
    if verbose:
        print(p.name, ellapsed)
    return properties


problems = sorted(pycutest.getProblemNames())
problems = [p for p in problems if p not in pycutest.SLOTHS]

problems_properties = list(map(getProblemProperties, problems))
writePropsToFile(problems_properties, PROPERTIES, PROPERTIES_FILE)
