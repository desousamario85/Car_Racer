
# Importing required modules into the project

import gspread
from google.oauth2.service_account import Credentials

# Allowing to display text in colour easier
from termcolor import colored, cprint

# Basic python function
import os
import sys
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
    os.system('cls' if os.name == 'nt' else 'clear')


def get_leaderboard_data():
    """
    Getting leaderboard data to compare current user score.
    Add users to leaderboard and then display their position.
    """
    scorecard = SHEET.worksheet("scorecard").get_all_values()
    print(scorecard)


def get_randomtext():
    """
    Retrieving random text from 'https://api.quotable.io/random'.
    This will be text text that the user needs to match.
    """

    response = requests.get(url='https://api.quotable.io/random').json()
    targetText = response["content"]
    return targetText


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


def compare_text(sourcetext ,position ,finishline ,x ,startTime , retries):
    print(colored(sourcetext,'yellow'))
    usertext = input()    
    try:x
    except NameError:x = 0

    while True:
        try:
            if sourcetext == usertext and  x < 4:
                x = x + 1                              
                position += 15                   
                timeElapsed = time.time() - startTime
                print(f'Current time lapse = {timeElapsed} seconds')                                      
                player_car(position ,finishline)
                game_play(position ,finishline ,x ,startTime )
            elif x == 4:
                cls()
                print(racecomplete)
                break                                    
        except:
            raise
        if retries < 3:
            retries = retries + 1
            print(colored(f'Text did not match, try again','white', 'on_red'))
            game_play(position ,finishline ,x ,startTime,retries)          

            break
        else:
            typing_print("Sorry you have exceed the amount of tries")            
            typing_print("We hope you enjoyed the game.")
            typing_print("We are restarting the game")
            time.sleep(5.00)
            cls()
            main()


def main():
    """
    Starts the game function, requesting users name,
     calling other function to insert scores
    """

    ascii_banner = colored(pyfiglet.figlet_format(" Car Racer!!! ", font="doom"),
                           'white', 'on_green', attrs=['bold'])  # Game banner with game is loaded
    print(ascii_banner)
    while True:
        try:
            username = input(colored("Please enter your name: ",
                             'blue', attrs=['bold']))  # Players username
            if username and len(username) >= 3:
                typing_print(f'Hi {username} and welcome to Car Racer \n')
                break
        except:
            raise
        print(f'Name is either blank or too short. Please try again.')

    while True:
        try:
            # Checking with player if they want to start the game.
            start_game = input(
                colored('Are you ready to play? (Y/N) ', 'blue', attrs=['bold']))
            if start_game.lower() == 'y':
                print(f'\n {username}, get ready to race!! \n')
                position = 0  # setting starting point for the car
                finishline = 74  # setting position of the middle finish line
                startTime = time.time()
                player_car(position, finishline)
                retries = 0  
                game_play(position ,finishline ,0 ,startTime , retries)

                break
            elif start_game.lower() == "n":
                end_game()
                break
        except:
            raise
        print(
            f'\nYou have enter "{start_game}" which is an invalid input. Please select Y or N')

def game_play(position ,finishline ,x ,startTime , retries):    
    random_text = get_randomtext()
    compare_text(random_text ,position ,finishline , x, startTime ,retries)



def end_game():
    """
    Notification to the user that the game as ended or been chosen not to run.
    """
    print('Thank you for choosing Car Racer')

    while True:
        try:
            # Checking with player if they want to start the game.
            restart_game = input(
                colored('Do you want to restart the game? (Y/N) ', 'blue', attrs=['bold']))
            if restart_game.lower() == 'y':
                cls()
                main()
                break
            elif restart_game.lower() == "n":
                print('We sad to see you go. Hope you enjoyed the game')
                return False

        except:
            raise
        print(
            f'you have enter "{restart_game}" which is an invalid input. Please select Y or N')


def game_instructions():
    """
    Explaination on the game rules and how to play the game

    """
    typing_print("Test your typing skills by typing out the random text that appears on the screen")

def player_car(position, finishline):
    """
    Defining how the player car look.
    """

    car = "|o==o>"
    finish = "||||"

    print(colored(f'{finish : >81}\n {car: >{position}}\n {finish : >80}', 'red'))

racecomplete = """
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⣿⣿⠋⠐⢢⣤⡀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⠁⢀⣿⣷⡦⠾⣿⣿⠗⢄⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣶⠶⠤⣤⣴⣿⡿⠋⠛⣿⡁⠀⢨⣯⡀⠈⣧⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⣿⣶⣴⠟⠁⣩⣷⣤⣴⣿⣿⡶⢿⣿⡷⢾⣿⣧⡀
⠀⠀⠀⠀⠀⠀⠀⢠⣾⣿⠛⠻⣿⣿⣷⠖⠻⣿⠋⠀⢙⣏⠀⠀⣻⠀⠀⢹⠋⣣
⠀⠀⠀⠀⠀⠀⡠⠛⢻⣧⡤⠊⢉⣽⣧⣄⣴⣿⣷⡤⣿⣿⣷⢼⣿⣷⢴⣿⡶⠁
⠀⠀⠀⠀⢀⣬⣄⣠⣾⣇⢈⣽⣿⣿⡿⠁⠀⢙⣏⠀⠈⣻⡁⠀⢹⡃⠈⡟⠀⠀
⠀⠀⠀⣰⣿⣿⡟⠀⠀⣽⣿⣿⠟⠉⢻⠶⣤⣾⣿⣷⢴⣿⣷⣤⣿⣧⠌⠀⠀⠀
⠀⣠⣂⣀⣠⣾⣿⡿⠚⠿⡿⠉⢑⣤⣾⣧⣨⣿⣿⠃⠀⠹⠟⠈⢿⠃⠀⠀⠀⠀
⠈⠉⠀⠀⠀⠉⠙⠳⢄⣴⣿⡦⣾⣿⣿⠋⣹⠋⠉⢢⢠⣾⣧⡰⠁⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⡁⠀⣽⣿⠜⠁⠀⠀⡜⣿⣿⠟⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠚⠛⠋⠀⠀⠀⡸⣻⠿⠋⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠜⡵⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⢊⡞⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡰⣡⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠜⡴⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣾⠞⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢀⣼⡿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢠⣾⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣰⣿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢀⣼⡿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢾⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀"""

main()

