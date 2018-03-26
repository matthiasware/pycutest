from pycutest import settings
from pycutest.sloth import SLOTHS
import importlib
import os
import sys

# no smart behaviour here


def getModuleName(problem_name):
    return "M_" + problem_name.replace("-", "_")


def getProblemName(module_name):
    return module_name[:2].replace("-", "-")


def getEnvironmentVariable(name):
    var = os.getenv(name)
    if var is None:
        errmsg = ("Missing environment"
                  "variable '%s'" % name)
        raise ValueError(errmsg)
    return var


def getModuleDirPath(problem_name):
    path = getEnvironmentVariable(settings.env_mypycutest)
    path = os.path.join(path, problem_name)
    return path


def getProblemPath(name):
    path = getEnvironmentVariable(settings.env_mypycutest)
    path = os.path.join(path, name)
    return path


def getProblemNames(path=None, use_sloths=False):
    if path is None:
        path = getEnvironmentVariable(settings.env_mastsif)
    names = [file[:-4] for file in os.listdir(path) if file[-4:] == ".SIF"]
    names.sort()
    if not use_sloths:
        names = [name for name in names if name not in set(SLOTHS)]
    return names


def loadCutestProblem(module_name, module_dir_path):
    if '.' not in sys.path:
        sys.path.append(".")
    wd = os.getcwd()
    os.chdir(module_dir_path)
    problem_name = getProblemName(module_name).encode("UTF-8")
    cutest_module = importlib.import_module(module_name)
    cutest_object = cutest_module.Cutest(problem_name)
    cutest_object.setup()
    os.chdir(wd)
    return cutest_object


def loadCutestProblems(problem_names=None, path=None,
                       sloth=False, verbose=False):
    if not path:
        path = getEnvironmentVariable(settings.env_mypycutest)
    if not problem_names:
        problem_names = getProblemNames()
    if not sloth:
        problem_names = [n for n in problem_names if n not in SLOTHS]
    pycutest_problems = {}
    for problem_name in problem_names:
        if verbose:
            print("Loading: {}".format(problem_name))
        module_name = getModuleName(problem_name)
        module_dir_path = os.path.join(path, problem_name)
        cutest_object = loadCutestProblem(module_name, module_dir_path)
        pycutest_problems[problem_name] = cutest_object
    return pycutest_problems


def checkDependencies():
    envs = [settings.env_sifdecode, settings.env_myarch,
            settings.env_mastsif, settings.env_cutest]
    map(getEnvironmentVariable, envs)
