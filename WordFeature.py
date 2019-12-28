import math
from abc import ABC, abstractmethod
from collections import Counter, defaultdict


class WordFeature(ABC):
    def __init__(self):
        self._word_feature = defaultdict(Counter)
        self._feature_word = defaultdict(list)
        self._last_key = 0
        self._number_key_of_word = defaultdict()
        self._total_feature_co_occurrences = defaultdict(int)
        self._total_target_word_co_occurrences = defaultdict(int)
        self._total_co_occurrences = 0

    def get_word_feature_dict(self):
        return self._word_feature

    def filter_features(self, filtered_target_words, most_common=100, at_least_feature_occurrences=75):
        self._total_co_occurrences = 0
        filtered_word_feature = defaultdict(Counter)
        for target_word in filtered_target_words:
            word_feature = self._word_feature[hash(target_word)]
            filtered_features = Counter()
            for feature, occurrence in word_feature.items():
                if occurrence >= at_least_feature_occurrences:
                    filtered_features[feature] = occurrence
                    self._feature_word[feature].append(target_word)
                    self._total_co_occurrences += 1
                    self._total_feature_co_occurrences[feature] += 1
                    self._total_target_word_co_occurrences[feature] += 1

            if len(filtered_features.items()):
                filtered_word_feature[target_word] = Counter(filtered_features.most_common(most_common))
        self._word_feature = filtered_word_feature

    def _update_word_feature(self, target_word, feature):

        # hash_target_word = hash(target_word)
        # hash_feature = hash(feature)
        # self._number_key_of_word[hash_target_word] = target_word
        # self._number_key_of_word[feature] = feature
        self._word_feature[self._get_number_key(target_word)][self._get_number_key(feature)] += 1

    def _calculate_pmi(self, target_word, feature):
        return math.log((self._word_feature[target_word][feature] * self._total_co_occurrences) / (
                self._total_feature_co_occurrences[feature] * self._total_target_word_co_occurrences[target_word]))

    def get_most_similarity_words(self, word, most_common=20):
        similarity = list(sorted(self.similarity_vector(word), key=lambda k, v: v))
        if most_common > len(similarity):
            return similarity
        return similarity[:most_common]

    def similarity_vector(self, word):
        word = self._get_number_key(word)
        similarity = defaultdict(float)
        for feature, co_occurrences in self._word_feature[word].items():
            for target_word in self._feature_word[feature]:
                similarity[self._number_key_of_word[target_word]] += self._calculate_pmi(word, feature) * \
                                                                     self._calculate_pmi(target_word, feature)
        return similarity

    def _get_number_key(self, word):
        if word in self._number_key_of_word.keys():
            return self._number_key_of_word[word]
        else:
            self._last_key += 1
            self._number_key_of_word[word] = self._last_key
            return self._last_key

    @staticmethod
    def is_function_word(token):
        return True if token.CPOSTAG in ['DT', 'PRP', 'WDT', 'IN', 'CC', 'RB', 'RP', ',', '.', ':'] else False

    @staticmethod
    def is_preposition_word(token):
        return True if token.CPOSTAG == 'IN' else False

    @staticmethod
    def is_noun_word(token):
        return True if token.CPOSTAG in ['NN', 'NNP', 'NNS'] else False

    @abstractmethod
    def add_sentence(self, sentence):
        pass
