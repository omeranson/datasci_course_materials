import collections
import json
import re
import six
import sys


class HashtagCounter(object):
    def __init__(self):
        self.count = collections.defaultdict(int)

    def count_hashtags_from_filename(self, filename):
        with open(filename) as f:
            for line in f:
                self.count_hashtags_from_tweet_str(line)

    def count_hashtags_from_tweet_str(self, tweet_str):
        tweet_data = json.loads(tweet_str)
        self.count_hashtags_from_tweet_data(tweet_data)

    def count_hashtags_from_tweet_data(self, tweet_data):
        try:
            entities = tweet_data['entities']
            hashtags = entities['hashtags']
        except KeyError:
            return  # Nothing to do
        for hashtag in hashtags:
            try:
                hashtag_str = hashtag['text']
            except KeyError:
                continue  # Skip this one
            if six.PY2:
                hashtag_str = hashtag_str.encode('utf-8')
            self.count[hashtag_str] += 1


def hashtag_count_pair_cmp(i1, i2):
    hashtag1, count1 = i1
    hashtag2, count2 = i2
    return cmp(count1, count2)

def main():
    counter = HashtagCounter()
    tweets_filename = sys.argv[1]
    counter.count_hashtags_from_filename(tweets_filename)
    hashtag_list = list(counter.count.items())
    hashtag_list = sorted(hashtag_list, key=lambda i: i[1])
    for hashtag, count in reversed(hashtag_list):
        print("%s %d" % (hashtag, count))

if __name__ == '__main__':
    main()
