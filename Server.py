# import socket programming library
import socket
import time

# import thread module
import _thread
# from scapy.all import get_if_addr

def udpBroadcast(host):
    port = 13117

    try:
        # UDP socket
        udpSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udpSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        udpSock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    # Error creating socket
    except socket.error:
        return False

    try:
        udpSock.bind((host, port))
    # Error to bind
    except socket.error:
        return False

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
        try:
            udpSock.sendto(message, ('<broadcast>', port))
        # Error sending data
        except socket.error:
            return False
        time.sleep(1)

def tcpConnection(tcpSocket, clients):
    # timeout after 10 seconds
    start = time.time()
    while time.time() - start < 10:
        try:
            # get client name
            clientConn, addr = tcpSocket.accept()
            data = clientConn.recv(1024)
        # Error receiving data
        except socket.error:
            print("Client disconnected")
            return False
        if len(data) == 0:
            return False
        else:
            # save the client in the dict ({client name: client socket})
            clients[data.decode("utf-8")] = clientConn
            return True

def WaitingForClients(host, tcpServer, clients):
    if _thread.start_new_thread(udpBroadcast, (host,)) is False:
        return False
    if _thread.start_new_thread(tcpConnection, (tcpServer, clients)) is False:
        return False
    time.sleep(10.2)
    return True

def GameMode(clients, characters, GamesHistory):
    if len(clients) == 0:
        print('There are no clients that connected...')
        return False
    # group dict = {client name : points}
    group1 = {}
    group2 = {}
    counter = 0

    # building the welcome message
    welcome = '*******************************************\n'
    welcome += 'Welcome to Keyboard Spamming Battle Royale.\n\nGroup1:\n==\n'

    # randomly division into groups
    for c in clients.keys():
        GamesHistory[c] = 0
        if counter % 2 == 0:
            group1[c] = 0
        else:
            group2[c] = 0
        counter += 1

    if len(group1) != 0:
        for g1 in group1.keys():
            welcome += g1
    welcome += '\nGroup2:\n==\n'
    if len(group2) != 0:
        for g2 in group2.keys():
            welcome += g2
    else:
        welcome += 'There no players in Group 2, you play alone!\n'
    welcome += '*******************************************\n'
    welcome += '\nStart pressing keys on your keyboard as fast as you can!!\n'


    # the game is starting
    for clientName, clientConn in clients.items():
        _thread.start_new_thread(StartPressing, (clientName, group1, group2, clientConn, welcome, characters, GamesHistory, ))
    time.sleep(10.2)

    # building the game over message
    GameOver = '*******************************************\n'
    GameOver += '\nGame over!\n'
    GameOver += 'Group 1 typed in ' + str(sum(group1.values())) + ' characters.\nGroup 2 typed in ' + str(sum(group2.values())) + ' characters.\n'
    if sum(group1.values()) > sum(group2.values()):
        GameOver += '\n************** Group 1 wins! **************\n'
        GameOver += '*******************************************\n'
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
    GameOver += '*******************************************\n'

    # calculate statistics
    if len(characters) != 0 or len(GamesHistory) != 0:
        GameOver += '\nStatistics:\n'
    if len(characters) != 0:
        max_value = max(characters.values())  # maximum value
        max_keys = [k for k, v in characters.items() if v == max_value]  # getting all keys containing the `maximum`

        GameOver += 'Most commonly typed character:\n'
        for m in max_keys:
            GameOver += m + '\n'

    if len(GamesHistory) != 0:
        max_value = max(GamesHistory.values())  # maximum value
        max_keys = [k for k, v in GamesHistory.items() if v == max_value]  # getting all keys containing the `maximum`

        GameOver += '\nBest team ever to play:\n'
        for m in max_keys:
            GameOver += m + '\n'
        GameOver += '*******************************************\n'

    # sending the game over all the clients
    for clientConn in clients.values():
        try:
            clientConn.sendall(bytes(GameOver, 'utf-8'))
        # Error sending data
        except socket.error:
            print("Client disconnected")

def StartPressing(clientName, group1, group2, clientConn, welcome, characters, GamesHistory):
    try:
        clientConn.sendall(bytes(welcome, 'utf-8'))
    # Error sending data
    except socket.error:
        print("Client disconnected")
    # timeout after 10 seconds
    start = time.time()
    while time.time() - start < 10:
        try:
            keyPress = clientConn.recv(1024)
        # Error receiving data
        except socket.error:
            print("Client disconnected")
        if len(keyPress) != 0:
            char = keyPress.decode("utf-8")
            if char not in characters:
                characters[char] = 1
            else:
                characters[char] += 1

            if clientName in group1.keys():
                group1[clientName] += 1
                GamesHistory[clientName] += 1

            if clientName in group2.keys():
                group2[clientName] += 1
                GamesHistory[clientName] += 1

def Main():
    clients = {}
    characters = {}
    GamesHistory = {}

    host = '127.0.0.1'
    # host =  get_if_addr('eth1')
    port = 5005

    while True:
        openSocket = True
        while openSocket:
            try:
                # TCP socket
                tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Error creating socket
            except socket.error:
                continue

            try:
                tcpServer.bind((host, port))
                tcpServer.listen(20)
            # Error to bind
            except socket.error:
                continue
            openSocket = False

        if WaitingForClients(host, tcpServer, clients) is False:
            continue
        GameMode(clients, characters, GamesHistory)
        print('Game over, sending out offer requests...\n')
        print('*******************************************\n')

        # close the connection
        try:
            tcpServer.recv(1024)
        except socket.error:
            tcpServer.close()
        clients.clear()

if __name__ == '__main__':
    Main()
