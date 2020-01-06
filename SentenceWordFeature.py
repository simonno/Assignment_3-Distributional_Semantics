from WordFeature import WordFeature


class SentenceWordFeature(WordFeature):
    def __init__(self):
        super().__init__()

    def add_sentence(self, sentence):
        for target_word_token in sentence:
            if self._is_function_word(target_word_token):
                continue
            new_sentence = sentence.copy()
            new_sentence.remove(target_word_token)
            for feature_token in new_sentence:
                self._update_word_feature(target_word_token[2], feature_token[2])
