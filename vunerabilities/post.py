from Util import status_codes, PRE_DELIMITER, MAIN_DELIMITER, POST_DELIMITER, GREEN, RESET, LGREEN, BLUE, RED, \
    get_choice, fail_codes
from Util import convert_to_json, get_num, separator, get_screen_name
from vunerabilities.search import search


def create_post_payload(feed_owner_id, publisher_id, publisher_screen_name, publisher_avatar,
                        background_color, date, content, font_color):
    """
    Creates a post payload
    :param feed_owner_id: ID of a feed owner
    :param publisher_id: ID of a publisher
    :param publisher_screen_name: Publisher screen name
    :param publisher_avatar: Avatar of a publisher
    :param background_color: Background color
    :param date: Date
    :param content: Post content
    :param font_color: Font color
    :return: Generated payload
    """
    data = {
        "feed_owner_id": feed_owner_id,
        "publisher_id": publisher_id,
        "publisher_screen_name": publisher_screen_name,
        "publisher_avatar": publisher_avatar,
        "background_color": background_color,
        "date": date,
        "content": content,
        "font_color": font_color,
        "id": -1
    }
    return status_codes['publish_glit'] + PRE_DELIMITER + MAIN_DELIMITER + convert_to_json(data) + POST_DELIMITER


def send_post_request(sock, feed_owner_id, publisher_id, publisher_screen_name, publisher_avatar,
                      background_color, date, content, font_color):
    sock.send(create_post_payload(feed_owner_id, publisher_id, publisher_screen_name, publisher_avatar,
                                  background_color, date, content, font_color).encode())
    return sock.recv(4096).decode()


def get_post_info():
    """
    Gets post info from user
    :return: Tuple: data from user
    """
    return get_screen_name(), input("Enter avatar: "), input("Enter background color: "),\
           input("Enter date: "), input("Enter content: "), input("Enter font_color: ")


def print_glit_success(data):
    """
    Prints glit on success
    :param data: Data from server
    :return: None
    """
    print(f"""{LGREEN}
    [+] Glit published
    Info: 
    Feed owner id: {data[0]['feed_owner_id']}
    Publisher id: {data[0]['publisher_id']}
    Publisher screen name: {data[0]['publisher_screen_name']}
    Date: {data[0]['date']}
    Content: {data[0]['content']}
    Id: {data[0]['id']}
    {RESET}""")


def print_glit_error(data):
    """
    Prints data on error
    :param data: Data from server
    :return: None
    """
    print(f"{RED}[!] Failed to post glit, one or more parameters were incorrect{RESET}")


def print_glit(data):
    """
    Prints data on glit publish
    :param data: Data from server
    :return: None
    """
    if data[1] == fail_codes['glit_fail']:
        print_glit_error(data)
    else:
        print_glit_success(data)


def post_id(sock, user_id):
    """
    Makes post by id
    :param sock: TCP socket
    :param user_id: ID of a user
    :return: None
    """
    owner_id = get_num("Enter feed owner id: ")

    post_info = get_post_info()
    post_data = separator(send_post_request(sock, owner_id, user_id, post_info[0], post_info[1],
                                            post_info[2], post_info[3], post_info[4], post_info[5]))
    print_glit(post_data)


def post_name(sock, user_id):
    """
    Makes post by user screen name
    :param sock: TCP socket
    :param user_id: ID of a user
    :return: None
    """
    search_data = search(sock)

    if len(search_data[0]) == 1:
        print(f"{BLUE}[+] Posting Glit for {search_data[0][0]['screen_name']}{RESET}")

        post_info = get_post_info()
        print_glit(separator(send_post_request(sock, search_data[0][0]['id'], user_id, post_info[0],
                                               post_info[1], post_info[2], post_info[3], post_info[4],
                                               post_info[5])))
    else:
        user_num = get_num("Enter number of user: ", max_num=len(search_data[0]))
        print(f"{BLUE}[+] Posting Glit for {search_data[0][user_num - 1]['screen_name']}{RESET}")

        post_info = get_post_info()
        print_glit(separator(send_post_request(sock, search_data[0][user_num - 1]['id'], user_id, post_info[0],
                                               post_info[1], post_info[2], post_info[3], post_info[4],
                                               post_info[5])))


def print_post_menu():
    """
    Prints post menu
    :return: None
    """
    print("""
    [1] Create Glit by screen name
    [2] Create Glit by feed owner id
    """)


class PostSwitcher(object):
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

    # post functions
    @staticmethod
    def action_1(sock, user_id):
        post_name(sock, user_id)

    @staticmethod
    def action_2(sock, user_id):
        post_id(sock, user_id)


def post(sock, user_id):
    """
    Makes post
    :param sock: TCP socket
    :param user_id: ID of a user
    :return: None
    """
    switch = PostSwitcher()
    print_post_menu()

    while switch.numbers_to_action(sock, get_choice(), user_id) == "error":
        print_post_menu()