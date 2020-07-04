from colorama import init

from Util import status_codes, fail_codes, get_num, separator, RESET, BLUE
from Util import PRE_DELIMITER, MAIN_DELIMITER, POST_DELIMITER

try:
    from alive_progress import alive_bar
except:
    print("pip install alive-progress")
    exit()


def create_dislike_payload(like_id):
    """
    Creates dislike payload
    :param like_id: ID of a like
    :return: None
    """
    return status_codes['dislike'] + PRE_DELIMITER + MAIN_DELIMITER + str(like_id) + POST_DELIMITER


def send_dislike(sock, like_id):
    sock.send(create_dislike_payload(like_id).encode())
    return sock.recv(2048).decode()


def make_dislike(sock, like_id, num_dislikes):
    """
    Makes dislikes
    :param sock: TCP socket
    :param like_id: ID of a first like to delete
    :param num_dislikes: Number of likes to delete
    :return: None
    """
    with alive_bar(num_dislikes, bar="classic2", spinner="classic") as bar:
        for i in [(like_id - i) for i in range(num_dislikes)]:
            dislike_data = separator(send_dislike(sock, i))
            if dislike_data[1] == fail_codes['dislike_fail']:
                bar(f"No like with id: {i}")
            else:
                bar(f"{dislike_data[0]['id']}")
    init()


def dislike(sock):
    """
    Deletes likes
    :param sock: TCP socket
    :return: None
    """
    like_id = get_num("Enter like id: ")
    num_dislikes = get_num("Enter num of dislikes: ")

    print(f"{BLUE}[+] Making {num_dislikes} dislikes{RESET}")
    make_dislike(sock, like_id, num_dislikes)
