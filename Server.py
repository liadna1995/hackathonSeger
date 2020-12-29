
#
# def Main():
#     host = ""
#     portUDP = 5005
#
#     # UDP
#     ServerSideSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     ServerSideSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#     ServerSideSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
#
#     try:
#         ServerSideSocket.bind((host, portUDP))
#     except socket.error as e:
#         print(str(e))
#
#     # timeout for 10 seconds
#     ServerSideSocket.settimeout(10)
#     # mode of listening
#     print("Server started, listening on IP address " + host)
#     # our message is "offer" to every client who is listening
#     message = b"offer"
#
#     # TCP
#     TCP_PORT = 2004
#     BUFFER_SIZE = 20  # Usually 1024, but we need quick response
#
#     tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#     tcpServer.bind((host, TCP_PORT))
#     threads = []
#
#     # put the socket into listening mode
#     tcpServer.listen(5)
#
#     # a forever loop until client wants to exit
#     while True:
#         ServerSideSocket.sendto(message, ('255.255.255.255', 13117))
#         time.sleep(1)
#
#         # establish connection with client
#         c, addr = tcpServer.accept()
#
#         # lock acquired by client
#         print_lock.acquire()
#         print('Connected to :', addr[0], ':', addr[1])
#
#         # Start a new thread and return its identifier
#         start_new_thread(threaded, (c,))
#     s.close()

# import socket programming library
import socket
import time
# import thread module
import threading
import _thread

print_lock = threading.Lock()


# def udp_offer():

# thread function
def threaded(c):
    while True:

        # data received from client
        data = c.recv(1024)
        if not data:
            print('Bye')

            # lock released on exit
            print_lock.release()
            break

        # reverse the given string from client
        data = data[::-1]

        # send back reversed string to client
        c.send(data)

        # connection closed
    c.close()


# def Main():
#     host = ""
#
#     # reverse a port on your computer
#     # in our case it is 12345 but it
#     # can be anything
#     port = 12345
#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     s.bind((host, port))
#     print("socket binded to port", port)
#
#     # put the socket into listening mode
#     s.listen(5)
#     print("​Server started, listening on IP address")
#
#     # a forever loop until client wants to exit
#     while True:
#         # establish connection with client
#         c, addr = s.accept()
#
#         # lock acquired by client
#         print_lock.acquire()
#         print('Connected to :', addr[0], ':', addr[1])
#
#         # Start a new thread and return its identifier
#         start_new_thread(threaded, (c,))
#     s.close()

def startBroadcast():
    try:
        ip = '127.0.0.1'
        port = 13117
        # UDP
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.bind((ip, port))

        # mode of listening
        print("Server started, listening on IP address " + ip)
        # our message is "offer" to every client who is listening
        message = b'\xfe\xed\xbe\xef\x02\x13\x8D'
        # timeout for 10 seconds
        for i in range(10):
            sock.sendto(message, ('<broadcast>', 13117))
            time.sleep(1)
    except:
        print("bla")

def TCPconnection(socketTCP, groups):
    timeout = time.time() + 10  # 10 seconds from now
    while True:
        if time.time() >= timeout:
            break
        conn, addr = socketTCP.accept()
        data = conn.recv(1024)
        print(data.decode("utf-8"))
        groups[data.decode("utf-8")] = conn

def StartGeme(groups):
    group1 = []
    group2 = []



def Main():
    groups = {}

    # TCP
    ip = '127.0.0.1'
    TCP_PORT = 5005
    BUFFER_SIZE = 20  # Usually 1024, but we need quick response
    tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpServer.bind((ip, TCP_PORT))
    tcpServer.listen(20)

    while True:
        _thread.start_new_thread(startBroadcast, ())
        _thread.start_new_thread(TCPconnection, (tcpServer, groups))
        time.sleep(10.2)

if __name__ == '__main__':
    Main()
