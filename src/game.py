from words import answers, words
import numpy as np
from collections import Counter

class Game:

    def __init__(self, solution = None):
        self.solution = solution if solution else np.random.choice(answers)
        self.valid = set(words)

    def result_as_boxes(self, game_res):
        res = ""
        for c in game_res:
            if c == 'Y':
                res += '\U0001f7e9'
            elif c == 'M':
                res += '\U0001f7e8'
            else:
                res += '\u2B1B'
        return res
    
    def guess(self, word):
        if word not in self.valid:
            return []
        
        result = ['N' for _ in range(5)]
        cnt = Counter(self.solution)
        for i in range(5):
            guess_letter, actual_letter = word[i], self.solution[i]
            if guess_letter == actual_letter:
                result[i] = 'Y'
                cnt[guess_letter] -= 1
            elif cnt[guess_letter] and cnt[guess_letter] > 0:
                result[i] = 'M'
                cnt[guess_letter] -= 1
        return result

    def get_solution(self):
        return self.solution