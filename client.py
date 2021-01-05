import socket

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
    else:
        return 'error'

def winLose(computerChoice):
    if computerChoice == 'w':
        print("You win!")
    elif computerChoice == 'l':
        print("You lose!")
    elif computerChoice == 't':
        print("It's a tie!")
    else:
        print("Error")

if __name__ == '__main__':
    sClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sClient.connect(('localhost', 20005))
    try:
        print("Welcome to Rock, Paper, Scissors, Lizard, Spock!")
        choice = input("Enter your choice: ")
        if parseChoice(choice) == 0:
            while parseChoice(choice) == 0:
                print("This is not a valid choice.")
                choice = input("Please enter another choice: ")
        sClient.send(bytes(str(parseChoice(choice)), 'utf8'))
        print("Waiting for server to respond...")
        computerChoice = sClient.recv(30)
        print("Computer chose", parseComputerChoice(int(str(computerChoice, 'utf8')[0])))
        winLose(str(computerChoice, 'utf8')[1])
    finally:
        sClient.close()
