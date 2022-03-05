import numpy as np
from scipy.stats import entropy
import os, json
import itertools as it

DATA_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    "data",
)
WORD_FREQ_MAP_FILE = os.path.join(DATA_DIR, "freq_map.json")
PATTERN_MATRIX_FILE = os.path.join(DATA_DIR, "pattern_matrix.npy")

class Model:

    BLACK = 0
    YELLOW = 1
    GREEN = 2

    def __init__(self, all_words, all_solutions, naive = True):
        self.words = np.asarray(all_words)
        self.solutions = np.asarray(all_solutions)
        self.grid = dict()

        self.priors = self.get_naive_priors() if naive else self.get_freq_priors()
        self.first_guess = self.get_first_guess(self.priors)

    def __sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def __words_to_ascii(self, words):
        return np.array([[ord(c) for c in w] for w in words], dtype=np.uint8)

    def __generate_pattern_matrix(self, words1, words2):
        num_letters = len(self.words[0])
        num_words1 = words1.shape[0]
        num_words2 = words2.shape[0]

        int_words1, int_words2 = map(self.__words_to_ascii, (words1, words2))
        equality_grid = np.zeros((num_words1, num_words2, num_letters, num_letters), dtype=bool)
        for i, j in it.product(range(num_letters), range(num_letters)):
            equality_grid[:, :, i, j] = np.equal.outer(int_words1[:, i], int_words2[:, j])

        full_matrix = np.zeros((num_words1, num_words2, num_letters), dtype=np.uint8)

        for i in range(num_letters):
            matches = equality_grid[:, :, i, i].flatten()
            full_matrix[:, :, i].flat[matches] = Model.GREEN
            for k in range(num_letters):
                equality_grid[:, :, k, i].flat[matches] = False
                equality_grid[:, :, i, k].flat[matches] = False

        for i, j in it.product(range(num_letters), range(num_letters)):
            matches = equality_grid[:, :, i, j].flatten()
            full_matrix[:, :, i].flat[matches] = Model.YELLOW
            for k in range(num_letters):
                equality_grid[:, :, k, j].flat[matches] = False
                equality_grid[:, :, i, k].flat[matches] = False

        return np.dot(full_matrix, (3 ** np.arange(num_letters)).astype(np.uint8))

    def __generate_matrix_file(self, words1, words2):
        pattern_matrix = self.__generate_pattern_matrix(words1, words2)
        np.save(PATTERN_MATRIX_FILE, pattern_matrix)
        return pattern_matrix

    def get_pattern_matrix(self, choice_words, possible_answers):
        if not self.grid:
            if not os.path.exists(PATTERN_MATRIX_FILE):
                self.__generate_matrix_file(self.words, self.words)
            self.grid['grid'] = np.load(PATTERN_MATRIX_FILE)
            self.grid['words_to_index'] = dict(zip(self.words, it.count()))

        full_grid = self.grid['grid']
        words_to_index = self.grid['words_to_index']

        idx_words = [words_to_index[w] for w in choice_words]
        idx_answers = [words_to_index[w] for w in possible_answers]
        return full_grid[np.ix_(idx_words, idx_answers)]

    def get_pattern(self, guess, answer):
        if self.grid:
            saved_words = self.grid['words_to_index']
            if guess in saved_words and answer in saved_words:
                return self.get_pattern_matrix([guess], [answer])[0, 0]
        return self.__generate_pattern_matrix([guess], [answer])[0, 0]

    def get_word_frequencies(self):
        with open(WORD_FREQ_MAP_FILE) as f:
            fmap = json.load(f)
        return fmap

    def get_naive_priors(self):
        return dict((w, int(w in self.solutions)) for w in self.words)

    def get_freq_priors(self, n_common = 3000, width_under_sigmoid = 10):
        freq_map = self.get_word_frequencies()
        words = np.array(list(freq_map.keys()))
        freqs = np.array([freq_map[w] for w in words])
        arg_sort = freqs.argsort()
        sorted_words = words[arg_sort]

        priors = dict()
        x_width = width_under_sigmoid
        c = x_width * (-0.5 + n_common / len(words))
        xs = np.linspace(c - x_width / 2, c + x_width / 2, len(words))
        for word, x in zip(sorted_words, xs):
            priors[word] = self.__sigmoid(x)
        return priors

    def get_weights(self, words, priors):
        frequencies = np.array([priors[word] for word in words])
        total = frequencies.sum()
        if total == 0:
            return np.zeros(frequencies.shape)
        return frequencies / total

    def get_distributions(self, choice_words, possible_answers, weights):
        pattern_matrix = self.get_pattern_matrix(choice_words, possible_answers)

        n = len(choice_words)
        distributions = np.zeros((n, 3 ** 5))
        n_range = np.arange(n)
        for j, prob in enumerate(weights):
            distributions[n_range, pattern_matrix[:, j]] += prob
        return distributions

    def get_entropies(self, choice_words, possible_answers, weights):
        if weights.sum() == 0:
            return np.zeros(len(choice_words))
        distributions = self.get_distributions(choice_words, possible_answers, weights)
        ax = len(distributions.shape) - 1
        return entropy(distributions, base = 2, axis = ax)

    def get_possible_answers(self, guess, pattern, remaining_answers):
        all_patterns = self.get_pattern_matrix([guess], remaining_answers).flatten()
        return remaining_answers[all_patterns == pattern]

    def get_optimal_guess(self, choice_words, possible_answers, priors):
        weights = self.get_weights(choice_words, priors)
        entropies = self.get_entropies(choice_words, possible_answers, weights)
        return choice_words[np.argmax(entropies)]

    def get_first_guess(self, priors):
        weights = self.get_weights(self.words, priors)
        entropies = self.get_entropies(self.words, self.words, weights)
        return self.words[np.argmax(entropies)]

    def __call__(self, solution, **kwargs):
        guess = self.first_guess
        guesses = [guess]
        possible_answers = self.solutions
        while guess != solution:
            possible_answers = self.get_possible_answers(guess, self.get_pattern(guess, solution), possible_answers)
            guess = self.get_optimal_guess(possible_answers, possible_answers, self.priors)
            guesses.append(guess)
        return guesses
