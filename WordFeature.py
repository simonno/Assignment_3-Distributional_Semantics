from abc import ABC, abstractmethod
from collections import Counter, defaultdict
from math import log, inf


class WordFeature(ABC):
    _number_key_of_word = defaultdict()
    _number_to_word = list()
    _last_key = -1

    def __init__(self):
        self._word_feature = defaultdict(Counter)
        self._feature_word = defaultdict(list)
        self._total_feature_co_occurrences = Counter()
        self._total_target_word_co_occurrences = Counter()
        self._total_co_occurrences = 0

    def get_word_feature_dict(self):
        return self._word_feature

    def filter_features(self, filtered_target_words, most_common=100, at_least_feature_occurrences=75):
        self._total_co_occurrences = 0
        filtered_word_feature = defaultdict(Counter)
        for target_word in filtered_target_words:
            target_word = WordFeature._get_number_key(target_word)
            word_feature = self._word_feature[target_word]
            filtered_features = Counter()
            for feature, occurrence in word_feature.items():
                if occurrence >= at_least_feature_occurrences:
                    filtered_features[feature] = occurrence
                    self._feature_word[feature].append(target_word)
                    self._total_co_occurrences += 1
                    self._total_feature_co_occurrences[feature] += 1
                    self._total_target_word_co_occurrences[target_word] += 1

            if len(filtered_features.items()):
                filtered_word_feature[target_word] = Counter(dict(filtered_features.most_common(most_common)))
        self._word_feature = filtered_word_feature

    def _update_word_feature(self, target_word, feature):
        target_word2 = WordFeature._get_number_key(target_word)
        feature2 = WordFeature._get_number_key(feature)
        try:
            self._word_feature[target_word2][feature2] += 1
        except MemoryError:
            print('error')

    def _calculate_pmi(self, target_word, feature):
        word_feature_co_occurrences = self._word_feature[target_word][feature]
        if word_feature_co_occurrences == 0:
            return -inf
        return log((word_feature_co_occurrences * self._total_co_occurrences) / (
                self._total_feature_co_occurrences[feature] * self._total_target_word_co_occurrences[target_word]))

    def get_most_similarity_words(self, word, most_common=20):
        similarity = list(sorted(self._similarity_vector(word).items(), reverse=True, key=lambda item: item[1]))
        if most_common < len(similarity):
            similarity = similarity[:most_common]

        similarity = [word for (word, feature) in similarity]
        return similarity

    def _similarity_vector(self, word):
        word = WordFeature._get_number_key(word)
        similarity = defaultdict(float)
        for feature, co_occurrences in self._word_feature[word].items():
            for target_word in self._feature_word[feature]:
                word_pmi = self._calculate_pmi(word, feature)
                target_word_pmi = self._calculate_pmi(target_word, feature)
                if word_pmi == -inf or target_word_pmi == -inf:
                    continue
                similarity[self._get_word_by_number_key(target_word)] += word_pmi * target_word_pmi
        return similarity

    @staticmethod
    def _get_word_by_number_key(number_key):
        return WordFeature._number_to_word[number_key]

    @staticmethod
    def _get_number_key(word):
        if word in WordFeature._number_key_of_word.keys():
            return WordFeature._number_key_of_word[word]

        WordFeature._last_key += 1
        WordFeature._number_key_of_word[word] = WordFeature._last_key
        WordFeature._number_to_word.append(word)
        return WordFeature._last_key

    @staticmethod
    def is_function_word(token):
        return True if token[3] in ['DT', 'PRP', 'WDT', 'IN', 'CC', 'RB', 'RP'] or token[7] == 'p' else False

    @staticmethod
    def is_preposition_word(token):
        return True if token[3] == 'IN' else False

    @staticmethod
    def is_noun_word(token):
        return True if token[3] in ['NN', 'NNP', 'NNS'] else False

    @abstractmethod
    def add_sentence(self, sentence):
        pass
