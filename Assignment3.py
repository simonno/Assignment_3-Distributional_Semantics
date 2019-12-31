from collections import Counter, defaultdict
from datetime import datetime

from CorpusParse import corpus_parser


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


def main(corpus_file_name):
    target_words = ['car', 'bus', 'hospital', 'hotel', 'gun', 'bomb', 'horse', 'fox', 'table', 'bowl', 'guitar',
                    'piano']
    start = datetime.now()
    number_key_of_word, words_counter, sentence, window, dependency_edge = corpus_parser(corpus_file_name)
    words_counter = Counter({word: count for word, count in words_counter.items() if count > 99})
    sentence.filter_features(words_counter)
    window.filter_features(words_counter)
    dependency_edge.filter_features(words_counter)
    print_most_common_words(words_counter)

    similar_words = defaultdict(list)
    for target_word in target_words:
        target_word = number_key_of_word[target_word]
        similar_words[target_word].append(sentence.get_most_similarity_words(target_word))
        similar_words[target_word].append(window.get_most_similarity_words(target_word))
        similar_words[target_word].append(dependency_edge.get_most_similarity_words(target_word))

    print_most_similarity_words(similar_words)

    print('Running time: ', datetime.now() - start)


if __name__ == '__main__':
    main('wikipedia.sample.trees.lemmatized')
