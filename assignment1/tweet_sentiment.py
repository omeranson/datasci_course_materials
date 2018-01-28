import re
import sys

import json

def read_sentiments_file(filename):
    sentiments_dict = {}
    prog = re.compile('\s+')
    with open(filename) as fp:
        for line in fp:
            items = prog.split(line)
            if not items[-1]:
                items.pop()
            words, score = tuple(items[:-1]), items[-1]
            sentiments_dict[words] = int(score)
    return sentiments_dict

def get_tweet_text(tweet):
    tweet_data = json.loads(tweet)
    return get_tweet_data_text(tweet_data)

def get_tweet_data_text(tweet_data):
    try:
        tweet_text = tweet_data['text']
    except KeyError:
        return None
    tweet_unicode = tweet_text.encode('utf-8').lower()
    return tweet_unicode

def tweet_sentiment_score(sentiments_dict, tweet):
    tweet_unicode = get_tweet_text(tweet)
    if not tweet_unicode:
        return 0
    score = text_sentiment_score(sentiments_dict, tweet_unicode)
    return score

def list_contains_sublist(list_, sublist):
    item = sublist[0]
    while True:
        try:
            index = list_.index(item)
        except Exception:
            return False
        for sublistidx, sublistitem in enumerate(sublist):
            try:
                if list_[index+sublistidx] != sublistitem:
                    break
            except IndexError:
                return False
        else:
            return True
        list_ = list_[index+1:]

def get_words(text):
    prog = re.compile('[a-zA-Z0-9\'_-]+')
    words = prog.findall(text)
    return words

def text_sentiment_score(sentiments_dict, text):
    words = get_words(text)
    return words_sentiment_score(sentiments_dict, words)

def words_sentiment_counts(sentiments_dict, words):
    pos = 0
    neg = 0
    for item, score in sentiments_dict.items():
        if list_contains_sublist(words, item):
            if score > 0:
                pos += 1
            elif score < 0:
                neg += 1
    return pos, neg

def words_sentiment_score(sentiments_dict, words):
    result = 0
    for item, score in sentiments_dict.items():
        if list_contains_sublist(words, item):
            result += score
    return result

def get_tweet_scores(sentiments_dict, tweets_filename):
    with open(tweets_filename) as fp:
        scores = [tweet_sentiment_score(sentiments_dict, line) for line in fp]
    return scores

def main():
    sentiments_filename = sys.argv[1]
    tweets_filename = sys.argv[2]
    sentiments_dict = read_sentiments_file(sentiments_filename)
    scores = get_tweet_scores(sentiments_dict, tweets_filename)
    for score in scores:
        print score

if __name__ == '__main__':
    main()
