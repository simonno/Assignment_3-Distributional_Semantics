# fields_names = ['ID', 'FORM', 'LEMMA', 'CPOSTAG', 'POSTAG', 'FEATS', 'HEAD', 'DEPREL', 'PHEAD', 'PDEPREL']
from collections import Counter

from SentenceWordFeature import SentenceWordFeature


def decomposition(words, index):
    if index + 1 < len(words):
        return words[index], words[:index], words[index + 1:]
    else:
        return words[index], words[:index], []


def update_pairs_counter(pairs_counter, target_word, feature):
    if (target_word, feature) in pairs_counter.keys():
        pairs_counter[(target_word, feature)] += 1
    elif (feature, target_word) in pairs_counter.keys():
        pairs_counter[(feature, target_word)] += 1
    else:
        pairs_counter[(target_word, feature)] = 1


def update_counter(counter_dict, word):
    if word in counter_dict.keys():
        counter_dict[word] += 1
    else:
        counter_dict[word] = 1


def is_function_word(feature):
    return False  # TODO check if feature is a function word.


def update_window_pairs_counter_dict(window_pairs_counter, target_word, left_features, right_features):
    if target_word not in window_pairs_counter.keys():
        window_pairs_counter[target_word] = dict()

    update_features_counter(reversed(left_features), window_pairs_counter[target_word])
    update_features_counter(right_features, window_pairs_counter[target_word])


def update_features_counter(features, counter_dict, window_size=2):
    for feature in features:
        if window_size == 0:
            return

        if not is_function_word(feature):
            update_counter(counter_dict, feature)
            window_size -= 1


def compute_counters(sentences):
    #
    #
    # sentence_word_feature = defaultdict(Counter)
    # window_word_feature = defaultdict(Counter)
    # dependency_word_feature = defaultdict(Counter)
    # words_counter = defaultdict(int)
    #
    # for sentence in sentences:
    #     words_list = parse_words_of_sentence(sentence, words_counter)
    #     update_pairs_counter_dict(sentence_word_feature, window_word_feature, words_list)
    #
    # words_counter = [(k, v) for k, v in words_counter.items() if v > 99]

    number_to_word = dict()
    sentence_word_feature = SentenceWordFeature()
    window_word_feature = WindowWordFeature()
    words_counter = Counter()
    for sentence in sentences:
        words_list = parse_words_of_sentence(sentence, words_counter, number_to_word)
        sentence_word_feature.add_sentence(words_list)
        window_word_feature.add_sentence(words_list)

    return words_counter, sentence_word_feature, window_pairs_counter


def update_pairs_counter_dict(sentence_word_feature, window_word_feature, words_list):
    for index in range(len(words_list)):
        target_word, left_features, right_features = decomposition(words_list, index)
        update_window_pairs_counter_dict(window_word_feature, target_word, left_features, right_features)

        for feature in left_features + right_features:
            update_pairs_counter(sentence_word_feature, target_word, feature)


def parse_words_of_sentence(sentence, words_counter, number_to_word):
    words_list = list()
    for token in sentence:
        word = token.LEMMA
        hash_key = hash(word)
        number_to_word[hash_key] = word
        words_counter[hash_key] += 1
        words_list.append(hash_key)
    return words_list
