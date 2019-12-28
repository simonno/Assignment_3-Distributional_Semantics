from abc import ABC, abstractmethod
from collections import Counter, defaultdict


class WordFeature(ABC):
    def __init__(self):
        self._word_feature = defaultdict(Counter)

    def get_word_feature_dict(self):
        return self._word_feature

    def filter_features(self, most_common=100, at_least_feature_occurrences=75):
        filtered_word_feature = defaultdict(Counter)
        for target_word, word_feature in self._word_feature.items():
            filtered_features = Counter()
            for feature, occurrence in word_feature.items():
                if occurrence >= at_least_feature_occurrences:
                    filtered_features[feature] = occurrence

            if len(filtered_features.items()):
                filtered_word_feature[target_word] = Counter(filtered_features.most_common(most_common))
        self._word_feature = filtered_word_feature

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
