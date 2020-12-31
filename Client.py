# Import socket module
import socket
# from scapy.all import get_if_addr

# import to game
# windows
import msvcrt


# linux
# import sys
# import select
# import tty
# import termios

import time



def LookingForAServer(host):
    port = 13117

    # the message we suppose to get
    message = b'\xfe\xed\xbe\xef\x02'
    try:

        # UDP socket
        udpClient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        udpClient.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    except socket.error as e:
        print("Error creating socket: " + str(e))
        return False

    try:
        udpClient.bind(("", port))
    except socket.error as e:
        print("Error to bind: " + str(e))
        return False

    # mode of listening
    print("Client started, listening for offer requests...")

    try:
        # receive message from server
        data, addr = udpClient.recvfrom(1024)
    except socket.error as e:
        print("Error receiving data: " + str(e))
        return False

    # check if this is good message
    if data[0:4] != message[0:4] or len(data) == 0:
        print('Wrong message\n')
        return False
    else:
        tcpPort = int(hex(data[5])[2:] + hex(data[6])[2:], 16)
        print("Received offer from " + host + ", attempting to connect...\n")
        return tcpPort


def ConnectingToAServer(host, tcpPort):
    try:
        # TCP socket
        tcpClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e:
        print("Error creating socket: " + str(e))
        return False

    try:
        # connect to the server with the socket that sent in the message
        tcpClient.connect((host, tcpPort))
    except socket.error as e:
        print("Error to connect: " + str(e))
        return False

    try:
        # send the group name
        tcpClient.sendall(bytes('Bits Magnet\n', 'utf-8'))
    except socket.error as e:
        print("Error sending data: " + str(e))
        return False

    try:
        # receive message from server
        WelcomeData = tcpClient.recvfrom(1024)
    except socket.error as e:
        print("Error receiving data: " + str(e))
        return False

    if len(WelcomeData) == 0:
        print('The server does not respond')
        return False
    else:
        print(WelcomeData[0].decode("utf-8"))
        return tcpClient


def GameMode(tcpClient):
    # windows
    # timeout after 10 seconds
    start = time.time()
    while time.time() - start < 10:
        if msvcrt.kbhit():
            keyPress = msvcrt.getch()
            try:
                # send the key that pressed
                tcpClient.send(keyPress)
            except socket.error as e:
                print("Error sending data: " + str(e))
                return False
    # linux
    # def isData():
    #     return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])
    #
    # old_settings = termios.tcgetattr(sys.stdin)
    # try:
    #     tty.setcbreak(sys.stdin.fileno())
    #
    # timeout after 10 seconds
    # start = time.time()
    # while time.time() - start < 10:
    #
    #         if isData():
    #             c = sys.stdin.read(1)
    #             if c == '\x1b':  # x1b is ESC
    #                 break
    #
    # finally:
    #     termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

    try:
        # receive message from server
        GameOverData = tcpClient.recvfrom(1024)
    except socket.error as e:
        print("Error receiving data: " + str(e))
        return False
    if len(GameOverData) == 0:
        print('The server does not respond')
        return False
    print(GameOverData[0].decode("utf-8"))
    return True

def Main():
    host = '127.0.0.1'
    # host =  get_if_addr('eth1')

    while True:
        tcpPort = LookingForAServer(host)
        if tcpPort is False:
            continue
        tcpClient = ConnectingToAServer(host, tcpPort)
        if tcpClient is False:
            continue
        if GameMode(tcpClient) is False:
            continue
        tcpClient.close()

        print('Server disconnected, listening for offer requests...\n')
        print('*****************************************************\n')


if __name__ == '__main__':
    Main()