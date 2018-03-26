from distutils import sysconfig
from functools import partial
from pycutest import settings
from pycutest import tools
import multiprocessing as mp
import numpy as np
import os
import pathlib
import pathlib
import subprocess
import sys
import tempfile
import time


# !!! INJECTION OF ARGUMENTS IS SUPERIOR, REFACTOR !!!!!
# TODO recheck compiler flags
# TODO improve variable naming
class SIFCompiler:

    def __init__(self):
        self.path = {}  # General storage for all kinds of paths
        self.envs = {}  # Environmental variables

        self.envs["arch"] = tools.getEnvironmentVariable('MYARCH')
        self.envs["cutest"] = tools.getEnvironmentVariable('CUTEST')

        self.path["cutest_lib_double"] = os.path.join(self.envs['cutest'],
                                                      "objects",
                                                      self.envs['arch'],
                                                      "double")
        self.path['cutest_include'] = os.path.join(self.envs['cutest'],
                                                   'include')
        self.ccompiler = 'gcc'
        self.fcompiler = 'gfortran'
        self.linker = 'ld'

        self.cython_file_name = 'cutest'

        self.fortran_src = ["ELFUN.f", "RANGE.f", "GROUP.f", "EXTER.f"]
        self.fortran_out = ["ELFUN.o", "RANGE.o", "GROUP.o", "EXTER.o"]
        self.verbose = False

    def buildModule(self, name, outpath=None, verbose=False):

        self.verbose = verbose
        self._setupEnvironment(name, outpath)
        self._compileCythonFiles()
        self._decodeSIF()
        self._compileInterface()
        self._compileFortranFiles()
        self._linkLibrary()
        self._createSO()
        self._verifyBuild()
        self._cleanEnvironment()
        return self.path['out']

    def _setupEnvironment(self, name, outpath):
        # CUTEST problem name
        self.name = name
        # module name, that can be imported in python
        self.moduleName = tools.getModuleName(name)
        self.path["working"] = os.getcwd()
        self.path["resource"] = os.path.dirname(os.path.abspath(__file__))

        if outpath is None:
            self.path["out"] = tempfile.mkdtemp()
        else:
            self.path["out"] = outpath
            if not os.path.exists(self.path['out']):
                pathlib.Path(self.path['out']).mkdir(parents=True,
                                                     exist_ok=True)

        os.chdir(self.path["out"])

        if self.verbose:
            print("Setup environment for '%s' in '%s'" % (self.name,
                                                          self.path["out"]))

        # copy and paste .pxd and .pyx to the new directory
        self.path['pxd_res'] = os.path.join(self.path['resource'],
                                            self.cython_file_name + ".pxd")
        self.path['pyx_res'] = os.path.join(self.path['resource'],
                                            self.cython_file_name + ".pyx")
        self.path["pxd"] = os.path.join(self.path['out'],
                                        self.moduleName + ".pxd")
        self.path["pyx"] = os.path.join(self.path['out'],
                                        self.moduleName + ".pyx")

        self._runSubprocess(['cp', self.path["pxd_res"], self.path["pxd"]])
        self._runSubprocess(['cp', self.path["pyx_res"], self.path["pyx"]])

    def _compileCythonFiles(self):
        cmd = ['cython', self.moduleName + ".pyx"]
        self._runSubprocess(cmd)

    def _decodeSIF(self):
        cmd = ['sifdecoder', '-o', '0', self.name]
        self._runSubprocess(cmd, stdout=subprocess.DEVNULL)

    def _compileInterface(self):
        # compile cythonized files and create .o
        cmd = [self.ccompiler,
               "-w", "-g", "-O3", "-fPIC",
               "-I" + np.get_include(),
               "-I" + sysconfig.get_python_inc(),
               "-I" + self.path['cutest_include'],
               "-c", self.moduleName + '.c',
               "-o", self.moduleName + '.o']
        self._runSubprocess(cmd)

    def _compileFortranFiles(self):
        # compile fortran stuff
        cmd = [self.fcompiler,
               "-c", "-fPIC"] + self.fortran_src
        self._runSubprocess(cmd)

    def _linkLibrary(self):
        # link library
        cmd = [self.linker, "-shared", "-o", "lib%s.so" % self.moduleName,
               "-L", self.path["cutest_lib_double"],
               "-lcutest"] + self.fortran_out
        self._runSubprocess(cmd)

    def _createSO(self):
        # Link all problem library to create the .so
        cmd = [self.ccompiler, "-shared", self.moduleName + '.o']
        cmd += self.fortran_out
        cmd += ["-L%s" % self.path["cutest_lib_double"]]
        cmd += ["-lcutest", "-lgfortran"]
        cmd += ["-o", self.moduleName + ".so"]
        self._runSubprocess(cmd)

    def _verifyBuild(self):
        if (os.path.isfile('OUTSDIF.d') and
            os.path.isfile('AUTOMAT.d') and
            os.path.isfile('lib' + self.moduleName + '.so') and
                os.path.isfile(self.moduleName + '.so')):
            if self.verbose:
                print("Successfully built '%s.so'" % self.moduleName)
        else:
            raise ValueError("Failed to build '%s.so'" % self.moduleName)

    def _cleanEnvironment(self):
        # Clean the source files and leave the temporary directory
        cmd = ['rm', self.moduleName + ".c", self.moduleName + ".o",
               self.moduleName + ".pxd", self.moduleName + ".pyx"]
        cmd += self.fortran_src + self.fortran_out
        self._runSubprocess(cmd)
        os.chdir(self.path['working'])

    def _runSubprocess(self, cmd, stdout=None):
        if self.verbose:
            print(" ".join(cmd))
        subprocess.run(cmd, stdout=stdout, check=True)


