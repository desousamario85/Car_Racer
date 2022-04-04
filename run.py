
# Importing required modules into the project

import gspread
from google.oauth2.service_account import Credentials
import sys
from termcolor import colored, cprint

# Standard Google Drive Scope to access files in our google drive.

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

# Credentials to authenticate to the Leader_Board file

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('Leader_Board')

def get_leaderboard_data():
    """
    Getting leaderboard data to compare current user score.
    Add users to leaderboard and then display their position.
    """
    scorecard = SHEET.worksheet("scorecard").get_all_values()
    print(scorecard)

get_leaderboard_data()