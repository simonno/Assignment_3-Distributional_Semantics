import sys

import numpy as np


def load_normalized_vectors(vec_file):
    W = list()
    w2i = dict()
    words = list()
    line_counter = 0
    with open(vec_file, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip().split()
            w2i[line[0]] = line_counter
            words.append(line[0])
            W.append(np.array([float(v) for v in line[1:]]))
            line_counter += 1
    return np.array(W), w2i, words


def get_contexts(context_vec_file):
    contexts = list()
    with open(context_vec_file, 'r', encoding='utf-8') as file:
        for line in file:
            contexts.append(line.strip().split()[0])

    return contexts


class Word2Vec:
    def __init__(self, word_vec_file, context_vec_file):
        self.W, self.w2i, self.words = load_normalized_vectors(word_vec_file)
        self.contexts = get_contexts(context_vec_file)

    def compute_similarities(self, word):
        word_vector = self.get_word_vector(word)
        return self.W.dot(word_vector)

    def get_word_vector(self, word):
        return self.W[self.w2i[word]]

    def most_similar_words(self, word, most_similar=20):
        sims = self.compute_similarities(word)
        most_similar_indexes = sims.argsort()[-2:-(most_similar + 1):-1]
        return [self.words[index] for index in most_similar_indexes]

    def best_context_attributes(self, word, best=20):
        word_vector = self.get_word_vector(word)
        best_context_indexes = word_vector.argsort()[-1:-best:-1]
        return [self.contexts[index] for index in best_context_indexes]


def get_similar_words_and_best_contexts(word_vec_file, context_vec_file, words):
    word2vec = Word2Vec(word_vec_file, context_vec_file)

    similar_words = list()
    best_context_attributes = list()
    for word in words:
        similar_words.append(word2vec.most_similar_words(word))
        best_context_attributes.append(word2vec.best_context_attributes(word))

    return similar_words, best_context_attributes


def print_format(target_word, similar_words_list):
    line = '{}\n'.format(target_word)
    for similar_words in similar_words_list:
        line += '{}\n'.format(' '.join(similar_words))
    return line + '*********\n'


def print_most_similarity_words(file_name, target_words, similar_words_lists):
    with open(file_name, 'w', encoding='utf-8') as file:
        for target_word, similar_words_list in zip(target_words, similar_words_lists):
            file.write(print_format(target_word, similar_words_list))


def combine_words_lists(words_list1, words_list2):
    combined_list = list()
    for word1, word2 in zip(words_list1, words_list2):
        combined_list.append([word1, word2])
    return combined_list


def combine_results(result1, result2):
    combined_result = list()
    for words_list1, words_list2 in zip(result1, result2):
        combined_result.append(combine_words_lists(words_list1, words_list2))
    return combined_result


def main(bow5_word_file, bow5_contexts_file, deps_words_file, dep_contexts_file):
    target_words = ['car', 'bus', 'hospital', 'hotel', 'gun', 'bomb', 'horse', 'fox', 'table', 'bowl', 'guitar',
                    'piano']

    bow5_similar_words, bow5_best_contexts = get_similar_words_and_best_contexts(bow5_word_file, bow5_contexts_file,
                                                                                 target_words)
    deps_similar_words, deps_best_contexts = get_similar_words_and_best_contexts(deps_words_file, dep_contexts_file,
                                                                                 target_words)

    print_most_similarity_words('similarities_words', target_words,
                                combine_results(bow5_similar_words, deps_similar_words))
    print_most_similarity_words('best_contexts', target_words, combine_results(bow5_best_contexts, deps_best_contexts))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
