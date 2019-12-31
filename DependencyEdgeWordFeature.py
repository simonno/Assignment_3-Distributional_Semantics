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
        if target_word_token[6] == 0:
            return

        head = sentence[target_word_token[6] - 1]
        if self.is_preposition_word(head):
            modified_token = self.search_modified_by_preposition(head, sentence)
            if not modified_token:
                return
            dependency = target_word_token[7] + ' ' + head[7]
            lemma = head[2] + ' ' + modified_token[2]
        else:
            dependency = target_word_token[7]
            lemma = head[2]
        self.__add_feature(target_word_token[2], lemma, dependency, 1)

    def __add_sons_of_target_word(self, sentence, target_word_token):
        for token in sentence:
            if token[6] == target_word_token[0]:

                if self.is_preposition_word(token):
                    modifies_token = self.search_modifies_the_preposition(token, sentence)
                    if not modifies_token:
                        continue
                    dependency = token[7] + ' ' + modifies_token[7]
                    lemma = token[2] + ' ' + modifies_token[2]
                else:
                    dependency = token[7]
                    lemma = token[2]

                self.__add_feature(target_word_token[2], lemma, dependency, -1)

    def __add_feature(self, target_word, feature, feature_dep, direction):
        self._update_word_feature(target_word, (feature, feature_dep, direction))
        # self._word_feature[target_word][(feature, feature_dep, direction)] += 1

    @staticmethod
    def search_modifies_the_preposition(preposition_token, sentence):
        for token in sentence:
            if token[6] == preposition_token[0] and WordFeature.is_noun_word(token):
                return token
        return None

    @staticmethod
    def search_modified_by_preposition(preposition_token, sentence):
        for token in sentence:
            if token[0] == preposition_token[0]:
                return token
        return None
