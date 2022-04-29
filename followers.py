import streamlit as st
import config
import tweet
import pandas as pd
import plotly.express as px
from streamlit_lottie import st_lottie
from numerize import numerize
import util

# set the layout of the app
st.set_page_config(layout='wide', page_title='TweetData')

# load animation
load_animation = util.load_lottieurl(config.lottie_animation_url)
st_lottie(load_animation, height=200)

# set the title of the app
st.title('Followers Data')

# hide the sidebar
st.markdown(""" <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style> """,
            unsafe_allow_html=True)

# about section
with st.expander('About this app'):
    st.write('This is a data collection app which allows to collect the tweets of Twitter users by using Twitter API.')

# streamlit form
st.subheader('Please enter the below details..')
with st.form('twitter_handle'):
    twitter_handle = st.text_input(label='Twitter handle', placeholder='Paste the twitter handle here...eg. @twiiter')
    st.form_submit_button(label='Get Followers')

if twitter_handle == '':
    st.stop()
else:
    followers_json_data = tweet.get_followers(twitter_handle)
    followers_data = tweet.get_follower_data(followers_json_data)

    st.markdown(""" ## Followers Details """)
    # metrics
    followers_count, verified_followers = st.columns((1, 1))
    followers_count.metric("Total Followers", followers_data['screen_name'].count())
    verified_followers.metric('Verified Followers', followers_data[followers_data.verified == 'TRUE']['verified'].count())
    st.subheader('Followers list')
    st.dataframe(followers_data)

    # Download Data
    file_name = twitter_handle
    csv = tweet.convert_df(followers_data)
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name=f'{file_name}_followers.csv',
        mime='text/csv',
    )
