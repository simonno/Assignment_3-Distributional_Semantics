from WordFeature import WordFeature


class SentenceWordFeature(WordFeature):
    def __init__(self):
        super().__init__()

    def add_sentence(self, sentence):
        filtered_sentence = [token for token in sentence if not self.is_function_word(token)]
        for target_word_token in filtered_sentence:
            features = filtered_sentence.copy()
            features.remove(target_word_token)
            for feature_token in features:
                self._update_word_feature(target_word_token[2], feature_token[2])
