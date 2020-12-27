# import socket programming library
import socket
import time
# import thread module
from _thread import *
import threading

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
def Main():
    try:
        ip = '127.0.0.1'
        port = 5005
        #UDP
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.bind((ip, port))
        # timeout for 10 seconds
        sock.settimeout(10)
        # mode of listening
        print("​Server started, listening on IP address "+ip)
        # our message is "offer" to every client who is listening
        message = b"offer"
        while True:
            sock.sendto(message, ('255.255.255.255', 13117))
            time.sleep(1)
    except:
        print("bla")

if __name__ == '__main__':
    Main()