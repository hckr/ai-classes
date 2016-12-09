#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import math
from random import randint, random
from matplotlib.pyplot import *

class NQueensSimulatedAnnealing(object):
    def __init__(self, t0, n, kmax):
        self.t0 = t0
        self.n = n
        s = []
        for col in range(n):
            s.append(randint(0, n-1))
        best_eval = self.f_eval(s)
        evals = [ best_eval ]
        for k in range(kmax):
            new_s = self.neighbour(s)
            evaln = self.f_eval(new_s)
            if self.probability(best_eval, evaln, k) > random():
                s = new_s
                best_eval = evaln
            evals.append(best_eval)
            if evaln == 0:
                break
        self.print_state(s)
        plot(evals, 'firebrick')
        ylim([min(evals)-1, max(evals) + 1])
        show()

    def f_eval(self, s):
        beats = [ set() for i in range(self.n) ]
        for col in range(self.n):
            for other_col in range(self.n):
                if col == other_col:
                    continue
                if s[col] == s[other_col] or abs(other_col - col) == abs(s[other_col] - s[col]):
                    beats[min(col, other_col)].add(max(col, other_col))
        beat_pairs = sum([ len(x) for x in beats ])
        return beat_pairs

    def probability(self, s_energy, new_s_energy, k):
        t = self.temp(k)
        if s_energy - new_s_energy < 0:
            return math.exp((s_energy - new_s_energy) / t)
        return 1

    def temp(self, k, alpha=0.95):
        return math.pow(alpha, k + 1) * self.t0

    def neighbour(self, s):
        new_s = list(s)
        col_to_move = randint(0, self.n - 1)
        while True:
            new_pos = randint(0, self.n - 1)
            if new_pos != s[col_to_move]:
                break
        new_s[col_to_move] = new_pos
        return new_s

    def print_state(self, s):
        if self.n < 20:
            rows_arr = []
            for row in range(self.n):
                row_arr = []
                for col in range(self.n):
                    if s[col] == row:
                        row_arr.append('X')
                    else:
                        row_arr.append(' ')
                rows_arr.append(' ' + ' | '.join(row_arr))
            print ('\n' + ''.join(['--- ' for i in range(self.n)]) + '\n').join(rows_arr)
        else:
            print ', '.join([ str(x) for x in s ])
        print 'eval: %d' % self.f_eval(s)


t0 = 2.5
n = 8
kmax = 1000
NQueensSimulatedAnnealing(t0, n, kmax)

# kolejne wywołania dla n = 100, kamx = 1000, t0 = 2.5: 22, 16, 19, 21, 21, 25, 20, 22, 22, 21 ;; średnia ~= 20.9