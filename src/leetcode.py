# Code borrowed from https://github.com/ufosc/UF-API-GROUP,
# Attributed to Chris Bloodsworth (me)

import requests
import leetcode_constants as LC
from bs4 import BeautifulSoup as bs

class User:
    name: str  # LC Username
    completed_total: int  # Total completed questions
    completed_list: list[int]  # Index 0,1,2 correspond to easy, med, hard
    rank: int  # User's rank. Based off of number of completed problems.
    recent: bool  # If the user has completed a problem in the last 24 hours
    recent_problem: str = ""  # The user's most recent problem, if it exists

    def getAttributes(self):
        """
        Returns attributes in easily readable string format.
        """
        recent_line = (
            f"\t Their most recent problem was {self.recent_problem}.\n" if self.recent else ""
        )
        return (
            f"**Username:** \t{self.name}\n"
            f"**Rank:** \t\t\t{self.rank}\n\n"
            f"This user is{' ' if self.recent else ' **_not_** '}active.\n"
            f"{recent_line}"
            f"\n**Number of completed problems:** ({self.completed_total})\n"
            f"\t_Easy:_ {self.completed_list[0]}\n"
            f"\t_Medium:_ {self.completed_list[1]}\n"
            f"\t_Hard:_ {self.completed_list[2]}\n"
        )

    def __str__(self):
        """
        Override for printing the object, just for clarity's sake
        """
        return self.getAttributes()


"""
Checks if the username provided is valid
"""
def checkUser(username: str) -> bool:
    r = requests.get("https://leetcode.com/" + username)
    return r.status_code != 404

def superRecentProblem(username: str):
    try: r = requests.get("https://leetcode.com/" + username)
    except requests.exceptions.InvalidURL: return -1
    html_doc = bs(r.content, "html.parser")

    raw_recent = html_doc.find("span", class_=LC.RECENT_DIV_CLASS).get_text()
    if "minute" in raw_recent:
        return html_doc.find("span", class_=LC.RECENT_PROBLEM_DIV_CLASS).get_text()

    return None

def leetcodeScrape(username: str) -> User:
    # Initialize user object
    user = User()

    # Get the user's LC URL
    user.name = username

    # Get Raw HTML
    try:
        r = requests.get("https://leetcode.com/" + user.name)
    except requests.exceptions.InvalidURL:
        print("Error [leetcodeScrape]: Invalid username")
        return user

    html_doc = bs(r.content, "html.parser")

    # Gets raw divs for user's number of completed problems by difficulty
    raw_completed = html_doc.find_all("span", class_=LC.DIFF_DIV_CLASS)

    # Translates those divs into usable numbers
    user.completed_list = [int(r.get_text()) for r in raw_completed]
    user.completed_total = sum(user.completed_list)

    # Get raw rank
    raw_rank = html_doc.find("span", class_=LC.RANK_DIV_CLASS).get_text()

    # Remove commas, assign rank
    user.rank = int(raw_rank.replace(",", ""))

    # Get the most recent problem, if any
    raw_recent = html_doc.find("span", class_=LC.RECENT_DIV_CLASS).get_text()

    # If submitted recently (LC uses the format "23 hours ago")
    for k in ["minute", "hour", "day "]:
        if k in raw_recent:
            user.recent = True
            break
    else: user.recent = False

    if user.recent:
        user.recent_problem = html_doc.find("span", class_=LC.RECENT_PROBLEM_DIV_CLASS).get_text()

    # Prints user data
    return user
