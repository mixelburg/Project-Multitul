from colorama import init
from Util import status_codes, PRE_DELIMITER, MAIN_DELIMITER, POST_DELIMITER, GREEN, RESET, BLUE, RED, separator
from Util import get_choice, convert_to_json, get_num, get_screen_name
from vunerabilities.Feed import load_feed

try:
    from alive_progress import alive_bar
except:
    print("pip install alive-progress")
    exit()


def create_like_payload(glit_id, user_id, screen_name="default"):
    """
    Creates like request payload according to given params
    :param glit_id: ID of a glit
    :param user_id: ID of a user
    :param screen_name: User screen name
    :return: generated payload
    """
    # dictionary that will be converted to json
    data = {
        "glit_id": glit_id,
        "user_id": user_id,
        "user_screen_name": screen_name,
        "id": -1
    }
    return status_codes['like'] + PRE_DELIMITER + MAIN_DELIMITER + convert_to_json(data) + POST_DELIMITER


def send_like(sock, glit_id, user_id, screen_name="default"):
    """
    Sends like payload and gets answer from server
    :param sock: TCP socket
    :param glit_id: ID of a glit
    :param user_id: ID of a user
    :param screen_name: User screen name
    :return: answer from server
    """
    sock.send(create_like_payload(glit_id, user_id, screen_name).encode())
    return sock.recv(2048).decode()


def make_like(sock, num_likes, glit_id, user_id, screen_name):
    """
    Makes a number of likes
    :param sock: TCP socket
    :param num_likes: Number of likes
    :param glit_id: ID of a glit
    :param user_id: ID of a user
    :param screen_name: User screen name
    :return:
    """
    print(f"{BLUE}[+] Making likes to glit id: {glit_id}{RESET}")
    with alive_bar(num_likes, bar="classic2", spinner="classic") as bar:
        for i in range(num_likes):
            like_data = separator(send_like(sock, glit_id, user_id, screen_name))
            bar(f"{like_data[0]['id']}")
    init()


def like_id(sock, user_id):
    """
    Makes like by id
    :param sock: TCP socket
    :param user_id: ID of a user
    :return: None
    """
    num_likes = get_num("Enter number of likes: ")
    screen_name = get_screen_name()
    glit_id = get_num("Enter glit id: ")

    make_like(sock, num_likes, glit_id, user_id, screen_name)


def like_glit(sock, user_id):
    """
    Makes like by user id
    :param sock: TCP socket
    :param user_id: ID of a user
    :return: None
    """
    data = load_feed(sock, user_id)
    glit_num = get_num("Enter glit number: ", max_num=len(data[0]['glits']))
    glit_id = data[0]['glits'][glit_num - 1]['id']

    num_likes = get_num("Enter number of likes: ")
    screen_name = get_screen_name()

    make_like(sock, num_likes, glit_id, user_id, screen_name)


class LikeSwitcher(object):
    def numbers_to_action(self, sock, argument, user_id):
        """Dispatch method"""
        method_name = 'action_' + str(argument)

        def error(*args):
            print(f"{RED}[!] Option does not exist, try again{RESET}")
            return "error"

        # Get the method from 'self'. Default to lambda
        method = getattr(self, method_name, error)
        # Call the method as we return it
        return method(sock, user_id)

    # like functions
    @staticmethod
    def action_1(sock, user_id):
        like_glit(sock, user_id)

    @staticmethod
    def action_2(sock, user_id):
        like_id(sock, user_id)


def print_like_menu():
    """
    Prints like menu
    :return: None
    """
    print("""
    [1] make like by post
    [2] make like by id
    """)


def like(sock, user_id):
    """
    Makes likes
    :param sock: TCP socket
    :param user_id: ID of a user
    :return: None
    """
    switch = LikeSwitcher()
    print_like_menu()
    while switch.numbers_to_action(sock, get_choice(), user_id) == "error":
        print_like_menu()


