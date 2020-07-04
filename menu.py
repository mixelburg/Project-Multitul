from Util import RED, GREEN, RESET
from Util import login, logout, crack_password, get_choice
from getpass import getpass

from myLib.mySock import close
from vunerabilities.Feed import feed
from vunerabilities.Like import like
from vunerabilities.dislike import dislike
from vunerabilities.search import search
from vunerabilities.post import post
from vunerabilities.comment import comment
from vunerabilities.wow import wow
from vunerabilities.delete_wow import delete_wow
import json


EXIT_CHOICE = "0"


def get_credentials():
    """
    Gets credentials from user
    :return: user credentials
    """
    username = input("Enter username: ")
    while username == "":
        print(f"{RED}[!] Username mustn't be empty{RESET}")
        username = input("Enter username: ")

    password = getpass("Enter password: ")
    while password == "":
        print(f"{RED}[!] Password mustn't be empty{RESET}")
        password = getpass("Enter password: ")

    return username, password


def get_username():
    """
    Gets username from user
    :return:
    """
    username = input("Enter username to crack: ")
    while username == "":
        print(f"{RED}[!] Username mustn't be empty{RESET}")
        username = input("Enter username to crack: ")
    return username


def print_main_menu():
    """
    Prints main menu
    :return: None
    """
    print(f"""
    [0] Exit
    [1] Crack password
    [2] Login and go to secondary menu 
    """)


def print_second_menu():
    """
    Prints second menu
    :return: None
    """
    print(f"""
    [0] Logout and return to main menu
    [1] Make like
    [2] Make dislike
    [3] Make Glit
    [4] Make comment
    [5] Load feed
    [6] Search
    [7] Make WOW
    [8] Delete WOW
    """)


class SecondSwitcher(object):
    def numbers_to_action(self, sock, argument, user_id):
        """Dispatch method"""
        method_name = 'action_' + str(argument)

        # Get the method from 'self'. Default to lambda
        method = getattr(self, method_name, lambda *args: print(f"{RED}[!] Option does not exist, try again{RESET}"))
        # Call the method as we return it
        method(sock, user_id)

    # main options
    @staticmethod
    def action_0(sock, user_id):
        logout(sock, user_id)
        main_menu(sock)

    @staticmethod
    def action_1(sock, user_id):
        like(sock, user_id)

    @staticmethod
    def action_2(sock, user_id):
        dislike(sock)

    @staticmethod
    def action_3(sock, user_id):
        post(sock, user_id)

    @staticmethod
    def action_4(sock, user_id):
        comment(sock, user_id)

    @staticmethod
    def action_5(sock, user_id):
        feed(sock)

    @staticmethod
    def action_6(sock, user_id):
        search(sock)

    @staticmethod
    def action_7(sock, user_id):
        wow(sock, user_id)

    @staticmethod
    def action_8(sock, user_id):
        delete_wow(sock)


def second_menu(sock, user_id):
    """
    Driver function for second menu
    :param sock: TCP socket
    :param user_id: ID of user
    :return: None
    """
    while True:
        print_second_menu()
        choice = get_choice()

        switch = SecondSwitcher()
        switch.numbers_to_action(sock, choice, user_id)


class MainSwitcher(object):
    def numbers_to_action(self, sock, argument):
        """Dispatch method"""
        method_name = 'action_' + str(argument)

        # Get the method from 'self'. Default to lambda
        method = getattr(self, method_name, lambda *args: print(f"{RED}[!] Option does not exist, try again{RESET}"))
        # Call the method as we return it
        method(sock)

    # main menu functions
    @staticmethod
    def action_0(sock):
        close(sock)
        exit()

    @staticmethod
    def action_1(sock):
        crack_password(sock, get_username())

    @staticmethod
    def action_2(sock):
        user_id = login(sock, get_credentials())

        if user_id == "error":
            main_menu(sock)
        second_menu(sock, int(user_id))


def main_menu(sock):
    """
    Driver function for main function
    :param sock: TCP socket
    :return: None
    """
    while True:
        print_main_menu()
        choice = get_choice()

        switch = MainSwitcher()
        switch.numbers_to_action(sock, choice)


