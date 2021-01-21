import socket
import select
import errno
import signal
import sys
import colorama
from colorama import Fore

HEADER_LENGTH = 10

IP = "192.168.230.5"
PORT = 8888

def signal_handler(sig,frame):
	print("Please exit properly by typing 'exit' while in Table No:")

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
	record = open('record.txt','a')

	#no ctrl-c allowed here
	signal.signal(signal.SIGINT, signal_handler)

	print(Fore.YELLOW)
	table_ID = input("Table No: ")

	#user exit program
	if table_ID.lower() == 'exit':
		print(Fore.WHITE)
		client_socket.close()
		sys.exit()

	record.write(f'{table_ID};')
	#create socket
	client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	client_socket.connect((IP, PORT))

	#set to non-blocking
	client_socket.setblocking(False)

	table = table_ID.encode('utf-8')
	table_header = f"{len(table):<{HEADER_LENGTH}}".encode('utf-8')
	client_socket.send(table_header + table)
	total_price = 0
	while True:
		message = input(Fore.YELLOW + f'{table_ID} > ')

		# If message is not empty - send it
		if message.lower() == 'set a' or message.lower()=='set b' or message.lower()=='set c':
			record.write(f'{message};')
			total_price += menuChoice(message)

			message = message.encode('utf-8')
			message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')

			client_socket.send(message_header + message)
		elif message.lower() =='total':
			print(Fore.YELLOW + f'TOTAL PRICE : RM {total_price}')
			record.write(f'RM {total_price}\n')
			record.close()
			break
		else:
			print(Fore.RED + 'INVALID')
			continue
