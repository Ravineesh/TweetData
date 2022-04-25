# TweetData
An data collection and visualization web app for Twitter


If you want to view the live application, below is the link
https://share.streamlit.io/ravineesh/tweetdata/main/fetch_tweets.py

# Installation instruction for Local
After cloning this repository.

``` 
git clone  https://github.com/Ravineesh/TweetData.git
cd TweetData/
pip install -r requirements.txt  
```

Before running the web app you have export the `API_KEY`, `API_SECRET_KEY`, `ACCESS_TOKEN`, `ACCESS_TOKEN_SECRET` via tha command line. These keys can be generated from your Twitter Developer account.
```
 $export  API_KEY='your_api_key'
 $export  API_SECRET_KEY='your_api_secret_key'
 $export  ACCESS_TOKEN='your_access_token'
 $export  ACCESS_TOKEN_SECRET='your_access_token_secret'
```

Run the following command.

 `` streamlit run fetch_tweets.py ``
