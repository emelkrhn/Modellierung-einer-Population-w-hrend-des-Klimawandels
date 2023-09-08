from scipy import stats
from scipy.optimize import fsolve
from scipy import integrate as integ


print('math_functions module imported')

def skew_norm_dist(x, a, loc, scale):
    '''
        scipy.stats.norm.pdf(x, a, loc, stats)
            a: skewness parameter 
            loc: mean
            scale: standard deviation
    '''
    y = stats.skewnorm.pdf(x, a, loc=loc, scale=scale)
    return y


def get_roots(function):
    roots = fsolve(function,[20,50])
    return roots


def integrate(function, args, roots):
    '''
    math_functions.integrate contains:
        scipy.integrate.quad(func, a, b, args=())
            func: a Python function or method to integrate
            a: lower limit of integration
            loc: upper limit of integration
            args: extra arguments to pass into the function, in this case time
    '''
    min, max = roots

    integral = integ.quad(function, min, max, args=(args))
    return integral[0]