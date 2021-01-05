import socket
import select
import random

def RPSLS(choice):
    computerChoice = random.randint(1, 5)
    if computerChoice == 1:
        if choice == 1:
            return '1t'
        elif choice == 2 or choice == 5:
            return '1w'
        elif choice == 3 or choice == 4:
            return '1l'
        else:
            return '0a'
    elif computerChoice == 2:
        if choice == 2:
            return '2t'
        elif choice == 3 or choice == 4:
            return '2w'
        elif choice == 1 or choice == 5:
            return '2l'
        else:
            return '0a'
    elif computerChoice == 3:
        if choice == 3:
            return '3t'
        elif choice == 1 or choice == 5:
            return '3w'
        elif choice == 2 or choice == 4:
            return '3l'
        else:
            return '0a'
    elif computerChoice == 4:
        if choice == 4:
            return '4t'
        elif choice == 1 or choice == 3:
            return '4w'
        elif choice == 2 or choice == 5:
            return '4l'
        else:
            return '0a'
    elif computerChoice == 5:
        if choice == 5:
            return '5t'
        elif choice == 2 or choice == 4:
            return '5w'
        elif choice == 1 or choice == 3:
            return '5l'
        else:
            return '0a'
    else:
        return '0a'

if __name__ == '__main__':
    print("Press q to quit")
    sServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sServer.bind(('localhost', 20005))
    sServer.setblocking(False)
    sServer.listen(3)
    inputs = [sServer]
    outputs = []
    choices = {}
    clientsNumber = 0

    while inputs:
        readSocks, writeSocks, exceptSocks = select.select(inputs, outputs, inputs)

        for sock in readSocks:
            if sock is sServer:
                if clientsNumber < 3:
                    sServer.setblocking(False)
                    sClient, clientAddress = sServer.accept()
                    sClient.setblocking(False)
                    inputs.append(sClient)
                    clientsNumber += 1
                    print("Client connected from: ", clientAddress)
                else:
                    sServer.setblocking(True)
            else:
                c = sock.recv(30)
                if c:
                    choice = int(str(c, 'utf8'))
                    choices[sock] = choice
                    if sock not in outputs:
                        outputs.append(sock)
                else:
                    if sock in outputs:
                        outputs.remove(sock)
                    inputs.remove(sock)
                    sock.close()
                    del choices[sock]
                    clientsNumber -= 1

        for sock in writeSocks:
            if choices[sock]:
                computerChoice = RPSLS(choices[sock])
                sock.send(bytes(computerChoice, 'utf8'))
                outputs.remove(sock)

        for sock in exceptSocks:
            inputs.remove(sock)
            if sock in outputs:
                outputs.remove(sock)
            sock.close()
            del choices[sock]
            clientsNumber -= 1
