import time

import tweepy
from decouple import config
from mongoengine import NotUniqueError, connect
from tqdm import tqdm

from models.user import User, UserConnection

__author__ = "Enis Simsar"


connect(
    config("MONGODB_DB"),
    username=config("MONGODB_USER"),
    password=config("MONGODB_PASSWORD"),
    host=config("MONGODB_HOST"),
    port=config("MONGODB_PORT", cast=int),
    authentication_source="admin",
    connect=False,
)

# Twitter API credentials
consumer_key = config("TWITTER_CUSTOMER_KEY")
consumer_secret = config("TWITTER_CUSTOMER_SECRET")
access_key = config("TWITTER_ACCESS_KEY")
access_secret = config("TWITTER_ACCESS_SECRET")

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)


def limit_handled(cursor):
    while True:
        try:
            yield next(cursor)
        except tweepy.RateLimitError:
            print("Sleep 15 mins")
            time.sleep(15 * 60)
            pass


for page in limit_handled(
    tweepy.Cursor(
        api.followers,
        screen_name="ElectraProtocol",
        count=200,
    ).pages()
):

    for follower in tqdm(page):
        j = follower._json
        try:
            uc = User(user_id=j["id_str"], entry=j)
            uc.save()
        except NotUniqueError:
            pass

        try:
            uc = UserConnection(user_id="917007096209723392", follower_id=j["id_str"])
            uc.save()
        except NotUniqueError:
            pass

    time.sleep(61)
