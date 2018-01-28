
import json
import sys

import tweet_sentiment
import term_sentiment

def get_tweet_data(tweets_filename):
    with open(tweets_filename) as fp:
        data = [json.loads(line) for line in fp]
    return data

def normalize(text):
    return text.encode('utf-8').lower()

def get_tweet_location(tweet_data):
    tweet_user = tweet_data.get('user')
    tweet_location = tweet_data.get('location')
    if not tweet_location:
        return None
    tweet_unicode = tweet_location.encode('utf-8')
    return tweet_unicode

def get_tweet_state(tweet_data):
    pass

def get_state_happiness_scores(scores, tweet_data):
    result = {}
    for idx, tweet in enumerate(tweet_data):
        state = get_tweet_state(tweet)
        if not state:
            continue
        score = scores[idx]

        score_sum, count = result.setdefault(state, (0, 0))
        score_sum += score
        count += 1

        result[state] = (score_sum, count)

    for state, (score, count) in result.items():
        result[state] = float(score)/count

    return result

def find_key_of_max_value(d):
    max_value = None
    max_key = None
    for key, value in d.items():
        if not max_value or value > max_value:
            max_value = value
            max_key = key
    return max_key

def get_happiest_state(scores, tweet_data):
    state_scores = get_state_happiness_scores(scores, tweet_data)
    state = find_key_of_max_value(state_scores)
    return state

def get_tweet_data_score(sentiments_dict, tweet_data):
    tweet_text = tweet_sentiment.get_tweet_data_text(tweet_data)
    if not tweet_text:
        return 0
    score = tweet_sentiment.text_sentiment_score(sentiments_dict, tweet_text)
    return score

def main():
    tweets_filename = sys.argv[1]
    tweet_data = get_tweet_data(tweets_filename)
    for tweet in tweet_data:
        location = get_tweet_location(tweet)
        if not location:
            continue
        print location
    return

    scores = [get_tweet_data_score(sentiments_dict, tweet)
              for tweet in tweet_data]
    state = get_happiest_state(scores, tweet_data)
    print state

if __name__ == '__main__':
    main()
