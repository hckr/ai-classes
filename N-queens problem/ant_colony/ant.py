from __future__ import division
import random

class Ant(object):
    ALPHA = None
    BETA = None
    MAX_PHEROMONE_AMOUNT = None

    def __init__(self, problem_size, pheromone_trail):
        self.pheromone_trail = pheromone_trail
        self.problem_size = problem_size
        self.queens_rows = []
        self.place_queens()

    def place_queens(self):
        rows = [0] * self.problem_size
        rows[0] = random.randint(0, self.problem_size - 1)
        for column2 in range(1, self.problem_size):
            decision_values = []
            for row2 in range(self.problem_size):
                rows[column2] = row2
                pheromone_amount = self.pheromone_trail.get_value(column2 - 1, column2, rows[-1], row2)
                not_beating = self.count_not_beating(rows)
                decision_values.append(pheromone_amount**self.ALPHA * not_beating**self.BETA)
            decision_values_sum = sum(decision_values)
            if decision_values_sum == 0:
                probabilities = [ 1 / len(decision_values) for _ in decision_values ]
            else:
                probabilities = [ v / decision_values_sum for v in decision_values ]
            random_val = random.random()
            sum_ = 0
            for i, p in enumerate(probabilities):
                sum_ += p
                if random_val <= sum_:
                    row2 = i
                    break
            else:
                raise RuntimeError('Should never happen')
            rows[column2] = row2
        self.queens_rows = rows

    def count_not_beating(self, queens_rows=None):
        if queens_rows is None:
            queens_rows = self.queens_rows
        problem_size = len(queens_rows)
        not_beating = 0
        for col in range(problem_size):
            for other_col in range(problem_size):
                if col == other_col:
                    continue
                if queens_rows[col] == queens_rows[other_col]:
                    break
                if abs(other_col - col) == abs(queens_rows[other_col] - queens_rows[col]):
                    break
            else:
                not_beating += 1
        return not_beating

    def get_not_beating(self):
        not_beating = []
        for col in range(self.problem_size):
            for other_col in range(self.problem_size):
                if col == other_col:
                    continue
                if self.queens_rows[col] == self.queens_rows[other_col]:
                    break
                if abs(other_col - col) == abs(self.queens_rows[other_col] - self.queens_rows[col]):
                    break
            else:
                not_beating.append(col)
        return not_beating

    def place_pheromone(self):
        not_beating = self.count_not_beating()
        divider = self.problem_size - not_beating
        if divider == 0:
            amount = self.MAX_PHEROMONE_AMOUNT
        else:
            amount = self.MAX_PHEROMONE_AMOUNT / divider
        self.pheromone_trail.mark_trail(self.queens_rows, amount)