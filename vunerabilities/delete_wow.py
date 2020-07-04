try:
    from alive_progress import alive_bar
except:
    print("pip install alive-progress")
    exit()
from colorama import init

from Util import status_codes, fail_codes, get_num, separator, RESET, BLUE
from Util import PRE_DELIMITER, MAIN_DELIMITER, POST_DELIMITER


def create_wow_payload(wow_id):
    """
    Creates wow id payload
    :param wow_id: ID of a wow
    :return: generated payload
    """
    return status_codes['delete_wow'] + PRE_DELIMITER + MAIN_DELIMITER + str(wow_id) + POST_DELIMITER


def send_delete_wow_request(sock, wow_id):
    sock.send(create_wow_payload(wow_id).encode())
    return sock.recv(4096).decode()


def delete(sock, num_wows, wow_id):
    """
    Deletes a number of wows
    :param sock: TCP socket
    :param num_wows: Number of wows to delete
    :param wow_id: ID of a first wow t delete
    :return: None
    """
    with alive_bar(num_wows, bar="classic2", spinner="classic") as bar:
        for i in [(wow_id - i) for i in range(num_wows)]:
            wow_data = separator(send_delete_wow_request(sock, i))
            if wow_data[1] == fail_codes["wow_delete_fail"] or wow_data[0] == "error":
                bar(f"No WOW with id: {i}")
            else:
                bar(f"{wow_data[0]['id']}")
    init()


def delete_wow(sock):
    """
    Deletes wows
    :param sock: TCP socket
    :return: None
    """
    # get data from user
    wow_id = get_num("Enter first WOW id: ")
    num_wows = get_num("Enter number of WOWs to delete: ")

    delete(sock, num_wows, wow_id)