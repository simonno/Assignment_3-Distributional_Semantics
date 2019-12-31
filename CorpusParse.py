from collections import namedtuple, Counter
from datetime import datetime

Token = namedtuple('Token', ['ID', 'FORM', 'LEMMA', 'CPOSTAG', 'POSTAG', 'FEATS', 'HEAD', 'DEPREL', 'PHEAD', 'PDEPREL'])


def line_parser(line):
    fields = line.strip().split('\t')
    fields[0] = int(fields[0])
    fields[6] = int(fields[6])
    return Token._make(fields)


def corpus_parser(corpus_file_name, word_feature_types):
    sentence = list()
    words_counter = Counter()
    start = datetime.now()
    counter = 0
    with open(corpus_file_name, 'r', encoding='utf8') as corpus_file:
        for line in corpus_file:
            if line == '\n':
                for word_feature in word_feature_types:
                    word_feature.add_sentence(sentence)
                sentence.clear()
                if counter % 10000 == 0:
                    print('sentence {0} running time: {1}'.format(counter, datetime.now() - start))
                counter += 1
            else:
                token = line_parser(line)
                words_counter[token.LEMMA] += 1
                sentence.append(token)
    return words_counter
