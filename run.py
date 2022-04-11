
# Importing required modules into the project

import gspread
from google.oauth2.service_account import Credentials

# Allowing to display text in colour easier
from termcolor import colored, cprint

# Basic python function
import os,sys 
from sys import exit

# module needed to convert normal text to banner looking heading
import pyfiglet

# Used to get keystroke as input for race

import keyboard

# Used to calculate time taken to complete the race

import time
import curses
from curses import wrapper
import requests


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

def cls():
    """
    Clearing Screen to restart the Game or to begin the race.
    """
    os.system('cls' if os.name=='nt' else 'clear')

def get_leaderboard_data():
    """
    Getting leaderboard data to compare current user score.
    Add users to leaderboard and then display their position.
    """
    scorecard = SHEET.worksheet("scorecard").get_all_values()
    print(scorecard)


def typing_print(text):
    """
    Function provides the typing effect in the terminal
    when we wish to use the print command.
    """

    for character in text:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.05)
  
def typing_input(text):
    """
    Function provides the typing effect in the terminal.
    when we wish to use the input command.
    """
    for character in text:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.05)
    value = input()  
    return value


def main():
    """
    Starts the game function, requesting users name,
     calling other function to insert scores
    """

    ascii_banner = colored(pyfiglet.figlet_format(" Car Racer!!! ",font = "doom"),'white','on_green',attrs=['bold']) # Game banner with game is loaded
    print(ascii_banner)
    while True:
        try:
            username = input(colored("Please enter your name: ",'blue',attrs=['bold'])) # Players username
            if username and len(username) >= 3:
                typing_print(f'Hi {username} and welcome to Car Racer \n')
                break            
        except:            
            raise
        print(f'Name is either blank or too short. Please try again.')
    
    

    while True:
        try:
            # Checking with player if they want to start the game.
            start_game = input(colored('Are you ready to play? (Y/N) ','blue',attrs=['bold'])) 
            if start_game.lower() == 'y':
                print(f'\n {username}, get ready to race!! \n')                              
                player_car()
                random_text()                              
                break
            elif start_game.lower() == "n":
                end_game()
                break
        except:
            raise
        print(f'\nYou have enter "{start_game}" which is an invalid input. Please select Y or N')
     

 
def end_game():
    """
    Notification to the user that the game as ended or been chosen not to run.
    """
    print('Thank you for choosing Car Racer')

    while True:
            try:
                restart_game = input(colored('Do you want to restart the game? (Y/N) ','blue',attrs=['bold'])) # Checking with player if they want to start the game.
                if restart_game.lower() == 'y':
                    cls()
                    main()
                    break
                elif restart_game.lower() == "n":
                    print('We sad to see you go. Hope you enjoyed the game')
                    return False
                                              
            except:
                raise
            print(f'you have enter "{restart_game}" which is an invalid input. Please select Y or N')



def road_layout():
    """
    Building the road layout where the car with drive in
    """
    
def player_car():
    """
    Defining how the player car look.
    """    
    print(colored("   |O==O| ","red"))
    print(colored("   |     \\","red"))
    print(colored("   |     /","red"))
    print(colored("   |O==O| ","red"))

def random_text():# randomQuoteAPIURL = 'https://api.quotable.io/random'
    response = requests.get(url='https://api.quotable.io/random').json()
    # here everytime we get the new sentence with this API
    targetText = response["content"]

    return targetText   


main()
