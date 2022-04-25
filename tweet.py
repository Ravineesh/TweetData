import pandas as pd
import streamlit as st
import config
import tweepy
import util
import os

# Creating an OAuthHandler instance.
auth = tweepy.OAuthHandler(st.secrets["API_KEY"], st.secrets["API_SECRET_KEY"])
# Setting the access token provided by the Twitter
auth.set_access_token(st.secrets["ACCESS_TOKEN"], st.secrets["ACCESS_TOKEN_SECRET"])

# The API class is used to provide access to entire twitter RESTFul API methods
api = tweepy.API(auth)


def fetch_tweets(twitter_handle, tweet_limit, from_date, to_date):
    """Fetch the tweets from Twitter API and returns pandas dataframe.

    :param twitter_handle: Twitter handle of the user
    :param tweet_limit: number of tweets to be fetched (upper cap)
    :param from_date: date
    :param to_date: date
    :return : dataframe
    """

    tweets = tweepy.Cursor(api.user_timeline, id=twitter_handle, tweet_mode='extended').items(int(tweet_limit))
    start_date = util.get_date_time(from_date)
    end_date = util.get_date_time(to_date)

    for tweet in tweets:
        creation_date = util.get_date_time(tweet.created_at)
        if (creation_date > start_date) & (creation_date < end_date):
            config.user_name.append(tweet.user.name)
            config.user_id.append(tweet.user.id_str)
            config.user_screen_name.append(tweet.user.screen_name)
            config.source.append(tweet._json["source"])
            config.language.append(tweet._json["lang"])
            config.tweet_text.append(tweet.full_text)
            config.tweet_creation_date.append(tweet.created_at)
            config.retweets_count.append(tweet._json["retweet_count"])
            config.like_count.append(tweet._json["favorite_count"])

            # If tweet contains hashtags
            config.hashtag.append(util.extract_hash_tags(tweet._json["entities"]["hashtags"]))

            # If tweet contains user_mentions
            config.user_mention.append(util.extract_user_mention(tweet._json["entities"]["user_mentions"]))

    df = pd.DataFrame(zip(config.user_id, config.user_name, config.user_screen_name, config.tweet_text,
                          config.tweet_creation_date, config.language, config.retweets_count,
                          config.like_count, config.hashtag, config.user_mention, config.source)
                      , columns=config.tweet_columns)

    return df


def user_details(twitter_handle):
    """Fetch the user details from Twitter API and returns pandas dataframe.

    :param twitter_handle: twitter handle of the user
    :return : dataframe
    """

    user_name = []
    user_location = []
    is_verified = []
    followers_count = []
    friends_count = []
    tweet_count = []
    joining_date = []

    user_detail = api.get_user(screen_name=twitter_handle)
    user_name.append(user_detail.name)
    user_location.append(user_detail.location)
    is_verified.append(user_detail.verified)
    followers_count.append(user_detail.followers_count)
    friends_count.append(user_detail.friends_count)
    tweet_count.append(user_detail.statuses_count)
    joining_date.append(user_detail.created_at)

    return pd.DataFrame(zip(user_name, user_location, is_verified, followers_count, friends_count, tweet_count,
                            joining_date), columns=config.user_details_columns)


@st.cache
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')
