# import socket programming library
import socket
import time

# import thread module
import _thread


def udpBroadcast():
    host = '127.0.0.1'
    port = 13117

    # UDP socket
    udpSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udpSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    udpSock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    try:
        udpSock.bind((host, port))
    except socket.error as e:
        print(str(e))

    # mode of listening
    print("Server started, listening on IP address " + host)

    # Magic cookie (4 bytes): 0xfeedbeef. The message is rejected if it doesn’t start with this cookie
    # Message type (1 byte): 0x2 for offer. No other message types are supported
    # Server port (2 bytes): The port on the server that the client is supposed to connect to over TCP

    # our message to every client who is listening
    message = b'\xfe\xed\xbe\xef\x02\x13\x8D'

    # timeout after 10 seconds
    start = time.time()
    while time.time() - start < 10:
        # send broadcast one every second
        udpSock.sendto(message, ('<broadcast>', port))
        time.sleep(1)

def tcpConnection(tcpSocket, clients):
    # timeout after 10 seconds
    start = time.time()
    while time.time() - start < 10:
        # get client name
        clientConn, addr = tcpSocket.accept()
        data = clientConn.recv(1024)
        print(data.decode("utf-8"))
        # save the client in the dict
        clients[data.decode("utf-8")] = clientConn

def StartGame(clients):
    # timeout after 10 seconds
    start = time.time()
    while time.time() - start < 10:
        group1 = {}
        group2 = {}
        counter = 0
        welcome = 'Welcome to Keyboard Spamming Battle Royale.\nGroup1:\n==\n'

        for c in clients.keys():
            if counter % 2 == 0:
                group1[c] = 0
            else:
                group2[c] = 0
            counter += 1

        for g1 in group1.keys():
            welcome += g1
        welcome += 'Group2:\n'
        # for g2 in group2.keys():
        #     welcome += g2
        welcome += '\nStart pressing keys on your keyboard as fast as you can!!\n'

        for clientName, clientConn in clients.items():
            _thread.start_new_thread(GameMode, (group1, group2, clientConn, welcome,))
        time.sleep(10.2)

    GameOver = 'Game over!\n'
    GameOver += 'Group 1 typed in ' + str(sum(group1.values())) + ' characters. Group 2 typed in ' + str(sum(group2.values())) + ' characters.\n'
    if sum(group1.values()) > sum(group2.values()):
        GameOver += 'Group 1 wins!\n'
        GameOver += 'Congratulations to the winners:\n==\n'
        for g1 in group1.keys():
            GameOver += g1
    elif sum(group2.values()) > sum(group1.values()):
        GameOver += 'Group 2 wins!\n'
        GameOver += 'Congratulations to the winners:\n==\n'
        for g2 in group2.keys():
            GameOver += g2
    else:
        GameOver += 'It is a tie!\n'

    for clientConn in clients.values():
        clientConn.send(bytes(GameOver, 'utf-8'))

def GameMode(clientName, group1, group2, clientConn, welcome):
    clientConn.send(bytes(welcome, 'utf-8'))

    keyPress = clientConn.recv(1024)
    if clientName in group1.keys():
        group1[clientName] += 1

    if clientName in group2.keys():
        group2[clientName] += 1


def Main():
    clients = {}

    host = '127.0.0.1'
    port = 2060

    # TCP socket
    BUFFER_SIZE = 20  # Usually 1024, but we need quick response
    tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        tcpServer.bind((host, port))
    except socket.error as e:
        print(str(e))

    tcpServer.listen(20)

    while True:
        _thread.start_new_thread(udpBroadcast, ())
        _thread.start_new_thread(tcpConnection, (tcpServer, clients))
        time.sleep(10.2)
        StartGame(clients)
        tcpServer.close()
        print('Game over, sending out offer requests...')




if __name__ == '__main__':
    Main()
