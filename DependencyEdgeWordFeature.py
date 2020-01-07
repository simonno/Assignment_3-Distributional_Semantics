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
            modified_tokens = self.search_modified_by_preposition(head, sentence)
            if not modified_tokens:
                return
            dependency = modified_tokens[-1][7]
            lemma = '_'.join([token[2] for token in modified_tokens])
        else:
            dependency = target_word_token[7]
            lemma = head[2]
        self.__add_feature(target_word_token[2], lemma, dependency, 'up')

    def __add_sons_of_target_word(self, sentence, target_word_token):
        for token in sentence:
            if token[6] == target_word_token[0]:

                if self.is_preposition_word(token):
                    modifies_tokens = self.search_modifies_the_preposition(token, sentence)
                    if not modifies_tokens:
                        continue
                    dependency = modifies_tokens[-1][7]
                    lemma = token[2] + '_' + '_'.join([token[2] for token in modifies_tokens])
                else:
                    dependency = token[7]
                    lemma = token[2]

                self.__add_feature(target_word_token[2], lemma, dependency, 'down')

    def __add_feature(self, target_word, feature, feature_dep, direction):
        self._update_word_feature(target_word, '|'.join([feature, feature_dep, direction]))

    @staticmethod
    def search_modifies_the_preposition(preposition_token, sentence):
        for token in sentence:
            if token[6] == preposition_token[0]:
                if WordFeature.is_preposition_word(token):
                    pre_tokens = DependencyEdgeWordFeature.search_modifies_the_preposition(token, sentence)
                    pre_tokens.insert(0, token)
                    return pre_tokens
                else:
                    return [token]
        return list()

    @staticmethod
    def search_modified_by_preposition(preposition_token, sentence):
        pre_tokens = [preposition_token]
        while not WordFeature.is_root(pre_tokens[0]) and WordFeature.is_preposition_word(pre_tokens[0]):
            token = sentence[pre_tokens[0][6] - 1]
            pre_tokens.insert(0, token)
        return pre_tokens
