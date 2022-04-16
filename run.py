# pylint: disable=invalid-name, broad-except

"""Simple Python game to test the player typing skills."""

# Basic python function
import os
import sys

# Used to calculate time taken to complete the race
import time

# module needed to convert normal text to banner looking heading
import pyfiglet

# Used to send API calls.
import requests

# Google modules
import gspread
from google.oauth2.service_account import Credentials

# Allowing to display text in colour easier
from termcolor import colored

# Pandas for dataframe to sort leaderboard data
import pandas as pd
import numpy as np

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


def update_leaderboard(username, time_elapsed):
    """
    Inserting the players time into the google sheet.
    We limiting float to 2 decimals on the time score
    """
    format_float = "{:.2f}".format(time_elapsed)
    worksheet_to_update = SHEET.worksheet("scorecard")
    print("Updating scorecard...")
    data = [username, format_float]
    worksheet_to_update.append_row(data)
    return False


def get_leaderboard_data():
    """
    Getting leaderboard data to display top 10 players
    The records are obtained, then the Score column is converted in int
    There after the we are able to sort the scores. The index column
    is renamed and increase by to start from 1 and not 0
    """
    scorecard = SHEET.worksheet("scorecard").get_all_records()
    leaders = pd.DataFrame(scorecard)
    leaders_float = leaders.astype({'Score': 'float'})
    leaders_t10 = leaders_float.sort_values('Score', ascending=True).head(10)
    leaders_indexed = leaders_t10.reset_index(drop=True)
    leaders_indexed.index = np.arange(1, len(leaders_indexed) + 1)
    leaders_indexed.index.name = 'Rank'
    print(leaders_indexed)


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


def compare_text(source_text, position, successfully_entries,
                 start_time, retries, username):
    """
    Function checks to see if the entered text matches the random
    text received by the API (https://api.quotable.io/random').
    If they match they move on, if they don't match the retries
    count start. After 3 tries the game will restart
    """
    print(colored(source_text, 'yellow'))
    usertext = input()
    try:
        successfully_entries
    except NameError:
        successfully_entries = 0
    while True:
        try:
            if successfully_entries == 4:
                time_elapsed = time.time() - start_time
                cls()
                print(RACE_COMPLETE)
                time_float = "{:.2f}".format(time_elapsed)
                print(f'Well done. Your total time is {time_float} seconds')
                update_leaderboard(username, time_elapsed)
                end_game()
                break
            elif source_text == usertext and successfully_entries < 4:
                successfully_entries = successfully_entries + 1
                position += 18
                time_elapsed = time.time() - start_time
                time_float = "{:.2f}".format(time_elapsed)
                print(f'\n Current time lapse = {time_float} seconds')
                player_car(position)
                game_play(position, successfully_entries,
                          start_time, retries, username)
                break
            elif retries < 3:
                retries = retries + 1
                print(colored("Text did not match, please try again"
                              " with new text below", "white", "on_red"))
                game_play(position, successfully_entries, start_time,
                          retries, username)
                break
            else:
                typing_print("Sorry you have exceed the amount of tries. \n")
                typing_print("We hope you enjoyed the game. \n")
                typing_print("We will restart the game in just a moment \n")
                time.sleep(5.00)
                cls()
                main()
                break
        except NameError:
            print("Something went wrong. We are restarting the game")
            cls()
            main()


def main():
    """
    Starts the game function, requesting users name,
    calling other function to insert scores
    """
    # Game banner with game is loaded
    ascii_banner = colored(pyfiglet.figlet_format(" Car Racer ", font="doom"),
                           'white', 'on_green', attrs=['bold'])
    print(ascii_banner)
    while True:
        try:
            username = input(colored("Please enter your name: ",
                             'blue', attrs=['bold']))  # Players username
            if username and len(username.strip()) >= 3:
                typing_print(f'Hi {username} and Welcome to Car Racer')
                typing_print(GAME_INSTRUCTIONS)
                break
            else:
                print(colored("Name is either blank or too short."
                              "Please try again.", "white", "on_red"))
                continue
        except NameError:
            print("Name is either blank or too short. Please try again.")
            continue
    while True:
        try:
            option_selected = input(
                colored("\n1. Play Game \n2. View Leaderboard\n", "blue",
                        attrs=['bold']))
            if int(option_selected) == 1:
                start_game(username)
                break
            elif int(option_selected) == 2:
                get_leaderboard_data()
                continue
            else:
                print(colored(
                    f'\n You have enter ({option_selected}) which is an'
                    f' invalid input. Please select 1 or 2\n',
                    "white", "on_red"))
                continue
        except ValueError:
            print(colored(
                f'\nYou have enter ({option_selected}) which is an invalid'
                f' input. Please select 1 or 2\n', "white", "on_red"))
            continue
        return True


