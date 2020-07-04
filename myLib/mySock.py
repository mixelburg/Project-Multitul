import socket
from Util import GREEN, RED, RESET
import json

try:
    with open("Config.json") as config_file:
        data = json.load(config_file)
        SERVER_IP = data["SERVER_IP"]
        SERVER_PORT = data["SERVER_PORT"]
except FileNotFoundError:
    print("[!] Config file not found")
    exit()


def help():
    print("""This library was created by Ivan (mixelburg).
     It allows you to easily create server socket and client socket""")


def client():
    """
    Creates a client side socket for you
    :return: TCP socket
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(f"{GREEN}[+] Socket successfully created{RESET}")
    except socket.error as err:
        print(f"{RED}[!] socket creation failed with error %s{RESET}" % (err))
        exit()

    server_address = (SERVER_IP, SERVER_PORT)
    try:
     sock.connect(server_address)
    except ConnectionRefusedError:
        print(f"{RED}[!] Server refused the connection{RESET}")

    print(f"{GREEN}[+] Successfully connected\n{RESET}")

    return sock


def close(sock):
    """
    Closes tcp socket
    :param sock: TCP socket
    :return: None
    """
    try:
        sock.close()
        print(f"{GREEN}\n [+] Socket closed successfully{RESET}")
    except:
        print()

