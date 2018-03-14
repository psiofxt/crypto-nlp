# stdlib

# third-party
import praw

# local
from config import Config


def reddit_client():
    config = Config()

    reddit = praw.Reddit(
        client_id = config.reddit_id,
        client_secret = config.reddit_secret,
        user_agent = 'crypto-nlp-api'
    )

    return reddit


def get_posts(subreddit, style, limit):
    subreddit = r.subreddit(subreddit)
    posts = getattr(subreddit, style)(limit=limit)
    return posts
