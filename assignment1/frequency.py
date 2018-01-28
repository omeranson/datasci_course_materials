
import collections
import sys

import term_sentiment

def get_terms_frequency(tweet_words):
    result = collections.defaultdict(int)
    total = 0
    for word in term_sentiment.all_words(tweet_words):
        total += 1
        result[word] += 1
    for word, count in result.items():
        result[word] = float(count)/total
    return result

def main():
    tweets_filename = sys.argv[1]
    tweet_words = term_sentiment.get_tweet_words(tweets_filename)
    result = get_terms_frequency(tweet_words)
    for word, freq in result.items():
        print('%s %f' % (word, freq))

if __name__ == '__main__':
    main()
