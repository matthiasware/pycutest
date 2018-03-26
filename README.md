# PYCUTEST #
A python interface for the [CUTEST](https://ccpforge.cse.rl.ac.uk/gf/project/cutest/wiki/) package. It basically interfaces "Cutest.h. For this, pycutest relies on Cython and Numpy.

# TODO
- add tests !!!
- rework readme.md
- create compile function
- create recompile funciton
- create remake meta function
- do this from setup.py
- check if all environment variables are set!!!
- Multiimport BUG, release resources if not needed 
- remove del from \__del\__
- create a property csv file with bounds and constraints
- crate a benachmark file with ipopt and scipy runtimes.
- implement functions for constraint problems
- add interface for ipopt
- add more sample code

### Dependencies
- **Linux** (Although an adaption for MAC should be straightforward)
- **gcc**, **ld** and **gfortran**
- **CUTEST**, including **archdefs**, **SIFDecode** and the problem set.
- The environementvariables **_MYARCH_**, **_SIFDECODE_** **_MASTSIF_** and **_CUTEST_** must be set
- The **python3-dev** package is needed.
- Everything in **requirements.txt**

Since this interface uses **gcc** and **gfortran**, we recommend to let CUTEST use them as well. We also work with double precision, so make sure u setup CUTEST accordingly.

if you are using bash, your ".bashrc" should look similar to this one:

```sh
...
export ARCHDEFS=".../archdefs"
export SIFDECODE=".../sifdecode"
export CUTEST=".../cutest"
export MYARCH="pc64.lnx.gfo"
export MASTSIF=".../sif" 
export PATH="${SIFDECODE}/bin:${PATH}"
export PATH="${CUTEST}/bin:${PATH}"
export MANPATH="${SIFDECODE}/man:${MANPATH}"
export MANPATH="${CUTEST}/man:${MANPATH}"
...
```

### Minimal Installation
Check dependencies, clone repository and run :
``` sh
$ python setup.py install
```
In order to verify the installation, open a python console and run:
``` python
>>> import pycutest
>>> AKIVA = pycutest.PycutestProblem()
>>> AKIVA.compileAndLoad("AKIVA")
>>> AKIVA.fg(AKIVA.var_init)
(14.556090791758852, array([ 456.05,    0.5 ]))
```
If you get this result without complaints, the interface works. The following steps are recomended, but not necessary.

### Full Installation
In order to get the interface to work in python, we dynamically create python extension modules, which are shared libraries (.so). This involves a lot of compilation. In the previous step, we dropped all the resulting files in _/tmp_. In order to prevent permanent recompilation, we recommend to set the environment variable **_MYPYCUTEST_**. All of the pycutest functions check for this variable and use it if no other path is provided. Therefore in addition to the minimal installation, add the following line to the end of your **_~/.bashrc_**:

```sh
export MYPYCUTEST="/path/to/dir/of/choice"
```
Now open a python console and compile the problem set (this may take while):
``` python
>>> import pycutest
>>> pycutest.compile(verbose=True)
```
In order to verify the installation, open a python console and run:
``` python
>>> import pycutest
>>> AKIVA = pycutest.PycutestProblem("AKIVA")
>>> AKIVA.fg(AKIVA.var_init)
(14.556090791758852, array([ 456.05,    0.5 ]))
```

### Examples

Examples can be found in **_/scripts/_**

### Troubleshooting
For problems with the interface please contact me via matthias.mitterreiter@uni-jena.de.

## Notes
- You can compile just a subset of the problem set by providing a list of them.
- If you don't want to set **_MYPYCUTEST_**, you can provide a path with each compile/load step.
- If you change the interface, you need to recompile everything.
- Here we work with double precision only.
- A partly working python Interface for MAC can be found [@github](https://github.com/kenjydem/CUTEST.py). You may use the compilation script provided there.
- The following problems take CUTEST ages to load. You may be better off by avoiding them:
    - BA-L73 (4.850535665987991 s)
    - BA-L73LS (5.0699929900001734 s)
    - BDRY2 (1.4406649239826947 s)
    - CHANDHEU (2.5025131810689345 s)
    - CHARDIS0 (14.484561441000551 s)
    - CHARDIS1 (14.918080420000479 s)
    - DMN15102 (9.625917852041312 s)
    - DMN15102LS (9.542584719019942 s)
    - DMN15103 (14.728129283059388 s)
    - DMN15103LS (14.452318854047917 s)
    - DMN15332 (9.505480203893967 s)
    - DMN15332LS (9.479383587022312 s)
    - DMN15333 (12.871834745979868 s)
    - DMN15333LS (12.52549144194927 s)
    - DMN37142 (9.523974034003913 s)
    - DMN37142LS (9.505072196014225 s)
    - DMN37143 (13.113672949024476 s)
    - DMN37143LS (13.381633582990617 s)
    - GPP (6.087854203069583 s)
    - LEUVEN3 (1.14669645705726 s)
    - LEUVEN4 (1.1226522589568049 s)
    - LEUVEN5 (1.1110458229668438 s)
    - LEUVEN6 (1.1239287389907986 s)
    - LIPPERT2 (3.6417447249405086 s)
    - LOBSTERZ (1.7964531490579247 s)
    - PDE1 (1.1012970780720934 s)
    - PDE2 (1.2520159740233794 s)
    - PENALTY3 (1.189755222061649 s)
    - RDW2D51F (1.6091901200124994 s)
    - RDW2D51U (1.6037442940287292 s)
    - RDW2D52B (1.6436974169919267 s)
    - RDW2D52F (1.6701275389641523 s)
    - RDW2D52U (1.7224227929254994 s)
    - ROSEPETAL (51.78898571804166 s)
    - WALL100 (2.770009451895021 s)
    - YATP1SQ (2.4853961719200015 s)
    - YATP2SQ (1.5281431359471753 s)
    - BA-L16LS (129.48893941694405 s)
    - BA-L21 (13.488894623005763 s)
    - BA-L21LS (13.452077899943106 s)
    - BA-L49 (3.3572275530314073 s)
    - BA-L49LS (3.3248339479323477 s)
    - BA-L52LS (1096.2810307029868 s)
    - BA-L52 (1084.83357333194 s)
    - **In short**: ['BA-L73', 'BA-L73LS', 'BDRY2', 'CHANDHEU', 'CHARDIS0', 'CHARDIS1', 'DMN15102', 'DMN15102LS', 'DMN15103', 'DMN15103LS', 'DMN15332', 'DMN15332LS', 'DMN15333', 'DMN15333LS', 'DMN37142', 'DMN37142LS', 'DMN37143', 'DMN37143LS', 'GPP', 'LEUVEN3', 'LEUVEN4', 'LEUVEN5', 'LEUVEN6', 'LIPPERT2', 'LOBSTERZ', 'PDE1', 'PDE2', 'PENALTY3', 'RDW2D51F', 'RDW2D51U', 'RDW2D52B', 'RDW2D52F', 'RDW2D52U', 'ROSEPETAL', 'WALL100', 'YATP1SQ', 'YATP2SQ', 'BA-L16LS', 'BA-L21', 'BA-L21LS', 'BA-L49', 'BA-L49LS', 'BA-L52LS', 'BA-L52']

## Resources
- **CUTEST** (https://ccpforge.cse.rl.ac.uk/gf/project/cutest/wiki/)
- **CUTEST problems** (http://www.cuter.rl.ac.uk/Problems/mastsif.shtml)
- **Cython Basics** (http://docs.cython.org/en/latest/src/userguide/language_basics.html)