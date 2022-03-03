from game import Game
import numpy as np

game = Game()
for i in range(6):
    print(f'Guess {i+1}: ', end='')
    word = str(input())
    result = game.guess(word)
    while not(result):
        print("Invalid word")
        print(f'Guess {i+1}: ', end='')
        word = str(input())
        result = game.guess(word)
    print(' '.join(result))
    cnt = np.sum([c == '\U0001f7e9' for c in result])
    if cnt == 5:
        print(f'Solved {i+1}/6')
        break

print(f'The word was {game.get_solution()}')