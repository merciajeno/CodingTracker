#to use rules and send notifications if delay in streaks
from scripts.github_service import get_commits
from scripts.leetcode_service import return_submissions
#here we need rules

def submit_streaks():
    return get_commits('merciajeno')

def submit_leetcode_commits():
    return return_submissions()