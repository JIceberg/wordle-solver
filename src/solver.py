from game import result_as_int
from model import Model
from words import words, answers
import numpy as np

print('Loading model...')
model = Model(words, answers)

possible_answers = np.asarray(answers)
priors = model.get_freq_priors()
print('Model loaded!')
while True:
    print('I would like to enter a word [y/n] ', end='')
    play = str(input())
    if play != 'y':
        break
    else:
        print('What was your guess? ', end='')
        guess = str(input())
        print('What was the pattern? ', end='')
        pattern = str(input())
        val = result_as_int(pattern)
        possible_answers = model.get_possible_answers(guess, val, possible_answers)
        print(f'Your guess should be: {model.get_optimal_guess(possible_answers, possible_answers, priors)}')
    