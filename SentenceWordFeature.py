from collections import defaultdict, Counter


class SentenceWordFeature:
    def __init__(self):
        self.sentence_word_feature = defaultdict(Counter)

    def add_sentence(self, sentence):
        for word in sentence:
            for feature in sentence:
                if feature != word:
                    self.sentence_word_feature[word][feature] += 1




