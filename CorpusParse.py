from collections import namedtuple, Counter, defaultdict
from datetime import datetime

from DependencyEdgeWordFeature import DependencyEdgeWordFeature
from SentenceWordFeature import SentenceWordFeature
from WindowWordFeature import WindowWordFeature

Token = namedtuple('Token', ['ID', 'FORM', 'LEMMA', 'CPOSTAG', 'POSTAG', 'FEATS', 'HEAD', 'DEPREL', 'PHEAD', 'PDEPREL'])


def get_number_key(word, last_key, number_key_of_word):
    if word in number_key_of_word.keys():
        return number_key_of_word[word]

    last_key += 1
    number_key_of_word[word] = last_key
    return last_key


def line_parser(line, last_key, number_key_of_word):
    fields = line.strip().split('\t')
    fields[0] = int(fields[0])
    fields[2] = get_number_key(fields[2], last_key, number_key_of_word)
    fields[6] = int(fields[6])
    return Token._make(fields)


def corpus_parser(corpus_file_name):
    sentence = list()
    last_key = 0
    number_key_of_word = defaultdict()
    sentence_word_feature = SentenceWordFeature()
    window_word_feature = WindowWordFeature()
    dependency_edge_word_feature = DependencyEdgeWordFeature()
    words_counter = Counter()
    start = datetime.now()
    counter = 0
    with open(corpus_file_name, 'r', encoding='utf8') as corpus_file:
        for line in corpus_file:
            if line == '\n':
                sentence_word_feature.add_sentence(sentence)
                window_word_feature.add_sentence(sentence)
                dependency_edge_word_feature.add_sentence(sentence)
                sentence = list()
                if counter % 100000 == 0:
                    print('sentence {0} running time: {1}'.format(counter, datetime.now() - start))
                counter += 1
            else:
                token = line_parser(line, last_key, number_key_of_word)
                words_counter[token.LEMMA] += 1
                sentence.append(token)
    return number_key_of_word, words_counter, sentence_word_feature, window_word_feature, dependency_edge_word_feature
