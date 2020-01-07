from collections import Counter
from datetime import datetime

# Token = namedtuple('Token', ['ID', 'FORM', 'LEMMA', 'CPOSTAG', 'POSTAG', 'FEATS', 'HEAD', 'DEPREL', 'PHEAD', 'PDEPREL'])
from WordFeature import WordFeature


def line_parser(line):
    fields = line.strip().split('\t')
    fields[0] = int(fields[0])
    fields[6] = int(fields[6])
    return fields


def corpus_parser(lines, word_feature_types):
    sentence = list()
    words_counter = Counter()
    start = datetime.now()
    counter = 0
    for line in lines:
        if line == '\n':
            for word_feature in word_feature_types:
                word_feature.add_sentence(sentence)
            sentence.clear()
            if counter % 100000 == 0:
                print('sentence {0} running time: {1}'.format(counter, datetime.now() - start))
            counter += 1
        else:
            token = line_parser(line)
            if not WordFeature.is_function_word(token):
                words_counter[token[2]] += 1
            sentence.append(token)

    print('sentence {0} running time: {1}'.format(counter, datetime.now() - start))
    return words_counter
