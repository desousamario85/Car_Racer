# Importing required modules into the project

import gspread
from google.oauth2.service_account import Credentials

# Allowing to display text in colour easier
from termcolor import colored

#Pandas for dataframe to sort leaderboard data
import pandas as pd
import numpy as np

# Basic python function
import os
import sys

# module needed to convert normal text to banner looking heading
import pyfiglet

# Used to calculate time taken to complete the race
import time
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


def update_leaderboard(username, time_elapsed):
    """
    Inserting the players time into the google sheet.
    """
    format_float = "{:.2f}".format(time_elapsed) #limiting float to 2 decimals
    worksheet_to_update = SHEET.worksheet("scorecard")
    print("Updating scorecard...")
    data = [username, format_float]
    worksheet_to_update.append_row(data)


def get_leaderboard_data():
    """
    Getting leaderboard data to display top 10 players
    """
    scorecard = SHEET.worksheet("scorecard").get_all_records()
    df = pd.DataFrame(scorecard)
    df_converted_col = df.astype({'Score':'float'})
    df_top_10 = df_converted_col.sort_values('Score',ascending=False).head(10)
    df_indexed = df_top_10.reset_index(drop=True)
    df_indexed.index = np.arange(1, len(df_indexed) + 1)
    df_indexed.index.name = 'Rank'
    print(df_indexed)


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
                 start_time, retries):

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
            if source_text == usertext and successfully_entries < 4:
                successfully_entries = successfully_entries + 1
                position += 15
                time_elapsed = time.time() - start_time
                print(f'Current time lapse = {time_elapsed} seconds')
                player_car(position)
                game_play(position, successfully_entries,
                          start_time, retries)
            elif successfully_entries == 4:
                time_elapsed = time.time() - start_time
                cls()
                print(RACE_COMPLETE)
                print(f'Well done. Your total time is {time_elapsed}')
                update_leaderboard(username, time_elapsed)
                end_game()
                break
        except ValueError():
            raise
        if retries < 2:
            retries = retries + 1
            print(colored("Text did not match, try again", "white", "on_red"))
            game_play(position, successfully_entries, start_time,
                      retries)

            break
        else:
            typing_print("Sorry you have exceed the amount of tries. \n")
            typing_print("We hope you enjoyed the game. \n")
            typing_print("We are restarting the game \n")
            time.sleep(5.00)
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
    typing_print(GAME_INSTRUCTIONS)
    global username
    while True:
        try:
            username = input(colored("Please enter your name: ",
                             'blue', attrs=['bold']))  # Players username
            if username and len(username) >= 3:
                typing_print(f'Hi {username} and welcome to Car Racer \n')
            break
        except:
            raise
        print("Name is either blank or too short. Please try again.")
    while True:
            try:
                option_selected = input(colored("\n1. Play Game \n2. View Leaderboard\n"
                                        , "blue",attrs=['bold']))
                if int(option_selected) == 1:
                    start_game()
                    break
                elif int(option_selected) == 2:
                    get_leaderboard_data()
                    continue
                else:
                    print(colored(
                    f'\nYou have enter ({option_selected}) which is an invalid input.'
                    f' Please select 1 or 2\n',"white","on_red"))
                    continue
            except ValueError:
                print(colored(
                    f'\nYou have enter ({option_selected}) which is an invalid input.'
                    f' Please select 1 or 2\n',"white","on_red"))
                continue
            return True


def game_play(position, successfully_entries,
              start_time, retries):
    """
    Here we are Displaying the random text obtained from the API
    The data is sent to the next function for comparison.
    """
    random_text = get_randomtext()
    compare_text(random_text, position,
                 successfully_entries, start_time, retries)


def start_game():
    """
    Checking to see if the player is ready to play and kicking off the game.
    """
    while True:
        try:
        # Checking with player if they want to start the game.
            start_game = input(colored('Are you ready to play? (Y/N) ',
                               'blue', attrs=['bold']))
            if start_game.lower() == 'y':
                print(f'\n {username}, get ready to race!! \n')
                for i in range(3, 0, -1):
                    print(i)
                    time.sleep(1.00)
                    print(colored("GO!!", "green"))
                    position = 0  # setting starting point for the car
                    start_time = time.time()
                    player_car(position)
                    retries = 0
                    game_play(position, 0, start_time, retries)
                    break
            elif start_game.lower() == "n":
                end_game()
                break
        except:
            raise
        print(
              f'\nYou have enter ({start_game}) which is an invalid input.'
              f' Please select Y or N')




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
        except:
            raise
        print(f'you have enter {restart_game} which is an invalid input.'
              f' Please select Y or N')


GAME_INSTRUCTIONS = """
Welcome to Car Racer

Test your typing skills by typing the random text appearing on the screen.
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
