from WordFeature import WordFeature


class WindowWordFeature(WordFeature):
    def __init__(self, window_size=2):
        super().__init__()
        self.__window_size = window_size

    def add_sentence(self, sentence):
        if self.__window_size == 0:
            return
        filtered_sentence = [token for token in sentence if not self.is_function_word(token)]
        for target_word_index in range(len(filtered_sentence)):
            target_word_token = filtered_sentence[target_word_index]
            features = self._get_features(target_word_index, filtered_sentence)
            self.__add_features(target_word_token, features)
            # left_features_tokens = filtered_sentence[:target_word_index]
            # right_features_tokens = filtered_sentence[target_word_index + 1:]
            # self.__add_features(target_word_token, reversed(left_features_tokens))
            # self.__add_features(target_word_token, right_features_tokens)

    def _get_features(self, target_word_index, sentence):
        features = list()
        if target_word_index - self.__window_size >= 0:
            features += sentence[target_word_index - self.__window_size: target_word_index]
        else:
            features += sentence[: target_word_index]

        if target_word_index + self.__window_size < len(sentence):
            features += sentence[target_word_index + 1: target_word_index + self.__window_size]
        else:
            features += sentence[target_word_index + 1:]

        return features

    # def __add_features(self, target_word_token, features_tokens):
    #     window_size = 0
    #     for feature_token in features_tokens:
    #         self._update_word_feature(target_word_token[2], feature_token[2])
    #         window_size += 1
    #
    #         if window_size == self.__window_size:
    #             break
    def __add_features(self, target_word_token, features_tokens):
        for feature_token in features_tokens:
            self._update_word_feature(target_word_token[2], feature_token[2])
