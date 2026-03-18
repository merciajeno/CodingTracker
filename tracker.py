#to use rules and send notifications if delay in streaks
from github_service import get_commits
from leetcode_service import return_submissions
#here we need rules

def submit_streaks():
    return get_commits('merciajeno')

def submit_leetcode_commits():
    return return_submissions()