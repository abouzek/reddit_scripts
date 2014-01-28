#!/usr/bin/env python

import praw, goslate, logging, re
from collections import deque
from time import sleep

def check(comment):
    size = len(comment.body)
    return (size > MIN_LENGTH and size < MAX_LENGTH
        and comment.author.name != USER
        and any(word in comment.body for word in KEYWORDS))

def action(comment):
    print "Replying to comment: " + comment.body
    text = gs.translate(comment.body, 'es')
    text += SIGNATURE
    comment.reply(text)

def run_bot():
    cache = deque(maxlen=200)
    count = 0
    for s in SUBREDDIT_NAMES:
        print "Running on subreddit '" + s + "'..."
        comments = r.get_comments(s, limit=None)
        for c in comments:
            if c.id in cache:
                break
            cache.append(c.id)

            if check(c):
                try:
                    action(c)
                    count += 1
                except KeyboardInterrupt:
                    quit()
                except Exception, e:
                    print "[ERROR]:", e
                    print "Waiting 30 seconds..."
                    sleep(30)
    print "Finished. Replied to " + count + " comments."

USER = "USER"
PASS = "PASS"
USER_AGENT = "USERAGENT"
MIN_LENGTH = 500
MAX_LENGTH = 5000
SIGNATURE = "\n\n\n*-- Viva la mexibot! Translated because you used a particularly* **spicy** *word.*"
SUBREDDIT_NAMES = ['tacobell']
KEYWORDS = set(['taco', 'burrito', 'queso', 'taquito', 'chaquita', 'chalupa', 'horchata', 'tortilla', 'cinco de mayo', 'mexican', 'chihuahua'])

r = praw.Reddit(USER_AGENT)
r.login(USER, PASS)
gs = goslate.Goslate()
run_bot()

