
# Importing required modules into the project

import gspread
from google.oauth2.service_account import Credentials
import sys
from termcolor import colored, cprint
import time,os,sys

import pyfiglet

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


def typingPrint(text):
  for character in text:
    sys.stdout.write(character)
    sys.stdout.flush()
    time.sleep(0.05)
  
def typingInput(text):
  for character in text:
    sys.stdout.write(character)
    sys.stdout.flush()
    time.sleep(0.05)
  value = input()  
  return value


def main():
    """
    Starts the game function, requesting users name, calling other function to insert scores
    """
    ascii_banner = pyfiglet.figlet_format("Car Racer!!!",font = "slant")
    print(ascii_banner)
    username = input(colored("Please enter your name: ",'blue',attrs=['bold']))
    typingPrint(f'Welcome {username}. \n')
    start_game = input(colored('Are you ready to play? ','blue',attrs=['bold']))




main()
