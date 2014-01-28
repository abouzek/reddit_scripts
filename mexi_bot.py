#!/usr/bin/env python

import praw, goslate, logging, re
from collections import deque
from time import sleep

def check(comment):
    if len(comment.body) < MAX_LENGTH:
        return any(word in comment.body for word in keywords)

def action(comment):
    print "Replying to comment: " + comment.body
    comment.reply(gs.translate(comment.body, 'es'))

def run_bot(subreddit_names):
    for s in subreddit_names:
        print "Running on subreddit '" + s + "'..."
        comments = r.get_comments(s, limit=None)
        for c in comments:
            if c.id in cache:
                break
            cache.append(c.id)

            if check(c):
                try:
                    action(c)
                except KeyboardInterrupt:
                    quit()
                except praw.errors.APIException, e:
                    print "[ERROR]:", e
                    print "waiting 30 seconds"
                    sleep(30)
                except Exception, e:
                    print "[ERROR]:", e
                    print "continuing with execution"
                    continue

USER = "USER"
PASS = "PASS"
USER_AGENT = "USERAGENT"
MAX_LENGTH = 9000

cache = deque(maxlen=200)
subreddit_names = ['test']
keywords = set(['test', 'taco', 'burrito', 'queso', 'taquito', 'chaquita', 'chalupa', 'horchata', 'tortilla', 'mexi', 'cinco de mayo', 'mexican', 'viva', 'mundo', 'chihuahua'])

r = praw.Reddit(USER_AGENT)
r.login(USER, PASS)
gs = goslate.Goslate()
pattern = re.compile('(taco|burrito|queso|taquito|chaquita|horchata|tortilla|mexi|mexican|viva|mundo|chihuahua)', re.IGNORECASE)

run_bot(subreddit_names)

