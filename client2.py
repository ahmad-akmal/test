import socket
import select
import errno
import sys

HEADER_LENGTH = 10

IP = "192.168.208.7"
PORT = 8888

def menuChoice(set):
	if set.lower() == 'set a':
		price = 30
	elif set.lower() == 'set b':
		price = 35
	elif set.lower() == 'set c':
		price = 40
	else:
		return 0
	return price

while True:
	history = open('history.txt','a')

	my_username = input("Username: ")
	if my_username.lower() == 'exit':
		sys.exit()

	history.write(f'{my_username};')
	#create socket
	client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	client_socket.connect((IP, PORT))

	#non-blocking
	client_socket.setblocking(False)

	username = my_username.encode('utf-8')
	username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
	client_socket.send(username_header + username)
	total_price = 0
	while True:
		message = input(f'{my_username} > ')
		# If message is not empty - send it
		if message.lower() == 'set a' or message.lower()=='set b' or message.lower()=='set c':
			history.write(f'{message};')
			total_price += menuChoice(message)

			message = message.encode('utf-8')
			message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')

			client_socket.send(message_header + message)
		elif message.lower() =='total':
			print(f'Harga : RM {total_price}')
			history.write(f'RM {total_price}\n')
			history.close()
			break
		elif message.lower() =='exit':
			sys.exit()
			history.close()
		else:
			print('invalid')
			continue
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

				# Print message
				print(f'{username} > {message}')

		except IOError as e:
			if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
				print('Reading error: {}'.format(str(e)))
				sys.exit()

				# We just did not receive anything
				continue

		except Exception as e:
			# Any other exception
			print('Reading error: '.format(str(e)))
			sys.exit()
