from words import answers, words
import numpy as np
from collections import Counter

class Game:

    def __init__(self):
        self.solution = np.random.choice(answers)
        self.valid = set(words)
    
    def guess(self, word):
        if word not in self.valid:
            return []
        
        result = ['\u2B1B' for _ in range(5)]
        cnt = Counter(self.solution)
        for i in range(5):
            guess_letter, actual_letter = word[i], self.solution[i]
            if guess_letter == actual_letter:
                result[i] = '\U0001f7e9'
                cnt[guess_letter] -= 1
            elif cnt[guess_letter] and cnt[guess_letter] > 0:
                result[i] = '\U0001f7e8'
                cnt[guess_letter] -= 1
        return result

    def get_solution(self):
        return self.solution