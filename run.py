# stdlib

# third-party

# local
from classifier.train import get_classifier
import collector.reddit as r


# ----------------------------------------
# REDDIT ---------------------------------
# ----------------------------------------
if __name__ == '__main__':
    reddit = r.reddit_client()
    posts = r.get_posts(reddit, 'cryptocurrency', 'hot', 5)
    comments = r.get_all_comments(posts, 'bitcoin')
    #print(len(comments))

    classifier = get_classifier()
