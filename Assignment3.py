from collections import Counter
from datetime import datetime

from CorpusParse import corpus_parser


def print_most_common_words(words_counter, most_common=50):
    with open('counts_words.txt', 'w') as file:
        for word, count in words_counter.most_common(most_common):
            file.write('{0} {1}\n'.format(word, count))


def main(corpus_file_name):
    target_words = ['car', 'bus', 'hospital', 'hotel', 'gun', 'bomb', 'horse', 'fox', 'table', 'bowl', 'guitar',
                    'piano']
    start = datetime.now()
    words_counter, sentence, window, dependency_edge = corpus_parser(corpus_file_name)
    sentence.filter_features()
    window.filter_features()
    dependency_edge.filter_features()
    words_counter = Counter({word: count for word, count in words_counter.items() if count > 99})
    print_most_common_words(words_counter)
    print('Running time: ', datetime.now() - start)


if __name__ == '__main__':
    main('wikipedia.sample.trees.lemmatized')
