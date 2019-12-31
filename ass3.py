import sys
from collections import Counter, defaultdict
from datetime import datetime

from CorpusParse import corpus_parser, writetofile
from DependencyEdgeWordFeature import DependencyEdgeWordFeature
from SentenceWordFeature import SentenceWordFeature
from WindowWordFeature import WindowWordFeature


def print_most_common_words(words_counter, most_common=50):
    with open('counts_words.txt', 'w') as file:
        for word, count in words_counter.most_common(most_common):
            file.write('{0} {1}\n'.format(word, count))


def print_most_similarity_words(similar_words, most_similar=20):
    with open('top20.txt', 'w') as file:
        for word, co_occurrence_types in similar_words.items():
            file.write('{}\n\n'.format(word))
            for i in range(most_similar):
                similar_words_line = list()
                for j in range(len(co_occurrence_types)):
                    similar_words_line.append(co_occurrence_types[j][i][1])
                line = ' '.join(similar_words_line)
                file.write('{}\n'.format(line))
            file.write('*********\n')


def read_lines(corpus_file_name):
    with open(corpus_file_name, 'r', encoding='utf8', errors='ignore') as corpus_file:
        lines = corpus_file.readlines()
    return lines


def main(corpus_file_name):
    target_words = ['car', 'bus', 'hospital', 'hotel', 'gun', 'bomb', 'horse', 'fox', 'table', 'bowl', 'guitar',
                    'piano']
    start = datetime.now()
    lines = read_lines(corpus_file_name)
    # writetofile(lines)

    sentence_word_feature = SentenceWordFeature()
    window_word_feature = WindowWordFeature()
    dependency_edge_word_feature = DependencyEdgeWordFeature()

    words_counter = corpus_parser(lines,
                                  [sentence_word_feature, window_word_feature, dependency_edge_word_feature])
    words_counter = Counter({word: count for word, count in words_counter.items() if count > 99})

    sentence_word_feature.filter_features(words_counter)
    window_word_feature.filter_features(words_counter)
    dependency_edge_word_feature.filter_features(words_counter)

    # start2 = datetime.now()
    # sentence_word_feature = SentenceWordFeature()
    # words_counter = corpus_parser(lines, sentence_word_feature)
    # words_counter = Counter({word: count for word, count in words_counter.items() if count > 99})
    # sentence_word_feature.filter_features(words_counter)
    # print('all sentence running time: {}'.format(datetime.now() - start2))
    #
    # start2 = datetime.now()
    # window_word_feature = WindowWordFeature()
    # corpus_parser(lines, window_word_feature)
    # window_word_feature.filter_features(words_counter)
    # print('window running time: {}'.format(datetime.now() - start2))
    #
    # start2 = datetime.now()
    # dependency_edge_word_feature = DependencyEdgeWordFeature()
    # dependency_edge_word_feature.filter_features(words_counter)
    # corpus_parser(lines, dependency_edge_word_feature)
    # print('dep running time: {}'.format(datetime.now() - start2))

    print_most_common_words(words_counter)

    similar_words = defaultdict(list)
    for target_word in target_words:
        similar_words[target_word].append(sentence_word_feature.get_most_similarity_words(target_word))
        similar_words[target_word].append(window_word_feature.get_most_similarity_words(target_word))
        similar_words[target_word].append(dependency_edge_word_feature.get_most_similarity_words(target_word))

    print_most_similarity_words(similar_words)

    print('Running time: ', datetime.now() - start)


if __name__ == '__main__':
    main(sys.argv[1])
