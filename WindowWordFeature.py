from datetime import datetime

from WordFeature import WordFeature


class WindowWordFeature(WordFeature):
    def __init__(self, window_size=2):
        super().__init__()
        self.__window_size = window_size

    def add_sentence(self, sentence):
        if self.__window_size == 0:
            return
        for target_word_index in range(len(sentence)):
            target_word_token = sentence[target_word_index]
            if self.is_function_word(target_word_token):
                continue
            left_features_tokens = sentence[:target_word_index]
            right_features_tokens = sentence[target_word_index + 1:]
            self.__add_features(target_word_token, reversed(left_features_tokens))
            self.__add_features(target_word_token, right_features_tokens)

    def __add_features(self, target_word_token, features_tokens):
        window_size = 0
        for feature_token in features_tokens:
            if not self.is_function_word(feature_token):
                self._update_word_feature(target_word_token[2], feature_token[2])
                window_size += 1

            if window_size == self.__window_size:
                break