def buildModule(problem_name, path=None, verbose=False):
    if path is None:
        path = tools.getEnvironmentVariable(settings.env_mypycutest)
    module_dir_path = os.path.join(path, problem_name)
    if not os.path.exists(module_dir_path):
        pathlib.Path(path).mkdir(parents=True, exist_ok=True)
    SIFCompiler().buildModule(problem_name, module_dir_path, verbose)


def verifyBuild(problem_names, path=None):
    if path is None:
        path = tools.getEnvironmentVariable(settings.env_mypycutest)
    for problem_name in problem_names:
        module_dir_path = os.path.join(path, problem_name)
        module_name = tools.getModuleName(problem_name)
        path_outsdif = os.path.join(module_dir_path, 'OUTSDIF.d')
        path_automat = os.path.join(module_dir_path, 'AUTOMAT.d')
        path_lib = os.path.join(module_dir_path, 'lib' + module_name + '.so')
        path_so = os.path.join(module_dir_path, module_name + ".so")

        if not (os.path.isfile(path_outsdif) and
                os.path.isfile(path_automat) and
                os.path.isfile(path_lib) and
                os.path.isfile(path_so)):
            raise ValueError("Failed to build module for '%s'" % problem)


def progress(current, total):
    return (current + 1) * 100 / total


def pverbose(progress, name=None, start=None):
    out = "Installed: {:5.1f}%".format(progress)
    if start:
        end = time.time()
        elapsed = int(end - start)
        h, s = divmod(elapsed, 3600)
        m, s = divmod(s, 60)
        out += " - {:02d}:{:02d}:{:02d}".format(h, m, s)
    if name:
        out += " - Module: {:15s}".format(name)
    print(out, end='\r', flush=True)


def buildModuleParallel(problem_name, queue, path, verbose, debug):
    buildModule(problem_name, path=path, verbose=debug)
    queue.put(problem_name)


def buildParallel(problem_names, path, verbose, debug):
    try:
        pool = mp.Pool(os.cpu_count() * 2)
        m = mp.Manager()
        q = m.Queue()
        pool.map_async(partial(buildModuleParallel,
                       queue=q,
                       path=path,
                       verbose=verbose,
                       debug=False), problem_names)
        if verbose:
            start = time.time()
            pverbose(0, start=start)
        for i, _ in enumerate(problem_names):
            problem_name = q.get()
            p = progress(i, len(problem_names))
            pverbose(p, problem_name, start)
    finally:
        pool.close()
        pool.join()


def buildSerial(problem_names, path, verbose, debug):
    if verbose:
        start = time.time()
        pverbose(0, start=start)
    for i, problem_name in enumerate(problem_names):
        buildModule(problem_name, path, debug)
        if verbose:
            p = progress(i, len(problem_names))
            pverbose(p, problem_name, start)


def build(problem_names=None, path=None,
          verbose=True, parallel=True, debug=False):
    if debug:
        verbose = True
    if problem_names is None:
        problem_names = tools.getProblemNames()
    if parallel:
        buildParallel(problem_names, path, verbose, debug)
    else:
        buildSerial(problem_names, path, verbose, debug)
    verifyBuild(problem_names, path)
    if verbose:
        print("\n\nSuccessfully built modules!\n")
