import praw


"""
Keys are subreddits, values are a list of revelant keywords for that subreddit
"""
KEYWORDS = {
    "cs50" : [
        "speller",
        "memory leaks",
        "c",
        "segmentation fault",
        "segmentation faults",
        "segfault",
        "segfaults",
        "pointer",
        "tutor",
        "tutoring",
        "[c]",
        "c.",
        "c?"
    ],
    "c_programming" : [
        "segmentation fault",
        "segmentation faults",
        "segfault",
        "segfaults",
        "pointer",
        "memory leaks",
        "cs50",
        "tutor",
        "tutoring",
        "[c]",
        "c.",
        "c?"
    ],
    "learnprogramming" : [
        "c",
        "segmentation fault",
        "segmentation faults",
        "segfault",
        "segfaults",
        "pointer",
        "memory leaks",
        "cs50",
        "tutor",
        "tutoring",
        "[c]",
        "c++",
        "c.",
        "c?"
    ],
    "askprogramming" : [
        "c",
        "segmentation fault",
        "segmentation faults",
        "segfault",
        "segfaults",
        "pointer",
        "memory leaks",
        "cs50",
        "tutor",
        "tutoring",
        "[c]",
        "c.",
        "c?"
    ],
    "codinghelp" : [
        "c",
        "c++",
        "c.",
        "c?"
    ],
    "homeworkhelp" : [
        "c",
        "c++",
        "c.",
        "c?"
    ],
    "cprogramming" : [

    ]
}


class Reddit:
    """
    Reddit (PRAW) instance class to access reddit API
    """

    def __init__(self):
        """
        Initializes reddit instance using app data in praw.ini
        TODO: Make login dynamic per user
        """
        self.reddit = praw.Reddit('no_more_segfaults')
        self.monitor_subreddit = None
        self.post_subreddit = None


    def set_monitor_subreddit_manual(self, sub_name: str) -> None:
        """
        Sets the monitored subreddit instance to an instance of sub_name
        :param sub_name: name of the subreddit to be accessed
        """
        self.monitor_subreddit = self.reddit.subreddit(sub_name)
        print("Monitored subreddit has been set to:", self.monitor_subreddit.display_name)


    def set_monitor_subreddit_auto(self, sub_names: list=KEYWORDS.keys()) -> None:
        """
        Sets the monitored subreddit instances to instances of values in sub_names
        :param sub_names: list of names of subreddits to be accessed
        """
        self.monitor_subreddit = []
        for sub_name in sub_names:
            self.monitor_subreddit.append(self.reddit.subreddit(sub_name))


    def set_post_subreddit(self, sub_name: str="c_posts") -> None:
        """
        Sets the subreddit to post to instance to an instance of sub_name
        :param sub_name: name of the subreddit to be accessed
        """
        self.post_subreddit = self.reddit.subreddit(sub_name)


    def filter_submissions_manual(self, n_submissions: int, keywords: dict=KEYWORDS) -> [praw.models.Submission]:
        """
        Grabs n_submissions most recent submissions from subreddit and displays relevant ones containing KEYWORDS in title
        :param n_submissions: number of most recent submissions to retrieve, default
        :param keywords: dict of keywords to filter submissions by, default is const KEYWORDS
        :return: returns a list of praw.models.Submission objects
        """
        submissions = self.monitor_subreddit.new(limit=n_submissions)
        filtered_submissions = []
        for submission in submissions:
            if KEYWORDS[self.monitor_subreddit.display_name] == []:
                filtered_submissions.append(submission)
            else if [word for word in submission.title.lower().split() if word in KEYWORDS[self.monitor_subreddit.display_name]]:
                filtered_submissions.append(submission)
        return filtered_submissions


    def filter_submissions_auto(self, n_submissions: int=50, keywords: dict=KEYWORDS) -> [praw.models.Submission]:
        """
        Grabs n_submissions most recent submissions from subreddit and displays relevant ones containing KEYWORDS in title
        :param n_submissions: number of most recent submissions to retrieve, default
        :param keywords: dict of keywords to filter submissions by, default is const KEYWORDS
        :return: returns a list of praw.models.Submission objects
        """
        filtered_submissions = []
        for subreddit in self.monitor_subreddit:
            submissions = subreddit.new(limit=n_submissions)
            for submission in submissions:
                if KEYWORDS[self.monitor_subreddit.display_name] == []:
                    filtered_submissions.append(submission)
                else if [word for word in submission.title.lower().split() if word in KEYWORDS[subreddit.display_name]]:
                    filtered_submissions.append(submission)
        return filtered_submissions


    def post_submission(self, submission: praw.models.Submission) -> None:
        """
        Crossposts a submission to the post subreddit; sends replies to crosspost to original author
        :param submission: submission to crosspost
        """
        submission.crosspost(subreddit=self.post_subreddit.display_name, send_replies=True)
