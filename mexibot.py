#!/usr/bin/env python

"""
By: Alan Bouzek

/u/mexibot translator bot for Reddit
https://github.com/abouzek/reddit_scripts

"""

import praw, goslate, json
from collections import deque
from time import sleep

def check(comment):
    size = len(comment.body)
    return (size > settings['min_length'] and size < settings['max_length']
        and comment.author.name != settings['username']
        and any(word in comment.body for word in set(settings['keywords'])))

def action(comment):
    print "Replying to comment: " + comment.body + "\n"
    text = gs.translate(comment.body, 'es')
    text += settings['signature']
    comment.reply(text)

def run_bot():
    cache = deque(maxlen=200)
    count = 0
    for s in settings['subreddit_names']:
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
    print "Finished. Replied to " + str(count) + " comments."

if __name__ == "__main__":
    settings_file = open('settings.json', 'r')
    settings = json.load(settings_file)
    r = praw.Reddit(settings['user_agent'])
    r.login(settings['username'], settings['password'])
    gs = goslate.Goslate()
    run_bot()

