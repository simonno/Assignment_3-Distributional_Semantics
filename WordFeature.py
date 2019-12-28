from abc import ABC, abstractmethod
from collections import Counter, defaultdict


class WordFeature(ABC):
    def __init__(self):
        self._word_feature = defaultdict(Counter)

    def get_word_feature_dict(self):
        return self._word_feature

    def filter_features(self, most_common=100, at_least_feature_occurrences=75):
        for target_word, word_feature in self._word_feature.items():
            filtered_features = Counter()
            for feature, occurrence in word_feature.items():
                if occurrence >= at_least_feature_occurrences:
                    filtered_features[feature] = occurrence
            self._word_feature[target_word] = Counter(filtered_features.most_common(most_common))

    @abstractmethod
    def add_sentence(self, sentence):
        pass
