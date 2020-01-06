from collections import defaultdict


def calculate_MAP(words_and_judgments_file):
    judgments = {'+': 1, '-': 0}

    with open(words_and_judgments_file, 'r') as similarities:
        words = set()
        words_and_judgments = defaultdict(list)

        for line in similarities:
            words_and_judgments_line = line.split()
            for index, word_and_judgment in enumerate(words_and_judgments_line):
                splited_judgement = word_and_judgment.split('(')
                word = splited_judgement[0]
                words.add(word)
                words_and_judgments[index].append(judgments[splited_judgement[1][0]])

    for context_type, judgments in words_and_judgments.items():
        map = 0

        for index, judgment in enumerate(judgments):
            if judgment:
                map += sum(judgments[:(index + 1)]) / (index + 1)

        map /= len(words)

        print(context_type)
        print(map)


if __name__ == '__main__':
    calculate_MAP("car_semantic_topic.txt")
