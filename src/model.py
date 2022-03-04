import numpy as np
from words import words, possible_results
from game import Game

LOG_CONST = 1e-32

class Model:

    def __init__(self):
        self.words = np.asarray([list(w) for w in words])

    def __mask(self, guess, pattern):
        mask = np.ones(self.words.shape[0], dtype=bool)
        for i, (g, p) in enumerate(zip(guess, pattern)):
            if p == 'N':
                if np.count_nonzero(guess[p == 'Y'] == g) >= 1:
                    mask = np.logical_and(mask, self.words[:, i] != g)
                else:
                    mask = np.logical_and(mask, np.all(self.words != g, axis=1))
            elif p == 'M':
                mask = np.logical_and(mask, np.logical_and(np.any(self.words == g, axis=1), self.words[:, i] != g))
            elif p == 'Y':
                mask = np.logical_and(mask, self.words[:, i] == g)
        return mask

    def __mask_fraction(self, guess, pattern):
        mask = self.__mask(guess, pattern)
        return np.count_nonzero(mask) / self.words.shape[0]
    
    def prob_dist(self, guess):
        pmf = np.vectorize(self.__mask_fraction)
        return np.array([pmf(guess, pattern) for pattern in possible_results])

    def entropy(self, pmf):
        return -np.sum(pmf * np.log2(pmf + LOG_CONST), axis=0)
