user_name = []
user_id = []
user_screen_name = []
source = []
language = []
tweet_text = []
tweet_creation_date = []
retweets_count = []
like_count = []
hashtag = []
user_mention = []

# Twitter Columns
tweet_columns = ['user_id', 'user_name', 'user_screen_name', 'tweet_text',
                 'tweet_creation_date', 'language', 'retweets_count', 'like_count',
                 'hashtag', 'user_mention', 'tweet_source']

user_details_columns = ['user_name', 'location', 'verified', 'followers',
                        'friends', 'total_tweets', 'joining_date']

data = [user_name, user_id, user_screen_name, source, language, tweet_text, tweet_creation_date,
        retweets_count, like_count, hashtag, user_mention]


def reset_data():
    """Clears the data."""

    for item in data:
        item.clear()
