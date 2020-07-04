from myLib.mySock import client, close
from menu import main_menu


def print_hello():
    """
    Prints some info about this program
    :return: None
    """
    print("""
                 _ _   _ _              _ 
                | | | (_) |            | |
 _ __ ___  _   _| | |_ _| |_ ___   ___ | |
| '_ ` _ \| | | | | __| | __/ _ \ / _ \| |
| | | | | | |_| | | |_| | || (_) | (_) | |
|_| |_| |_|\__,_|_|\__|_|\__\___/ \___/|_|
                                          
       created by: mixelburg                                   
    """)


def main():
    print_hello()
    sock = client()

    main_menu(sock)


if __name__ == '__main__':
    main()
