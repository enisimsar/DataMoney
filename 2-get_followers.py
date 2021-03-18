import time

import tweepy
from decouple import config
from mongoengine import NotUniqueError, connect
from tqdm import tqdm
from tweepy.error import TweepError

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
            time.sleep(3 * 60)
            pass


user_ids = list(
    User.objects.filter(
        entry__screen_name__ne="ElectraProtocol", entry__protected__ne=True
    ).values_list("user_id")
)

user_ids = list(set(user_ids) - set(UserConnection.objects.values_list("user_id")))


def save_user_connections(user_id):
    for page in limit_handled(
        tweepy.Cursor(
            api.followers_ids,
            user_id=user_id,
        ).pages()
    ):

        for follower in page:
            try:
                uc = UserConnection(user_id=user_id, follower_id=str(follower))
                uc.save()
            except NotUniqueError:
                pass

        time.sleep(61)


for user_id in tqdm(user_ids):
    try:
        save_user_connections(user_id)
    except TweepError as e:
        print(user_id)
        print(e)
