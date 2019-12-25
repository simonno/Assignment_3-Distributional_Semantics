from datetime import datetime

from CorpusParse import corpus_parser
from SimilarityComputation import compute_counters


# def print_words_counter(words_counter, number=50):
#     words_counter = sorted(words_counter.items(), key=lambda item: item[1])
#     for i in range(number):
#         print('{}')


def main(corpus_file_name):
    start = datetime.now()
    sentences = corpus_parser(corpus_file_name)
    words_counter, pairs_counter, window_pairs_counter = compute_counters(sentences)
    # print_words_counter(words_counter)
    print('Running time: ', datetime.now() - start)


if __name__ == '__main__':
    main('wikipedia.tinysample.trees.lemmatized.txt')
