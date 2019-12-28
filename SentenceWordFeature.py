from WordFeature import WordFeature


class SentenceWordFeature(WordFeature):
    def __init__(self):
        super().__init__()

    def add_sentence(self, sentence):
        for target_word_token in sentence:
            for feature_token in sentence:
                if feature_token != target_word_token:
                    self._word_feature[target_word_token.LEMMA][feature_token.LEMMA] += 1
