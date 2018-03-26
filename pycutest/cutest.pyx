import numpy as np
cimport numpy as np
cimport cython
from cpython cimport bool

'''
  Cython cutest interface
  Should implement everything from 'cutest.h'
  Work in progress ... of course
'''
cdef class Cutest:
    # FORTRAN unit codes
    cdef int fu_file       # FORTRAN unit number for OUTSDIF.d
    cdef int fu_iout       # FORTRAN unit number for error output 6-> Terminal
    cdef int fu_io_buffer  # FORTRAN unit internal input/output

    # FORTRAN bool values
    cdef logical f_TRUE
    cdef logical f_FALSE

    # Cutest flags
    cdef int status        # Exit flag from CUTEST tools

    # Problem properties
    cdef char * name       # problem name
    cdef int num_var       # number of variables
    cdef int num_const     # number of constraints

    # Initial estimate of solution
    cdef np.ndarray var_init
        
    # lower bounds on variables
    cdef np.ndarray var_bounds_l
    
    # upper bounds on variables
    cdef np.ndarray var_bounds_u
    
    # initial estimate of lagragion multipliers at the solution
    cdef np.ndarray multipliers_init
    
    # lower bounds on inequality constraints
    cdef np.ndarray const_bounds_l
    
    # upper bounds on inequality constraints
    cdef np.ndarray const_bounds_u

    # note that boolean arrays not supported in cython
    # cdef np.ndarray[logical, cast=True] is_const_equality = np.arange(self.num_const, dtype='>i1')
    cdef np.ndarray is_const_equality
    
    # logical array, i-th component is TRUE if i-th constraint is (linear or affin) otherwise FALSE
    cdef np.ndarray is_const_linear


    def __init__(self, char* name):
        self.name = name
        self.fu_file = 42
        self.fu_iout = 6
        self.fu_io_buffer = 11
        self.status = 0
        self.f_TRUE = 1
        self.f_FALSE = 0

    def setup(self, char* filename = "OUTSDIF.d"):

        # CUTEST cutest_setup, see see cutest/doc/cutest_csetup.pdf
        cdef int v_order = 0
        cdef int e_order = 2
        cdef int l_order = 0

        # Open problem description file OUTSDif.d / fname
        FORTRAN_open(&self.fu_file, filename, &self.fu_iout)

        # determine number of variables, number of constraints
        CUTEST_cdimen(&self.status, &self.fu_file, &self.num_var, &self.num_const)
        self.checkStatus(self.status)

        # Allocate memory
        # Initial estimate of solution
        cdef np.ndarray var_init = np.zeros((self.num_var), dtype = np.double)
        
        # lower bounds on variables
        cdef np.ndarray var_bounds_l = np.zeros((self.num_var),dtype = np.double)
        
        # upper bounds on variables
        cdef np.ndarray var_bounds_u = np.zeros((self.num_var),dtype = np.double)
        
        # initial estimate of lagragion multipliers at the solution
        cdef np.ndarray multipliers_init = np.zeros((self.num_const),dtype = np.double)
        
        # lower bounds on inequality constraints
        cdef np.ndarray const_bounds_l = np.zeros((self.num_const), dtype = np.double)
        
        # upper bounds on inequality constraints
        cdef np.ndarray const_bounds_u = np.zeros((self.num_const), dtype = np.double)

        # logical array, i-th component is TRUE/FALSE if i-th constraint is an equality/inequality
        # note that boolean arrays not supported in cython
        # cdef np.ndarray[logical, cast=True] is_const_equality = np.arange(self.num_const, dtype='>i1')
        cdef np.ndarray[logical, cast=True] is_const_equality = np.arange(self.num_const, dtype=np.int8)
        
        # logical array, i-th component is TRUE if i-th constraint is (linear or affin) otherwise FALSE
        # note that boolean arrays not supported in cython
        # cdef np.ndarray[logical, cast=True] is_const_linear = np.arange(self.num_const, dtype='>i1')
        cdef np.ndarray[logical, cast=True] is_const_linear = np.arange(self.num_const, dtype=np.int8)

        # Setup data structures
        if self.num_const > 0: # constraint poblems
            CUTEST_csetup(&self.status, &self.fu_file, &self.fu_iout,
                          &self.fu_io_buffer, &self.num_var, &self.num_const,
                          <double *>var_init.data, <double *>var_bounds_l.data,
                          <double *>var_bounds_u.data,
                          <double *>multipliers_init.data, <double *>const_bounds_l.data,
                          <double *>const_bounds_u.data,
                          &is_const_equality[0], &is_const_linear[0],
                          &e_order, &l_order, &v_order)
        else: # unconstraint problems
            CUTEST_usetup(&self.status, &self.fu_file, &self.fu_iout,
                          &self.fu_io_buffer, &self.num_var,
                          <double *>var_init.data, <double *>var_bounds_l.data,
                          <double *>var_bounds_u.data)
        self.checkStatus(self.status)

        # Adjust bounds infinity values to be numpy conform
        # check 'cutest.h' for #defines
        var_bounds_l[np.where(var_bounds_l<=-1e+20)[0]] = -np.Inf 
        var_bounds_u[np.where(var_bounds_u>=1e+20)[0]] = np.Inf
        const_bounds_l[np.where(const_bounds_l<=-1e+20)[0]] = -np.Inf
        const_bounds_u[np.where(const_bounds_u>=1e+20)[0]] = np.Inf

        self.var_init = var_init
        self.var_bounds_l = var_bounds_l
        self.var_bounds_u = var_bounds_u
        self.multipliers_init = multipliers_init
        self.const_bounds_l = const_bounds_l
        self.const_bounds_u = const_bounds_u
        self.is_const_linear = np.array(is_const_linear, dtype=np.bool)
        self.is_const_equality = np.array(is_const_equality, dtype=np.bool)

    def getProperties(self):
        return {'problem_name'      : str(self.name, 'utf-8'),
                'num_var'           : self.num_var,
                'num_const'         : self.num_const,
                'var_init'          : self.var_init,
                'var_bounds_l'      : self.var_bounds_l,
                'var_bounds_u'      : self.var_bounds_u,
                'multipliers_init'  : self.multipliers_init,
                'const_bounds_l'    : self.const_bounds_l,
                'const_bounds_u'    : self.const_bounds_u,
                'is_const_linear'   : self.is_const_linear,
                'is_const_equality' : self.is_const_equality,
               }



    @cython.boundscheck(False)  # disable cython bound-checking
    @cython.wraparound(False)   # disable cython checks for negative indices
    def cutest_uofg(self, double[:] x):
        """function value and gradient of unconstraint problem."""
        cdef double f
        cdef np.ndarray g = np.zeros((self.num_var), dtype=np.double) 
        CUTEST_uofg(&self.status, &self.num_var, &x[0], &f, <double *>g.data, &self.f_TRUE)
        self.checkStatus(self.status)
        return f,g

    @cython.boundscheck(False)
    @cython.wraparound(False)
    def cutest_udh(self, double[:] x):
        """hessian of unconstraint problem"""
        cdef double[:] h = np.zeros((self.num_var * self.num_var), dtype=np.double)
        CUTEST_udh(&self.status, &self.num_var, &x[0], &self.num_var, &h[0])
        self.checkStatus(self.status)

        hess = np.reshape(h, (self.num_var, self.num_var), order='F')
        return hess


    def cutest_uterminate(self):
        pass

    def cutest_cterminate(self):
        pass

    def cutest_cofg(self, double[:] x):
        """function value and gradient of constraint problem."""
        cdef double f
        cdef np.ndarray g = np.zeros((self.num_var), dtype=np.double) 
        CUTEST_cofg( &self.status, &self.num_var, &x[0], &f, <double *>g.data, &self.f_TRUE)
        self.checkStatus(self.status)
        return f,g

    def cutest_cfn(self, double[:] x):
        cdef double f
        cdef np.ndarray c = np.zeros((self.num_const), dtype=np.double)
        CUTEST_cfn(&self.status,
                   &self.num_var,
                   &self.num_const,
                   &x[0],
                   &f,
                   <double *>c.data)
        self.checkStatus(self.status)
        return c


    def cutest_ccfg(self, double[:] x, grad=False, transpose=False):
        """evaluates constraints + its gradient"""
        cdef np.ndarray jacobi = np.zeros((self.num_const * self.num_var), dtype=np.double)
        cdef np.ndarray consts = np.zeros((self.num_const), dtype=np.double)
        # Notes:
        # Jacobi: i-th row is gradient of i-th constraint
        if grad:
            CUTEST_ccfg(&self.status,
                        &self.num_var,
                        &self.num_const,
                        &x[0],
                        <double *> consts.data,
                        &self.f_FALSE, # True if we want transpose of jacobian
                        &self.num_const, # Jacobi leading dimension
                        &self.num_var, # Jacobi other dimension
                        <double *>jacobi.data,
                        &self.f_TRUE); # True if the gradint is of constraints wanted
            self.checkStatus(self.status)
            jacobi = np.reshape(jacobi, [self.num_const, self.num_var], order='F')
            return consts, jacobi
        else:
            CUTEST_ccfg(&self.status,
                        &self.num_var,
                        &self.num_const,
                        &x[0],
                        <double *> consts.data,
                        &self.f_FALSE,
                        &self.num_const,
                        &self.num_var,
                        <double *>jacobi.data,
                        &self.f_FALSE);
            self.checkStatus(self.status)
            return consts

    def cutest_cdh(self, double[:] x, double[:] lagrange_mul):
        """ Evaluates Hessian of f """
        cdef np.ndarray H = np.zeros((self.num_var, self.num_var), dtype=np.double)
        CUTEST_cdh(&self.status, &self.num_var, &self.num_const,
                   &x[0], &lagrange_mul[0], &self.num_var, <double *>H.data)
        self.checkStatus(self.status)
        H = np.reshape(H, (self.num_var, self.num_var), order='F')
        return H


    def cutest_cjprod(self, double[:] x, double[:] v, transpose=False):
        """ calculates v*J(x) or ??? J(x)^T*v 
            x R^n
            v R^(m)
            J R^(m*n)
            y = v*J R^(n)
        """
        # for i in range(self.num_var):
        #     print(i, x[i])
        # for i in range(self.num_const):
        #     print(i, v[i])
        cdef np.ndarray y
        # (status:,
        #  num_var:,
        #  num_const,
        #  gotj: True if the first derivatives of groups and elements have been set, or should be computed,
        #  jtrans: True if we want J^T,
        #  X: will only be used if gotj is False
        #  Vector: vector whose product with J or J^T is required
        #  lvector: dimension of the vector
        #  result:
        #  lresult: dimension of the result) 
        if transpose:
            raise Exception("NOT IMPLEMENTED")
            # res = np.zeros((self.num_var), dtype=np.double)
            # CUTEST_cjprod(&self.status, &self.num_var, &self.num_const,
            #               &self.f_FALSE, &self.f_TRUE,
            #               &x[0], &v[0], &self.num_const,
            #               <double *> res.data, &self.num_var)
        else:
            y = np.zeros((self.num_var), dtype=np.double)
            CUTEST_cjprod(&self.status, &self.num_var, &self.num_const,
                          &self.f_FALSE, &self.f_TRUE,
                          &x[0], &v[0], &self.num_const,
                          <double *> y.data, &self.num_var)
            # for i in range(self.num_var):
                # print(y[i])

        self.checkStatus(self.status)
        return y

    def checkStatus(self, int status, msg=str()):
        # 0 = success
        # 1 = array allocation error
        # 2 = array bound error
        # 3 = array evaluation error
        if status > 0:
            if status == 1:
                raise RuntimeError('CUTEST memory allocation error %s' %msg)
            elif status == 2:
                raise RuntimeError('CUTEST array bound error %s' %msg)
            elif status == 3:
                raise RuntimeError('CUTEST evaluation error %s' %msg)
            else:
                raise RuntimeError('Some filthy error with CUTEST! %s' %msg)

    def __dealloc__(self):
        FORTRAN_close(&self.fu_io_buffer, &self.status)
        self.checkStatus(self.status)
        # self.cutest_uterminate()