from words import answers, words
import numpy as np

class Game:

    def __init__(self):
        self.solution = np.random.choice(answers)
        self.valid = set(words)
    
    def guess(self, word):
        if word not in self.valid:
            return []
        
        result = ['\u2B1B' for _ in range(5)]
        for i in range(5):
            guess_letter, actual_letter = word[i], self.solution[i]
            if guess_letter == actual_letter:
                result[i] = '\U0001f7e9'
            elif guess_letter in self.solution:
                result[i] = '\U0001f7e8'
        return result

    def get_solution(self):
        return self.solution