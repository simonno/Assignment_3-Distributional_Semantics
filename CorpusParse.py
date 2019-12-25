from collections import namedtuple

Token = namedtuple('Token', ['ID', 'FORM', 'LEMMA', 'CPOSTAG', 'POSTAG', 'FEATS', 'HEAD', 'DEPREL', 'PHEAD', 'PDEPREL'])


def line_parser(line):
    fields = line.strip().split('\t')
    return Token._make(fields)


def corpus_parser(corpus_file_name):
    sentences = [list()]
    with open(corpus_file_name, 'r', encoding='utf8') as corpus_file:
        for line in corpus_file:
            if line == '\n':
                sentences.append(list())
            else:
                sentences[-1].append(line_parser(line))
    return sentences
