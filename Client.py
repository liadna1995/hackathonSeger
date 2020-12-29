# Import socket module
import socket

# def state1_looking_for_server():
# def state2_connecting_to_server():
# def state2_game_mode():

# def Main():
#     # local host IP '127.0.0.1'
#     host = '127.0.0.1'
#
#     # Define the port on which you want to connect
#     port = 12345
#
#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#
#     # connect to server on local computer
#     s.connect((host, port))
#
#     # message you send to server
#     message = "shaurya says geeksforgeeks"
#     while True:
#
#         # message sent to server
#         s.send(message.encode('ascii'))
#
#         # messaga received from server
#         data = s.recv(1024)
#
#         # print the received message
#         # here it would be a reverse of sent message
#         print('Received from the server :', str(data.decode('ascii')))
#
#         # ask the client whether he wants to continue
#         ans = input('\nDo you want to continue(y/n) :')
#         if ans == 'y':
#             continue
#         else:
#             break
#     # close the connection
#     s.close()

def Main():
    message = b'\xfe\xed\xbe\xef\x02'
    while True:
        #try:
            # local host IP '127.0.0.1'
            ip = '127.0.0.1'

            #UDP
            port = 13117
            client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            client.bind(("", port))

            #TCP
            clientTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            print("Client started, listening for offer requests...")
            data, addr = client.recvfrom(1024)
            if data[0:4] != message[0:4]:
                print('Wrong message')
                continue

            print("Received offer from " + ip + "," + " attempting to connect...")
            clientTCP.connect((ip, int(hex(data[5])[2:]+hex(data[6])[2:], 16)))
            clientTCP.sendall(bytes('Liad&Shahar', 'utf-8'))

        #except:
            #print("bla")



if __name__ == '__main__':
    Main()