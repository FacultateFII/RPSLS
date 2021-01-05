import socket
import sys

def parseChoice(choice):
    if choice == 'rock':
        return 1
    elif choice == 'paper':
        return 2
    elif choice == 'scissors':
        return 3
    elif choice == 'lizard':
        return 4
    elif choice == 'spock':
        return 5
    else:
        return 0

def parseComputerChoice(computerChoice):
    if computerChoice == 1:
        return 'rock'
    elif computerChoice == 2:
        return 'paper'
    elif computerChoice == 3:
        return 'scissors'
    elif computerChoice == 4:
        return 'lizard'
    elif computerChoice == 5:
        return 'spock'

if __name__ == '__main__':
    sClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sClient.connect(('localhost', 20001))
    sClient.connect(('localhost', 20002))
    try:
        print("Welcome!")
        choice = input("Enter your choice")
        sClient.send(bytes(choice, 'utf-8'))
        print("Welcome to Rock, Paper, Scissors, Lizard, Spock!")
        choice = input("Enter your choice: ")
        if parseChoice(choice) == 0:
            while parseChoice(choice) == 0:
                print("This is not a valid choice.")
                choice = input("Please enter another choice: ")
        sClient.send(bytes(parseChoice(choice)))
        computerChoice = sClient.recv(30)
        print(computerChoice)
        print("Computer chose", parseComputerChoice(bytes.decode(computerChoice)))
    finally:
        sClient.close()
