from Util import status_codes, PRE_DELIMITER, MAIN_DELIMITER, POST_DELIMITER, GREEN, RESET, LGREEN, BLUE, RED, \
    get_choice
from Util import convert_to_json, get_num, separator
from vunerabilities.search import search


def create_feed_payload(user_id, glit_count):
    """
    Created feed load payload
    :param user_id: ID of a user
    :param glit_count: Number of glits to load
    :return: Generated payload
    """
    # data that will be converted to json
    data = {
        "feed_owner_id": user_id,
        "end_date": "2021-06-25T05:34:04.000Z",
        "glit_count": glit_count
    }
    return status_codes['load_feed'] + PRE_DELIMITER + MAIN_DELIMITER + convert_to_json(data) + POST_DELIMITER


def send_feed_request(sock, user_id, glit_count):
    sock.send(create_feed_payload(user_id, glit_count).encode())
    return sock.recv(10000).decode()


def print_feed(data):
    """
    Prints loaded feed
    :param data: Data from server
    :return: None
    """
    print(f"{GREEN}[+] {data[2]}{RESET}")

    count = 1
    for glit in data[0]['glits']:
        print(f"""{LGREEN}
        ****Glit - {count}****
        Publisher id: {glit['publisher_id']}
        Publisher screen name: {glit['publisher_screen_name']}
        Content: {glit['content']}
        Id: {glit['id']}
        Date: {glit['date']}
        {RESET}""")
        count += 1


def load_feed(sock, user_id):
    """
    Loads feed
    :param sock: TCP socket
    :param user_id: ID of a user
    :return: Data from server
    """
    glit_count = get_num("Enter number of glits to load: ")
    print(f"{BLUE}[+] Loading feeds for user id: {user_id}{RESET}")
    data = send_feed_request(sock, user_id, glit_count)
    data = separator(data)
    print_feed(data)

    return data


def print_feed_menu():
    """
    Prints feed menu
    :return: None
    """
    print("""
    [1] Load feed by screen name
    [2] Load feed by id
    """)


def feed_id(sock):
    """
    Loads feed by id
    :param sock: TCP socket
    :return:
    """
    # get user id
    user_id = get_num("Enter user id: ")

    load_feed(sock, user_id)


def feed_name(sock):
    """
    Loads feed by user screen name
    :param sock: TCP socket
    :return: None
    """
    search_data = search(sock)
    if len(search_data[0]) == 1:
        print(f"{BLUE}[+] Loading feed for {search_data[0][0]['screen_name']}{RESET}")
        load_feed(sock, search_data[0][0]['id'])
    else:
        user_num = get_num("Enter number of user to load: ", max_num=len(search_data[0]))
        print(f"{BLUE}[+] Loading feed for {search_data[0][user_num - 1]['screen_name']}{RESET}")
        load_feed(sock, search_data[0][user_num - 1]['id'])


class FeedSwitcher(object):
    def numbers_to_action(self, sock, argument):
        """Dispatch method"""
        method_name = 'action_' + str(argument)

        def error(*args):
            print(f"{RED}[!] Option does not exist, try again{RESET}")
            return "error"

        # Get the method from 'self'. Default to lambda
        method = getattr(self, method_name, error)
        # Call the method as we return it
        return method(sock)

    # feed functions
    @staticmethod
    def action_1(sock):
        feed_name(sock)

    @staticmethod
    def action_2(sock):
        feed_id(sock)


def feed(sock):
    """
    Loads feed
    :param sock: TCP socket
    :return: None
    """
    switch = FeedSwitcher()
    print_feed_menu()

    while switch.numbers_to_action(sock, get_choice()) == "error":
        print_feed_menu()
