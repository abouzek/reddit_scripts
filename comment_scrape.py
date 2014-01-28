# Alan Bouzek
# Reddit comment word occurrence counter
# Usage: comment_scraper.py <subreddit name> <keyword> [#comments]

import praw, sys

def contains_keyword(comment, keyword):
    return keyword in comment.body

def main():
    if len(sys.argv) < 3:
        print "\nmissing required arguments!\nusage: 'comment_scraper.py subreddit_name keyword [# comments]'"
        exit()

    r = praw.Reddit('abouzek comment_scraper_test')
    subreddit_name = sys.argv[1]
    keyword = sys.argv[2]

    comment_count = 2500
    if len(sys.argv) > 3:
        if int(sys.argv[3]) < 25:
            print "\n# of comments must be >= 25, using default"
        else:
            comment_count = int(sys.argv[3])

    run_scrape(r, subreddit_name, comment_count, keyword)

def run_scrape(r, subreddit_name, comment_count, keyword):
    print "\nFetching first " + str(comment_count) + " comments from subreddit '" + subreddit_name + "'..."
    comments = r.get_comments(subreddit_name, limit=comment_count)
    print "Checking for keyword '" + keyword + "'..."
    count = sum((contains_keyword(comment, keyword) for comment in comments))
    print "\n" + str(count) + " occurences of this word were found."

main()
