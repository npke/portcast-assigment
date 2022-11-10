from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist


def get_distinct_words_with_count(paragraph: str) -> FreqDist:
    words = word_tokenize(paragraph.lower())
    freq_dist = FreqDist(words)
    return freq_dist
