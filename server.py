import socket
import select
import sys

HEADER_LENGTH = 10

IP = ''
PORT = 8888

#Create socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((IP, PORT))

server_socket.listen()

sockets_list = [server_socket]

#connected clients - socket as a key, user header and name as data
clients = {}

print(f'Listening for connections...')

#receiving message from the clients
def newMessage(client_socket):

	try:
		message_header = client_socket.recv(HEADER_LENGTH)
		if not len(message_header):
			return False

		message_length = int(message_header.decode('utf-8'))
		return {'header': message_header, 'data': client_socket.recv(message_length)}

	#lost connection
	except:
		return False

while True:
	read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)
	for current_socket in read_sockets:

		if current_socket == server_socket:

			# Accept new connection
			client_socket, client_address = server_socket.accept()
			waiter = newMessage(client_socket)

			if waiter is False:
				continue

			# Add accepted socket to select.select() list
			sockets_list.append(client_socket)
			clients[client_socket] = waiter
			print('Accepted new connection from {}:{}, username: {}'.format(*client_address, waiter['data'].decode('utf-8')))

		# Else existing socket is sending message
		else:
			message = newMessage(current_socket)

			#client disconnected
			if message is False:
				print('Closed connection from: {}'.format(clients[current_socket]['data'].decode('utf-8')))
				sockets_list.remove(current_socket)
				del clients[current_socket]

				continue

			waiter = clients[current_socket]
			print(f'Received message from {waiter["data"].decode("utf-8")}: {message["data"].decode("utf-8")}')

			for client_socket in clients:
				#not sender
				if client_socket != current_socket:
					client_socket.send(waiter['header'] + waiter['data'] + message['header'] + message['data'])

	#handle socket exceptions
	for current_socket in exception_sockets:
		sockets_list.remove(current_socket)
		del clients[current_socket]
