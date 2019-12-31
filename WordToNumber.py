from collections import defaultdict


class WordToNumber:
    def __init__(self):
        self._number_key_of_word = defaultdict()
        self._last_key = 0

    def get_word_by_key(self, word_key):
        for word, key in self._number_key_of_word.items():
            if word_key == key:
                return word

    def convert_keys_to_words(self, keys_list):
        words = list()
        for key in keys_list:
            words.append(self.get_word_by_key(key))
        return words

    def get_number_key(self, word):
        if word in self._number_key_of_word.keys():
            return self._number_key_of_word[word]

        self._last_key += 1
        self._number_key_of_word[word] = self._last_key
        return self._last_key
