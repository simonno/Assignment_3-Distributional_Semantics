from collections import namedtuple, Counter
from datetime import datetime

from DependencyEdgeWordFeature import DependencyEdgeWordFeature
from SentenceWordFeature import SentenceWordFeature
from WindowWordFeature import WindowWordFeature

Token = namedtuple('Token', ['ID', 'FORM', 'LEMMA', 'CPOSTAG', 'POSTAG', 'FEATS', 'HEAD', 'DEPREL', 'PHEAD', 'PDEPREL'])


def line_parser(line):
    fields = line.strip().split('\t')
    fields[0] = int(fields[0])
    fields[6] = int(fields[6])
    return Token._make(fields)


def corpus_parser(corpus_file_name):
    sentence = list()
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
                token = line_parser(line)
                words_counter[token.LEMMA] += 1
                sentence.append(token)
    return words_counter, sentence_word_feature, window_word_feature, dependency_edge_word_feature
