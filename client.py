import socket
import sys

if __name__ == '__main__':
    sClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sClient.connect(('localhost', 20001))
    try:
        print("Welcome!")
        choice = input("Enter your choice")
        sClient.send(bytes(choice, 'utf-8'))
        computerChoice = sClient.recv(30)
        print(computerChoice)
    finally:
        sClient.close()
