# Made with help from tutorials at Sentdex youtube channel


import socket
import select

HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 1234

# Create TCP IPv4 Socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Set socket options to reuse socket addresses
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind socket to IP and port
server_socket.bind((IP, PORT))

# Set socket to listen mode
server_socket.listen()

# List of known sockets
sockets_list = [server_socket]

# Dict for each socket containing last receieved message
clients = {}


# Receice message from socket and returned parsed header and body
def recieve_msg(client_socket):
    try:
        message_header = client_socket.recv(HEADER_LENGTH)

        if not len(message_header):
            return False

        message_length = int(message_header.decode("utf-8").strip())
        return {"header": message_header, "data": client_socket.recv(message_length)}

    except:
        return False


while True:
    read_sockets, _, exception_sockets = select.select(
        sockets_list, [], sockets_list)

    for notified_socket in read_sockets:
        if notified_socket == server_socket:
            # Someone just made a connection request
            client_socket, client_address = server_socket.accept()

            user = recieve_msg(client_socket)
            if user is False:
                continue

            sockets_list.append(client_socket)
            clients[client_socket] = user

            print(
                f"Accepted new connection from {client_address[0]}:{client_address[1]} username: {user['data'].decode('utf-8')}")

        else:
            message = recieve_msg(notified_socket)

            # Find username for socket
            user = clients[notified_socket]
            user_name = user['data'].decode('utf-8')

            # Connection Lost
            if message is False:
                print(f"Closed connection from {user_name}")
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
                continue

            # Decode Message received
            user_message = message['data'].decode('utf-8')
            print(f"Recieved message from {user_name}: {user_message}")

            # Send recieved message to all other clients
            for client_socket in clients:
                if client_socket != notified_socket:
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])

    # Any sockets that recieve an exception, remove connection
    for notified_socket in exception_sockets:
        sockets_list.remove(notified_socket)
        del clients[notified_socket]