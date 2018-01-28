import math
import sys

import tweet_sentiment

class ScoreAlgorithm(object):
    def __init__(self, sentiments_dict, tweet_words, scores):
        self.sentiments_dict = sentiments_dict
        self.tweet_words = tweet_words
        self.scores = scores

    def get_score(self, word):
        pass

class AverageScoreAlgorithm(ScoreAlgorithm):
    def get_score(self, word):
        sum_ = 0
        count = 0
        for idx, words in enumerate(self.tweet_words):
            score = self.scores[idx]
            if word in words:
                sum_ += score
                count += 1
        return (float(sum_)/count)

class PosNegLogDifferenceScoreAlgorithm(ScoreAlgorithm):
    def __init__(self, sentiments_dict, tweet_words, scores):
        super(PosNegLogDifferenceScoreAlgorithm, self).__init__(
            sentiments_dict, tweet_words, scores)
        pos_neg_counts = []
        for words in self.tweet_words:
            pos, neg = tweet_sentiment.words_sentiment_counts(
                self.sentiments_dict, words)
            pos_neg_counts.append((pos, neg))
        self.pos_neg_counts = pos_neg_counts

    def get_score(self, word):
        pos = 1
        neg = 1
        for idx, words in enumerate(self.tweet_words):
            if word in words:
                tweet_pos, tweet_neg = self.pos_neg_counts[idx]
                pos += tweet_pos
                neg += tweet_neg
        result = math.log(pos) - math.log(neg)
        return result

def all_words(tweet_words):
    for words in tweet_words:
        for word in words:
            yield word

def get_term_sentiments(sentiments_dict, tweet_words, scores):
    scoring_algorithm = PosNegLogDifferenceScoreAlgorithm(
        sentiments_dict, tweet_words, scores)
    words_set = set(all_words(tweet_words))
    result = {}
    for word in words_set:
        result[word] = scoring_algorithm.get_score(word)
    return result

def get_tweet_words(tweets_filename):
    tweet_words = []
    with open(tweets_filename) as fp:
        for line in fp:
            text = tweet_sentiment.get_tweet_text(line)
            words = tweet_sentiment.get_words(text) if text else []
            tweet_words.append(words)
    return tweet_words

def main():
    sentiments_filename = sys.argv[1]
    tweets_filename = sys.argv[2]
    sentiments_dict = tweet_sentiment.read_sentiments_file(sentiments_filename)
    tweet_words = get_tweet_words(tweets_filename)
    scores = [tweet_sentiment.words_sentiment_score(sentiments_dict, words)
              for words in tweet_words]
    result = get_term_sentiments(sentiments_dict, tweet_words, scores)
    for word, score in result.items():
        print('%s %f' % (word, score))

if __name__ == '__main__':
    main()
