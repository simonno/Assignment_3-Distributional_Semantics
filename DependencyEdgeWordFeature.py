from WordFeature import WordFeature


class DependencyEdgeWordFeature(WordFeature):
    def __init__(self):
        super().__init__()

    def add_sentence(self, sentence):
        for target_word_index in range(len(sentence)):
            target_word_token = sentence[target_word_index]
            self.__add_head_of_target_word(sentence, target_word_token)
            self.__add_sons_of_target_word(sentence, target_word_token)

    def __add_head_of_target_word(self, sentence, target_word_token):
        if target_word_token.HEAD == 0:
            return

        head = sentence[target_word_token.HEAD - 1]
        if head.CPOSTAG == 'IN':
            prepostion_lemma = head.LEMMA
            head = sentence[head.HEAD - 1]
            self.__add_feature(sentence, , )
        else:
            self.__add_feature(target_word_token.LEMMA, head.LEMMA, target_word_token.DEPREL, 1)

    def __add_sons_of_target_word(self, sentence, target_word_token):
        for token in sentence:
            if token.HEAD == target_word_token.ID:
                self.__add_feature(target_word_token.LEMMA, token.LEMMA, token.DEPREL, -1)

    def __add_feature(self, target_word, feature, feature_dep, direction):
        self._word_feature[target_word][(feature, feature_dep, direction)] += 1
