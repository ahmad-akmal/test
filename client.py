import socket
import select
import errno

HEADER_LENGTH = 10

IP = "192.168.56.101"
PORT = 8888

my_username = "Kitchen"
print(my_username)

#create socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))

#recv() call won't block, just return exception
client_socket.setblocking(False)

username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(username_header + username)

while True:
	try:
		while True:

			username_header = client_socket.recv(HEADER_LENGTH)
			if not len(username_header):
				print('Connection closed by the server')
				sys.exit()
			username_length = int(username_header.decode('utf-8').strip())
			username = client_socket.recv(username_length).decode('utf-8')

			message_header = client_socket.recv(HEADER_LENGTH)
			message_length = int(message_header.decode('utf-8').strip())
			message = client_socket.recv(message_length).decode('utf-8')

			print(f'{username} > {message}')

	except IOError as e:

		if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
			print('Reading error: {}'.format(str(e)))
			sys.exit()

	except Exception as e:

		print('Reading error: '.format(str(e)))
		sys.exit()
