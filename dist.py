import praw

import time
import requests
import sys
from datetime import datetime, timedelta


SUBREDDIT = "cs50"

reddit = praw.Reddit('no_more_segfaults')

# Function is modified version of the one found here: https://www.reddit.com/r/redditdev/comments/8r756k/a_dropin_pushshift_replacement_for_the_deprecated/
# Uses Pushshift API to get num of submissions during specified timeframe
def get_num_submissions(subreddit, start=None, end=None, limit=100, extra_query=""):
    """
    A simple function that returns a count of PRAW submission objects during a particular period from a defined sub.
    This function serves as a replacement for the now deprecated PRAW `submissions()` method.

    :param subreddit: A subreddit name to fetch submissions from.
    :param start: A Unix time integer. Posts fetched will be AFTER this time. (default: None)
    :param end: A Unix time integer. Posts fetched will be BEFORE this time. (default: None)
    :param limit: There needs to be a defined limit of results (default: 100), or Pushshift will return only 25.
    :param extra_query: A query string is optional. If an extra_query string is not supplied,
                        the function will just grab everything from the defined time period. (default: empty string)

    Submissions are yielded newest first.

    For more information on PRAW, see: https://github.com/praw-dev/praw
    For more information on Pushshift, see: https://github.com/pushshift/api
    """

    # Default time values if none are defined (credit to u/bboe's PRAW `submissions()` for this section)
    utc_offset = 28800
    now = int(time.time())
    start = max(int(start) + utc_offset if start else 0, 0)
    end = min(int(end) if end else now, now) + utc_offset

    # Format our search link properly.
    search_link = ('https://api.pushshift.io/reddit/submission/search/'
                   '?subreddit={}&after={}&before={}&sort_type=score&sort=asc&limit={}&q={}')
    search_link = search_link.format(subreddit, start, end, limit, extra_query)

    # Get the data from Pushshift as JSON.
    retrieved_data = requests.get(search_link)
    try:
        returned_submissions = retrieved_data.json()['data']
    except:
        print("Failed to parse")
        return 0

    # Return number of returned submissions
    return len(returned_submissions)

def main():
    now = datetime.now()
    current = now.strftime("%m-%d-%Y")
    log_path = r"logs/" + current + "_metrics.txt"
    with open(log_path, "a") as log_file:
        log_file.write("Post Distribution for:\tr/" + SUBREDDIT + "\n\n")
        now = datetime.now()
        previous_midnight = datetime(now.year, now.month, now.day) - timedelta(days=1)
        start = previous_midnight
        end = previous_midnight + timedelta(hours=1)
        distribution = []
        for i in range(24):
            log_file.write("Start:\t" + start.strftime("%m/%d/%Y, %H:%M:%S") + "\n")
            log_file.write("End:\t" + end.strftime("%m/%d/%Y, %H:%M:%S") + "\n")
            count = get_num_submissions(subreddit=SUBREDDIT, start=start.timestamp(), end=end.timestamp())
            distribution.append(count)
            start = end
            end = start + timedelta(hours=1)
            log_file.write("Count:\t" + str(count) + "\n\n")
        log_file.write("Overall distribution:\n\t" + str(distribution) + "\n")

if __name__ == "__main__":
    main()
