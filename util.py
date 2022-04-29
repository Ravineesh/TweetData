from datetime import datetime
import pandas as pd
import requests


def extract_hash_tags(hash_tag_entries):
    """Return the list of hashtags if present in a tweet.

    :param hash_tag_entries: hash tag dictionary
    :return : list
    """

    hash_tag_list = []
    hashtag = ""
    if len(hash_tag_entries) > 0:
        for entry in range(0, len(hash_tag_entries)):
            hash_tag_list.append(hash_tag_entries[entry]['text'])
    else:
        hash_tag_list.append("#none")

    return hash_tag_list


def extract_user_mention(user_mention_entries):
    """Return the list of user mentions if present in a tweet.

    :param user_mention_entries: user mention dictionary
    :return : list
    """
    user_mention_list = []
    user_mention = ""
    if len(user_mention_entries) > 0:
        for entry in range(0, len(user_mention_entries)):
            user_mention_list.append(user_mention_entries[entry]['screen_name'])
    else:
        user_mention_list.append("#none")

    return user_mention_list


def get_date_time(date_):
    """Extracts the year, month, and day from tweet creation date.

    :param date_: tweet creation datetime object
    :return : datetime object
    """

    date_ = datetime(date_.year, date_.month, date_.day, 0, 0, 0)  # year, #month, # day

    return date_


def tweets_per_day(df):
    """Returns dataframe having tweets per day.

    :param df: Twitter dataframe
    :return : dataframe having tweets per day
    """

    df['date'] = pd.to_datetime(df['tweet_creation_date']).dt.date
    tweets_per_day = pd.Series(df['date']).value_counts().sort_index()
    tweets_per_day.index = pd.DatetimeIndex(tweets_per_day.index)
    df_tweets_per_day = tweets_per_day.rename_axis('date').reset_index(name='Tweet_Count')

    df_tweets_per_day['date'] = df_tweets_per_day['date'].astype(dtype=str)

    return df_tweets_per_day


def tweets_per_month(df):
    """Returns dataframe having tweets per month.

    :param df: Twitter dataframe
    :return : dataframe having tweets per month
    """

    df['monthyear'] = df['tweet_creation_date'].dt.to_period('M')
    df_tweets_per_month = pd.to_datetime(df['tweet_creation_date']).dt.to_period('M').value_counts().sort_index()
    df_tweets_per_month.index = pd.PeriodIndex(df_tweets_per_month.index)

    month_wise_tweets = df_tweets_per_month.rename_axis('Month').reset_index(name='Tweet_Counts')
    month_wise_tweets['Month'] = month_wise_tweets['Month'].astype(dtype=str)

    return month_wise_tweets


def get_top_10_hashtags(df):
    """"Returns the top 10 user mentions from user tweets

    :param df: dataframe of hashtags
    """
    hashtag_list = []
    for index, row in df.iterrows():
        hashtag = row['hashtag']
        if '#none' not in hashtag:
            if len(hashtag) > 0:
                for item in hashtag:
                    hashtag_list.append(item.strip())
            else:
                hashtag_list.append(hashtag[0].strip)

    hash_tag_df = pd.DataFrame(hashtag_list, columns=['hashtag'])
    hash_tag_count = hash_tag_df.hashtag.value_counts()
    hash_tag_count = hash_tag_count.to_frame()
    hash_tag_count['hash_tag'] = hash_tag_count.index
    hash_tag_count.columns = ['count', 'hash_tag']

    return hash_tag_count


def get_user_mentions(df):
    """"Returns the top 10 user mentions from user tweets

    :param df: dataframe of hashtags
    """
    user_mentions_list = []
    for index, row in df.iterrows():
        user_mention = row['user_mention']
        if '#none' not in user_mention:
            if len(user_mention) > 0:
                for user in user_mention:
                    user_mentions_list.append(user.strip())
            else:
                user_mentions_list.append(user_mention[0].strip)

    user_mention_df = pd.DataFrame(user_mentions_list, columns=['user'])
    user_mention_count = user_mention_df.user.value_counts()
    user_mention_count = user_mention_count.to_frame()
    user_mention_count.to_csv('testing.csv')
    user_mention_count['user_mention'] = user_mention_count.index
    user_mention_count.columns = ['count', 'user_mention']

    return user_mention_count


def load_lottieurl(url: str):
    """Load the animation."""

    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()