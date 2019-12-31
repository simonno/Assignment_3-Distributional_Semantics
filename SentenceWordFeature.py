from datetime import datetime

from WordFeature import WordFeature


class SentenceWordFeature(WordFeature):
    def __init__(self):
        super().__init__()

    def add_sentence(self, sentence):
        for target_word_token in sentence:
            if self.is_function_word(target_word_token):
                continue
            for feature_token in sentence:
                if feature_token != target_word_token:
                    self._update_word_feature(target_word_token[2], feature_token[2])
                    # self._word_feature[target_word_token.LEMMA][feature_token.LEMMA] += 1