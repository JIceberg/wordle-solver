# Wordle Solver

You can find the needed requirements in the [requirements.txt](requirements.txt) file
and install them locally to your device with `pip install -r requirements.txt` if you clone
this repository.

## Playing the Game Manually

Run `python src/main.py`, and you can play Wordle in your command line. Each time you run the game,
a new word will be chosen for the potential answer. Below is a sample game:

```sh
user@computer:~/...$ python src/main.py
Guess 1: crane
🟨🟨🟨⬛⬛
Guess 2: farce
⬛🟩🟨🟨⬛
Guess 3: macer  
🟩🟩🟩⬛🟨
Guess 4: macro
🟩🟩🟩🟩🟩
Solved 4/6
The word was macro
user@computer:~/...$
```

## Using the Solver

Run `python src/solver.py` and you can use the solver to play Wordle. Enter the pattern using
'Y' for green, 'M' for yellow, and 'N' for nothing. So, for example '🟩🟩🟩⬛🟨' would be 'YYYNM'.