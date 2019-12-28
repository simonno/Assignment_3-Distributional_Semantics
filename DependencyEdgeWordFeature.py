from WordFeature import WordFeature


class DependencyEdgeWordFeature(WordFeature):
    def __init__(self):
        super().__init__()

    def add_sentence(self, sentence):
        for target_word_index in range(len(sentence)):
            target_word_token = sentence[target_word_index]
            if self.is_function_word(target_word_token):
                continue
            self.__add_head_of_target_word(sentence, target_word_token)
            self.__add_sons_of_target_word(sentence, target_word_token)

    def __add_head_of_target_word(self, sentence, target_word_token):
        if target_word_token.HEAD == 0:
            return

        head = sentence[target_word_token.HEAD - 1]
        if self.is_preposition_word(head):
            modified_token = self.search_modified_by_preposition(head, sentence)
            if not modified_token:
                return
            dependency = target_word_token.DEPREL + ' ' + head.DEPREL
            lemma = head.LEMMA + ' ' + modified_token.LEMMA
        else:
            dependency = target_word_token.DEPREL
            lemma = head.LEMMA
        self.__add_feature(target_word_token.LEMMA, lemma, dependency, 1)

    def __add_sons_of_target_word(self, sentence, target_word_token):
        for token in sentence:
            if token.HEAD == target_word_token.ID:

                if self.is_preposition_word(token):
                    modifies_token = self.search_modifies_the_preposition(token, sentence)
                    if not modifies_token:
                        continue
                    dependency = token.DEPREL + ' ' + modifies_token.DEPREL
                    lemma = token.LEMMA + ' ' + modifies_token.LEMMA
                else:
                    dependency = token.DEPREL
                    lemma = token.LEMMA

                self.__add_feature(target_word_token.LEMMA, lemma, dependency, -1)

    def __add_feature(self, target_word, feature, feature_dep, direction):
        self._word_feature[target_word][(feature, feature_dep, direction)] += 1

    @staticmethod
    def search_modifies_the_preposition(preposition_token, sentence):
        for token in sentence:
            if token.HEAD == preposition_token.ID and WordFeature.is_noun_word(token):
                return token
        return None

    @staticmethod
    def search_modified_by_preposition(preposition_token, sentence):
        for token in sentence:
            if token.ID == preposition_token.ID:
                return token
        return None
