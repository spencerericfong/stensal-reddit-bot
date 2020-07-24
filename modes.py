from datetime import datetime
import sys

from prototype import *


def manual():
    """
    Runs the manual mode of the bot, requires user input
    Can only monitor one subreddit at a time
    """
    # Logs in using /u/no_more_segfaults
    print("Logging into reddit...")
    try:
        reddit = Reddit()
    except:
        print("Error logging in! Now exiting...")
        sys.exit(1)
    print("Successfully logged in!")
    print("-------------------------------------")

    # Accesses chosen subreddit to monitor
    monitor_sub_name = input("Which subreddit would you like to monitor?: ")
    try:
        reddit.set_monitor_subreddit_manual(monitor_sub_name)
    except:
        print("Error accessing subreddit! Now exiting...")
        sys.exit(1)
    print("Successfully accessed subreddit!")
    print("-------------------------------------")

    # Accesses chosen subreddit to post to
    post_sub_name = input("Which subreddit would you like to post to?: ")
    try:
        reddit.set_post_subreddit(post_sub_name)
    except:
        print("Error accessing subreddit! Now exiting...")
        sys.exit(1)
    print("Successfully accessed subreddit!")
    print("-------------------------------------")

    # Retrieves n_submissions number of most recent submissions from monitored subreddit
    # Filters out submissions according to KEYWORDS
    n_submissions = int(input("How many submissions would you like to retrieve?: "))
    try:
        submissions = reddit.filter_submissions_manual(n_submissions)
    except:
        print("Error retrieving submissions! Now exiting...")
        sys.exit(1)

    # Prints out tile and link to relevant submissions
    while len(submissions) != 0:
        print("Successfully retrieved submissions!\n")
        print("Relevant Submissions:")
        print("-------------------------------------")
        counter = 1
        for submission in submissions:
            print(str(counter) + ".", submission.title)
            print(submission.url)
            print("-------------------------------------")
            counter += 1

        # Posts chosen submission to post subreddit
        post_num = int(input("Which submission would you like to post? (Enter the #, or 0 to quit): "))
        if post_num == 0:
            print("Now exiting...")
            sys.exit(0)
        else:
            try:
                submission = submissions.pop(post_num - 1)
                reddit.post_submission(submission)
            except:
                print("Error posting! Now exiting...")
                sys.exit(1)
            print("Successfully posted!")
            print("-------------------------------------")

    # Once all available submissions are posted, exits program
    print("No relevant submissions available to post. Now exiting...")
    sys.exit(0)


def auto():
    """
    Runs the automatic mode of the bot, does not require user input
    """
    # Opens up log file to write to, filename is current datetime
    now = datetime.now()
    current = now.strftime("%m-%d-%Y")
    log_path = r"logs/" + current + ".txt"
    with open(log_path, "a") as log_file:

        # Logs in using /u/no_more_segfaults
        now = datetime.now()
        log_file.write(now.strftime("%H:%M:%S") + " " + "Logging into reddit...\n")
        try:
            reddit = Reddit()
        except:
            now = datetime.now()
            log_file.write(now.strftime("%H:%M:%S") + " " + "Error logging in! Now exiting...\n\n\n")
            log_file.close()
            sys.exit(1)
        now = datetime.now()
        log_file.write(now.strftime("%H:%M:%S") + " " + "Successfully logged in!\n")
        log_file.write("-------------------------------------\n")

        # Accesses chosen subreddit(s) to monitor
        now = datetime.now()
        log_file.write(now.strftime("%H:%M:%S") + " " + "Accessing subreddits to monitor...\n")
        try:
            reddit.set_monitor_subreddit_auto()
        except:
            now = datetime.now()
            log_file.write(now.strftime("%H:%M:%S") + " " + "Error accessing subreddits! Now exiting...\n\n\n")
            log_file.close()
            sys.exit(1)
        now = datetime.now()
        log_file.write(now.strftime("%H:%M:%S") + " " + "Successfully accessed subreddits!\n")
        log_file.write("-------------------------------------\n")

        # Accesses chosen subreddit to post to
        now = datetime.now()
        log_file.write(now.strftime("%H:%M:%S") + " " + "Accessing subreddit to post to...\n")
        try:
            reddit.set_post_subreddit()
        except:
            now = datetime.now()
            log_file.write(now.strftime("%H:%M:%S") + " " + "Error accessing subreddit! Now exiting...\n\n\n")
            log_file.close()
            sys.exit(1)
        now = datetime.now()
        log_file.write(now.strftime("%H:%M:%S") + " " + "Successfully accessed subreddit!\n")
        log_file.write("-------------------------------------\n")

        # Retrieves n_submissions number of most recent submissions from monitored subreddit
        # Filters out submissions according to KEYWORDS
        now = datetime.now()
        log_file.write(now.strftime("%H:%M:%S") + " " + "Filtering out submissions...\n")
        try:
            submissions = reddit.filter_submissions_auto()
        except:
            now = datetime.now()
            log_file.write(now.strftime("%H:%M:%S") + " " + "Error retrieving submissions! Now exiting...\n\n\n")
            sys.exit(1)
        now = datetime.now()
        log_file.write(now.strftime("%H:%M:%S") + " " + "Successfully retrieved submissions!\n\n")

        # Prints out title and link to relevant submissions
        log_file.write("Relevant Submissions:\n")
        log_file.write("-------------------------------------\n")
        counter = 1
        for submission in submissions:
            log_file.write("\t" + str(counter) + "." + " " + submission.title + "\n")
            log_file.write("\t" + submission.url + "\n")
            log_file.write("-------------------------------------\n")
            counter += 1

        # Posts all relevant submissions to post subreddit
        now = datetime.now()
        log_file.write("\n" + now.strftime("%H:%M:%S") + " " + "Posting submissions...\n")
        try:
            counter = 1
            for submission in submissions:
                try:
                    reddit.post_submission(submission)
                except praw.exceptions.APIException:
                    log_file.write("\t" + str(counter) + ". " + "This url has already been submitted, skipping...\n")
                finally:
                    counter += 1
        except:
            now = datetime.now()
            log_file.write(now.strftime("%H:%M:%S") + " " + "Error posting! Now exiting...\n\n\n")
            sys.exit(1)
        now = datetime.now()
        log_file.write(now.strftime("%H:%M:%S") + " " + "Successfully finished posting!\n")
        log_file.write("-------------------------------------\n")

        # Finish
        now = datetime.now()
        log_file.write(now.strftime("%H:%M:%S") + " " + "Finished running script, now exiting...\n\n\n")
