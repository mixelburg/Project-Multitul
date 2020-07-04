from Util import status_codes, PRE_DELIMITER, MAIN_DELIMITER, POST_DELIMITER, GREEN, RESET, LGREEN, BLUE, RED, \
    get_choice, fail_codes
from Util import convert_to_json, get_num, separator, get_screen_name


def create_comment_payload(glit_id, user_id, user_screen_name, content, date):
    """
    Creates comment payload
    :param glit_id: ID of a glit
    :param user_id: ID of a user
    :param user_screen_name: Screen name of user
    :param content: Content for comment
    :param date: Date
    :return: generated payload
    """
    # dictionary that will be converted to json
    data = {
        "glit_id": glit_id,
        "user_id": user_id,
        "user_screen_name": user_screen_name,
        "id": -1,
        "content": content,
        "date": date
    }
    return status_codes['publish_comment'] + PRE_DELIMITER + MAIN_DELIMITER + convert_to_json(data) + POST_DELIMITER


def send_comment_payload(sock, glit_id, user_id, user_screen_name, content, date):
    sock.send(create_comment_payload(glit_id, user_id, user_screen_name, content, date).encode())
    return sock.recv(4096).decode()


def print_comment(data):
    """
    Prints posted comment
    :param data: data from server
    :return: None
    """
    if data[1] == fail_codes['comment_fail']:
        print(f"{RED}[!] Comment publish failed{RESET}")
    else:
        print(f"""{GREEN}
        [+] Comment published
        Glit id: {data[0]['glit_id']}
        User id: {data[0]['user_id']}
        User screen name: {data[0]['user_screen_name']}
        Content: {data[0]['content']}
        Id: {data[0]['id']}
        Date: {data[0]['date']}
        {RESET}""") 


def comment(sock, user_id):
    """
    Posts a comment
    :param sock: TCP socket
    :param user_id: ID of a user
    :return: None
    """
    # get data from user
    glit_id = get_num("Enter glit id: ")
    user_screen_name = get_screen_name()
    content = input("Enter content: ")
    date = input("Enter date: ")

    print_comment(separator(send_comment_payload(sock, glit_id, user_id, user_screen_name, content, date)))
