#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from random import randint
from matplotlib.pyplot import *

class NQueensHillClimbing(object):
    def __init__(self, n, kmax):
        self.n = n
        s = []
        for col in range(n):
            s.append(randint(0, n-1))
        best_eval = self.f_eval(s)
        evals = [ best_eval ]
        for k in range(kmax):
            new_s = self.neighbour(s)
            evaln = self.f_eval(new_s)
            if evaln < best_eval:
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


n = 8
kmax = 1000
NQueensHillClimbing(n, kmax)
