# Import socket module
import socket

# import to game
# windows
import msvcrt


# linux
# import sys
# import select
# import tty
# import termios

# def state1_looking_for_server():
# def state2_connecting_to_server():
# def state2_game_mode():
import time


def Main():
    host = '127.0.0.1'
    port = 13117

    # the message we suppose to get
    message = b'\xfe\xed\xbe\xef\x02'
    while True:

        # UDP socket
        udpClient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        udpClient.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        try:
            udpClient.bind(("", port))
        except socket.error as e:
            print(str(e))

        # mode of listening
        print("Client started, listening for offer requests...")

        # receive message from server
        data, addr = udpClient.recvfrom(1024)
        # check if this is good message
        if data[0:4] != message[0:4]:
            print('Wrong message')
            continue

        # connect to the server
        print("Received offer from " + host + ", attempting to connect...")

        # TCP socket
        tcpClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # connect to the server with the socket that sent in the message
        tcpClient.connect((host, int(hex(data[5])[2:]+hex(data[6])[2:], 16)))
        # send the group name
        tcpClient.sendall(bytes('Bits Magnet\n', 'utf-8'))

        # receive message from server
        WelcomeData = tcpClient.recvfrom(1024)
        print(WelcomeData[0].decode("utf-8"))


        # windows
        # timeout after 10 seconds
        start = time.time()
        while time.time() - start < 10:
            if msvcrt.kbhit():
                keyPress = msvcrt.getch()

                # send the key that pressed
                tcpClient.sendall(bytes(keyPress, 'utf-8'))

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

        # receive message from server
        GameOverData = tcpClient.recvfrom(1024)
        print(GameOverData[0].decode("utf-8"))

        tcpClient.fileno() == -1
        print('Server disconnected, listening for offer requests...')


if __name__ == '__main__':
    Main()