def game_play(position, successfully_entries,
              start_time, retries, username):
    """
    Here we are Displaying the random text obtained from the API
    The data is sent to the next function for comparison.
    """
    random_text = get_randomtext()
    compare_text(random_text, position,
                 successfully_entries, start_time, retries, username)


def start_game(username):
    """
    Checking to see if the player is ready to play and kicking off the game.
    """
    while True:
        try:
            # Checking with player if they want to start the game.
            start_game_option = input(colored('Are you ready to play? (Y/N) ',
                                      'blue', attrs=['bold']))
            if start_game_option.lower() == 'y':
                print(f'\n {username}, get ready to race!! \n')
                for i in range(3, 0, -1):
                    print(i)
                    time.sleep(1.00)
                print(colored("GO!!", "green"))
                position = 0  # setting starting point for the car
                start_time = time.time()
                player_car(position)
                retries = 0
                game_play(position, 0, start_time, retries, username)
                break
            elif start_game_option.lower() == "n":
                end_game()
                break
            else:
                print(colored(
                    f'\nYou have enter ({start_game_option}) which is an '
                    f'invalid input. Please select Y or N',
                    "white", "on_red"))
                continue
        except NameError():
            print(colored(
                f'\nYou have enter ({start_game_option}) which is an '
                f'invalid input. Please select Y or N',
                "white", "on_red"))


def end_game():
    """
    Notification to the user that the game as ended or been chosen not to run.
    """
    print('Thank you for choosing Car Racer')

    while True:
        try:
            # Checking with player if they want to start the game.
            restart_game = input(
                colored('Do you want to restart the game? (Y/N) ', 'blue',
                        attrs=['bold']))
            if restart_game.lower() == 'y':
                cls()
                main()
                break
            elif restart_game.lower() == "n":
                print('We sad to see you go. Hope you enjoyed the game')
                return False
            else:
                print(colored(
                    f'you have enter {restart_game} which is an invalid input.'
                    f' Please select Y or N',
                    "white", "on_red"))
        except NameError():
            print(colored(
                f'you have enter {restart_game} which is an invalid input.'
                f' Please select Y or N',
                "white", "on_red"))


GAME_INSTRUCTIONS = """

Test your typing skills by typing the random text appearing on the screen.
There are 5 rounds to get the car to the finish line
You have 3 retries in total through out the game,
then after the game will end and restart from the beginning

Good luck!!
"""


def player_car(position):
    """
    Defining how the player car look.
    """

    car = "|o==o>"
    finish = "||||"

    print(colored(f'{finish : >81}\n {car: >{position}}\n {finish : >80}',
                  'red'))


RACE_COMPLETE = """

⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⣄⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢀⡔⢺⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⣿⣿⡗⠢⡀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢷⣶⡟⠉⢻⣷⡀⠀⠀⠀⠀⠀⠀⠀⣾⡿⠉⢻⣶⡾⠁⠀⠀⠀⠀
⣠⣤⣴⠖⠒⠹⣿⣷⣀⣸⣿⣧⠀⠀⠀⠀⠀⠀⣸⣿⣇⣀⣾⣿⠏⠒⠲⣶⣤⣄
⢹⣿⣿⡄⠀⣀⡝⠁⠘⣿⣿⣿⡆⠀⠀⠀⠀⢠⣿⣿⣿⠏⠈⢻⣀⠀⢠⣿⣿⡏
⠀⢃⠀⠘⣿⣿⣿⣄⣠⡟⠉⢿⣿⡀⠀⠀⠀⣾⡿⠉⢹⣄⣀⣿⣿⣿⠃⠀⡸⠀
⠀⠈⣦⣴⣾⠉⠁⠈⣿⣷⠀⠈⣿⣷⠀⠀⣼⣿⠃⠀⣾⣿⠃⠈⠉⣹⣦⣴⠁⠀
⠀⠀⠸⣿⣿⡦⠤⠐⠋⠁⠀⠀⠸⣿⣇⢰⣿⡏⠀⠀⠈⠙⠂⠤⢴⣿⣿⠇⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿⣿⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⡿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀

"""


main()
