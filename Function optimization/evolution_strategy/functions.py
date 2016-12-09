from __future__ import division
from math import exp, cos, pi, sqrt

def easom(x):
    return -cos(x[0])*cos(x[1])*exp(-(x[0]-pi)**2-(x[1]-pi)**2)

def rosenbrock(x):
    n = len(x);
    s = 0;
    for j in xrange(n-1):
        s += 100*(x[j]**2-x[j+1])**2+(x[j]-1)**2
    return s

def griewank(x):
    n = len(x)
    fr = 4000
    s = 0
    p = 1
    for j in xrange(n):
        s += x[j]**2
    for j in xrange(n):
        p *= cos(x[j]/sqrt(j + 1))
    return s/fr-p+1
