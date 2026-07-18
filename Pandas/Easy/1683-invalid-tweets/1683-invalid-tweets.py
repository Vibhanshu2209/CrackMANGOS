import pandas as pd

def invalid_tweets(tweets: pd.DataFrame) -> pd.DataFrame:

    invalid_tweets = tweets[tweets["content"].str.len() > 15]
    return invalid_tweets[["tweet_id"]]
    