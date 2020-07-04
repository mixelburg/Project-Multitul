from alive_progress import alive_bar
from colorama import init

from Util import status_codes, PRE_DELIMITER, MAIN_DELIMITER, POST_DELIMITER, GREEN, RESET, LGREEN, BLUE, RED, \
    get_choice, fail_codes
from Util import convert_to_json, get_num, separator, get_screen_name


def create_wow_payload(user_id, glit_id, user_screen_name):
    """
    Creates wow payload
    :param user_id: ID of a user
    :param glit_id: ID of a glit
    :param user_screen_name: Screen name of a user
    :return: generated payload
    """
    # data that will be converted to json
    data = {
        "glit_id": glit_id,
        "user_id": user_id,
        "user_screen_name": user_screen_name
    }
    return status_codes['publish_wow'] + PRE_DELIMITER + MAIN_DELIMITER + convert_to_json(data) + POST_DELIMITER


def send_wow_request(sock, user_id, glit_id, user_screen_name):
    sock.send(create_wow_payload(user_id, glit_id, user_screen_name).encode())
    return sock.recv(4096).decode()


def make_wow(sock, num_wows, user_id, glit_id, user_screen_name):
    """
    Makes wows
    :param sock: TCP socket
    :param num_wows: Number of wows to make
    :param user_id: ID of a user
    :param glit_id: ID of a glit
    :param user_screen_name: Screen name of a user
    :return: None
    """
    print(f"{BLUE}[+] Making wows to glit id: {glit_id}{RESET}")
    with alive_bar(num_wows, bar="classic2", spinner="classic") as bar:
        for i in range(num_wows):
            wow_data = separator(send_wow_request(sock, user_id, glit_id, user_screen_name))
            bar(f"{wow_data[0]['id']}")
    init()


def wow(sock, user_id):
    """
    Makes wows
    :param sock: TCP socket
    :param user_id: ID of a user
    :return: None
    """
    # get data from user
    glit_id = get_num("Enter glit id: ")
    user_screen_name = get_screen_name()
    num_wows = get_num("Enter number of wows: ")

    print(make_wow(sock, num_wows, user_id, glit_id, user_screen_name))
