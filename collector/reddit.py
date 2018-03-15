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


def get_posts(reddit_client, subreddit, style, limit):
    subreddit = reddit_client.subreddit(subreddit)
    posts = getattr(subreddit, style)(limit=limit)
    return posts


def get_all_comments(posts, keyword):
    comments = []
    for post in posts:
        for comment in post.comments.list():
            if keyword in comment.body:
                comments.append(comment.lower())
    return comments
