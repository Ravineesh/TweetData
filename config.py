user_name = []
user_screen_name = []
source = []
language = []
tweet_text = []
tweet_creation_date = []
retweets_count = []
like_count = []
hashtag = []
user_mention = []
lottie_animation_url = 'https://assets5.lottiefiles.com/private_files/lf30_oahjps8u.json'

# Twitter Columns
tweet_columns = ['user_name', 'user_screen_name', 'tweet_text',
                 'tweet_creation_date', 'language', 'retweets_count', 'like_count',
                 'hashtag', 'user_mention', 'tweet_source']


follower_columns = ["name", "screen_name", "location", "description", "followers_count",
                    'friends_count', "total_tweets", "created_at",  "verified"]


user_details_columns = ['user_name', 'location', 'verified', 'followers',
                        'friends', 'total_tweets', 'joining_date']

data = [user_name, user_screen_name, source, language, tweet_text, tweet_creation_date,
        retweets_count, like_count, hashtag, user_mention]


def reset_data():
    """Clears the data."""
    for item in data:
        item.clear()
