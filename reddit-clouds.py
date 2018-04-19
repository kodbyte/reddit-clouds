# -*- coding: utf-8 -*-
"""
Program to extract comments from top 100 all time posts for a list of
subreddits and create a wordcloud.
"""

import praw
from wordcloud import WordCloud
from os import path


class Reddit(object):

    def __init__(self):
        self.r = praw.Reddit(
                user_agent=('Comment Word Cloud Creator v1.0 by /u/zadixx'),
                client_id='',
                client_secret='')

    def get_posts(self, sub):
        top_posts = []
        for post in self.r.subreddit(sub).top(limit=100):
            top_posts.append(post.id)
        return top_posts

    def get_comments(self, post_id, sub):
        comments = []
        post = self.r.submission(id=post_id)
        post.comments.replace_more(limit=0)
        for comment in post.comments.list():
            if comment.author != 'AutoModerator':
                comments.append(comment.body)
        return comments


class Cloud(object):

    def create_cloud(self, text, sub):
        d = path.dirname(__file__)
        self.cloud = WordCloud(width=1200, height=800).generate(text)
        self.cloud.to_file(path.join(d, '{0}.png'.format(sub)))


# create a reddit ojbect
r = Reddit()

subreddits = ['politics', 'the_donald']

# iterate through the subreddits to build a word cloud for
for subreddit in subreddits:

    top_posts = r.get_posts(subreddit)

    for post in top_posts:
        comments = r.get_comments(post, subreddit)

    # create a wordcloud object
    cloud = Cloud()

    cloud.create_cloud(" ".join(comments), subreddit)
