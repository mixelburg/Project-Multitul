from Util import PRE_DELIMITER, MAIN_DELIMITER, POST_DELIMITER, GREEN, RESET, RED
from Util import status_codes
from Util import get_screen_name, separator


def create_search_payload(search_data):
    """
    Creates search payload
    :param search_data: Search data
    :return: generated payload
    """
    return status_codes['search'] + PRE_DELIMITER + MAIN_DELIMITER + '"' + search_data + '"' + POST_DELIMITER


def send_search_request(sock, search_data):
    sock.send(create_search_payload(search_data).encode())
    return sock.recv(8192).decode()


def print_data(data):
    """
    Prints search data
    :param data: Data from server
    :return: None
    """
    count = 1
    for user in data:
        print(f"""{GREEN}
        ***User {count} ***
        Name: {user['screen_name']}
        Description: {user['description']}
        Privacy: {user['privacy']}
        Id: {user['id']}{RESET}
        {RED}Mail: {user['mail']}{RESET}""")
        count += 1


def search(sock):
    """
    Searches users by name
    :param sock: TCP socket
    :return: None
    """
    screen_name = get_screen_name()

    search_data = separator(send_search_request(sock, screen_name))
    if len(search_data[0]) == 0:
        print(f"{RED}[!] No users found, try again{RESET}")
        search(sock)
    print_data(search_data[0])
    return search_data
