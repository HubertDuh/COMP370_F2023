import pandas as pd
import re


def mentions_trump(text):
    if re.search(r'\WTrump\W', text):
        return 'T'
    else:
        return 'F'


if __name__ == "__main__":
    tweets = pd.read_csv('Data/IRAhandle_tweets_1.csv', nrows=10000)

    engTweets = tweets[tweets['language'] == 'English']
    questionTweets = tweets[~tweets['content'].str.contains('\?')]

    engQuestionTweets = pd.merge(engTweets, questionTweets, how='inner')

    engQuestionTweets['trump_mention'] = engQuestionTweets['content'].apply(mentions_trump)

    trumpTweets = engQuestionTweets.head(10000)

    trumpTweets.to_csv('Data/dataset.tsv', index=False,
                       columns=['tweet_id', 'publish_date', 'content', 'trump_mention'], encoding='utf-8')

    mentionCount = len(trumpTweets[trumpTweets['trump_mention'] == 'T'].index);

    totalTweets = len(trumpTweets.index)

    mentionPercentage = round((mentionCount / totalTweets), 3)

    resultData = {'result': ['frac-trump-mentions'], 'value': [mentionPercentage]}

    resultDf = pd.DataFrame(data=resultData)

    resultDf.to_csv('Data/result.tsv', index=False)

    print(mentionPercentage)
