import pandas as pd
import string  # for removing punctuations marks
import re  # for removing url
import demoji  # for removing emoticons
from textblob import TextBlob
import spacy  # for tokenization
from spacy.lang.en import English
from spacy.lang.en.stop_words import STOP_WORDS as eng_stop_words
import streamlit as st

demoji.download_codes()  # download emoticons
punctuation_marks = list(string.punctuation)


def tokenization_en(input_string, stop_words):
    nlp = English()
    input_text = nlp(input_string)
    token_list = []
    for token in input_text:
        if token.text not in stop_words:
            token_list.append(token.text)

    return token_list


def remove_punctuation(input_string):
    result = []
    for word in input_string:
        if bool(word.translate(str.maketrans('', '', string.punctuation))):
            result.append(word)

    return result


def remove_emoticons(input_string):
    result = []
    for word in input_string:
        if len(demoji.findall(word)) == 0:
            result.append(word)

    return result


def remove_numbers(input_string):
    result = []
    for word in input_string:
        result.append(re.sub(r'\d+', '', word))

    return result


def remove_non_ascii(input_string):
    result = []
    for word in input_string:
        word = word.encode("ascii", "ignore")
        result.append(word.decode())

    return result


def remove_URL(input_string):
    result = []
    for token in input_string:
        result.append(re.sub(r'http\S+', "", token))
    return result


def remove_empty_strings(input_string):
    result = []
    for word in input_string:
        word.strip()
        if word != "":
            result.append(word)

    return result


def text_preprocessing(input_string):
    text = tokenization_en(input_string, eng_stop_words)
    text = remove_punctuation(text)
    text = remove_emoticons(text)
    text = remove_numbers(text)
    text = remove_non_ascii(text)
    text = remove_URL(text)
    text = remove_empty_strings(text)
    result = ' '.join([elem for elem in text])

    return result


def text_cleaning(df):
    clean_text = []
    st.markdown(""" ##### Cleaning Tweets .... """)
    my_bar = st.progress(1)
    for index, row in df.iterrows():

        if row['language'] == 'en':
            clean_text.append(text_preprocessing(row['tweet_text']))
        value_ = (index / len(df))
        my_bar.progress(value_)
        if index == len(df) - 1:
            diff = 1 - value_
            my_bar.progress(value_ + diff)

    return clean_text


def predict_sentiment(clean_text):
    positive = 0
    negative = 0
    neutral = 0
    st.markdown(""" ##### Predicting Tweets Sentiments .... """)
    my_bar = st.progress(1)
    i = 1
    for tweet in clean_text:
        value_ = (i / len(clean_text))
        i += 1
        my_bar.progress(value_)
        blob = TextBlob(tweet)
        polarity = blob.polarity
        if polarity < 0:
            negative += 1
        elif polarity == 0:
            neutral += 1
        else:
            positive += 1

    return positive, negative, neutral
