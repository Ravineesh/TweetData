import streamlit as st
import config
import tweet
import pandas as pd
import plotly.express as px
from streamlit_lottie import st_lottie
from numerize import numerize
import util
import clean_text

# set the layout of the app
st.set_page_config(layout='wide', page_title='TweetData')

# load animation
load_animation = util.load_lottieurl(config.lottie_animation_url)
st_lottie(load_animation, height=200)

# set the title of the app
st.title('Twitter Data')

# hide the sidebar
st.markdown(""" <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style> """,
            unsafe_allow_html=True)

# about section
with st.expander('About this app'):
    st.write('This is a data collection and visualization app which allows to collect the tweets of Twitter users by using Twitter API.')

# streamlit form
st.subheader('Please enter the below details..')
with st.form('twitter_handle'):
    twitter_handle = st.text_input(label='Twitter handle', placeholder='Paste the twitter handle here...eg. @elonmusk')
    tweet_limit = st.text_input(label='Tweet Limit', placeholder='Number of tweets to be fetched..eg. 500')
    from_date = st.date_input(label='From Date')
    to_date = st.date_input(label='To Date')
    st.form_submit_button(label='Get Tweets')

if twitter_handle == '':
    st.stop()
else:
    tweet_data = tweet.fetch_tweets(twitter_handle, tweet_limit, from_date, to_date)
    user_data = tweet.user_details(twitter_handle)

    st.markdown(""" ## User Details """)
    # metrics
    user_name, verified, location, = st.columns((3, 3, 3))
    followers, friends, total_tweets = st.columns((1, 1, 1))
    user_name.metric("Name", user_data.iloc[0]['user_name'])
    location.metric('Location', user_data.iloc[0]['location'])
    verified.metric("Verified Account", user_data.iloc[0]['verified'])
    friends.metric("Total Friends", user_data.iloc[0]['friends'])
    followers.metric("Total Followers", numerize.numerize(int(user_data.iloc[0]['followers'])))
    total_tweets.metric("Total Tweets", numerize.numerize(int(user_data.iloc[0]['total_tweets'])))

    st.markdown(""" ## Tweets Details """)
    # display dataframe
    if len(tweet_data) == 0:
        st.info('User has not posted any tweets during the defined period')
    else:
        st.info(f'{len(tweet_data)} tweets posted during defined time period')
        st.dataframe(tweet_data)

        # Download Data
        file_name = user_data.iloc[0]['user_name']
        csv = tweet.convert_df(tweet_data)
        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name=f'{file_name}_tweets.csv',
            mime='text/csv',
        )

        # most retweeted tweet
        st.subheader('Most Retweeted Tweet during the period:')
        retweeted_tweet = tweet_data.sort_values('retweets_count', ascending=False).head(1)['tweet_text']
        st.write(f'Tweet: *{retweeted_tweet.iloc[0]}*')

        # most liked tweet
        st.subheader('Most Liked Tweet during the period:')
        liked_tweet = tweet_data.sort_values('like_count', ascending=False).head(1)['tweet_text']
        st.write(f'Tweet: *{liked_tweet.iloc[0]}*')

        # visualization
        tweet_data['tweet_creation_date'] = pd.to_datetime(tweet_data['tweet_creation_date'])

        col1, col2 = st.columns(2)
        with col1:
            # generate graphs for tweets per month
            tweets_per_month = util.tweets_per_month(tweet_data)
            fig_tweets_per_month = px.bar(tweets_per_month, x='Month', y='Tweet_Counts', text_auto='.2s',
                                          title='Tweets posted per Month')
            st.plotly_chart(fig_tweets_per_month)

        with col2:
            # generate graph for tweets per day
            tweets_per_day = util.tweets_per_day(tweet_data)
            fig_tweets_per_day = px.bar(tweets_per_day, x='date', y='Tweet_Count',
                                        title='Tweets posted per Day')
            st.plotly_chart(fig_tweets_per_day)

        hash_tag_graph, user_mention_graph = st.columns(2)
        with hash_tag_graph:
            # generate graphs for top 10 hashtags per month
            hash_tag_df = util.get_top_10_hashtags(tweet_data)
            fig_hash_tag = px.bar(hash_tag_df.sort_values(by='count', ascending=False).head(10), x='hash_tag',
                                  y='count',
                                  text_auto='.2s',
                                  title='Top 10 Hashtags used in the tweets')
            st.plotly_chart(fig_hash_tag)

        with user_mention_graph:
            # generate graphs for user mentions
            user_mention_df = util.get_user_mentions(tweet_data)
            fig_user_mention = px.bar(user_mention_df.sort_values(by='count', ascending=False).head(10),
                                      x='user_mention',
                                      y='count',
                                      text_auto='.2s',
                                      title='Top 10 Users mentions in the tweets')
            st.plotly_chart(fig_user_mention)

        st.subheader('Do you wish to perform Sentiment Analysis for Tweets?')
        with st.expander(label="Click here to run the Sentiment Analysis"):
            run_analysis = st.button(label="Run Sentiment Analysis")
            if run_analysis:
                clean_tweets = clean_text.text_cleaning(tweet_data)
                positive, negative, neutral = clean_text.predict_sentiment(clean_tweets)
                st.info(f'Positive Tweets: {positive} , Negative Tweets: {negative}, Neutral Tweets: {neutral}')

        # reset the data
        config.reset_data()
