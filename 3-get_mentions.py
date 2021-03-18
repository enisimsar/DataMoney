import json
import time

import tweepy
from decouple import config
from mongoengine import NotUniqueError, connect
from tqdm import tqdm
from tweepy.error import TweepError

from models.user import User, UserMentions

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

client = tweepy.Client(
    config("TWITTER_BEARER_TOKEN"),
    consumer_key,
    consumer_secret,
    access_key,
    access_secret,
)


user_ids = list(User.objects.filter(entry__protected__ne=True).values_list("user_id"))


def save_user_mentions(user_id):
    pagination_token = None
    r = {}
    first_run = True
    while first_run or "next_token" in r:
        first_run = False
        try:
            r = client.get_users_mentions(
                id=user_id,
                max_results=100,
                pagination_token=pagination_token,
                expansions=["author_id"],
                tweet_fields=["created_at"],
            )

            if r is None or r.data is None:
                break

            if "next_token" in r.meta:
                pagination_token = r.meta["next_token"]

            for t in r.data:
                try:
                    uc = UserMentions(
                        user_id=user_id,
                        from_id=str(t.author_id),
                        mention_id=str(t.id),
                        published_at=t.created_at,
                    )
                    uc.save()
                except NotUniqueError:
                    pass
        except json.JSONDecodeError:
            first_run = True
            print("sleep 15 mins")
            time.sleep(60 * 15 + 1)


for user_id in tqdm(user_ids):
    try:
        save_user_mentions(user_id)
    except TweepError as e:
        print(user_id)
        print(e)
