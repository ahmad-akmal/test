import socket
import select
import errno
import signal
import sys
import colorama
from colorama import Fore

HEADER_LENGTH = 10

IP = "192.168.56.101"
PORT = 8888

def signal_handler(sig,frame):
	print("Please exit properly by typing 'exit' while in Username:")

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
	#file open
	history = open('history.txt','a')

	#no ctrl-c allowed here
	signal.signal(signal.SIGINT, signal_handler)

	print(Fore.YELLOW)
	my_username = input("Username: ")

	#user exit program
	if my_username.lower() == 'exit':
		print(Fore.WHITE)
		sys.exit()

	history.write(f'{my_username};')
	#create socket
	client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	client_socket.connect((IP, PORT))

	#set to non-blocking
	client_socket.setblocking(False)

	username = my_username.encode('utf-8')
	username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
	client_socket.send(username_header + username)
	total_price = 0
	while True:
		message = input(Fore.YELLOW + f'{my_username} > ')

		# If message is not empty - send it
		if message.lower() == 'set a' or message.lower()=='set b' or message.lower()=='set c':
			history.write(f'{message};')
			total_price += menuChoice(message)

			message = message.encode('utf-8')
			message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')

			client_socket.send(message_header + message)
		elif message.lower() =='total':
			print(Fore.YELLOW + f'Harga : RM {total_price}')
			history.write(f'RM {total_price}\n')
			history.close()
			break
		else:
			print(Fore.RED + 'invalid')
			continue
