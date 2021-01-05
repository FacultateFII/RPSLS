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
    sServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sServer.bind(('localhost', 20002))
    sServer.setblocking(False)
    sServer.listen(3)
    inputs = [sServer]
    outputs = []
    choices = {}

    while inputs:
        readSocks, writeSocks, exceptSocks = select.select(inputs, outputs, inputs, 300)

        for sock in readSocks:
            if sock is sServer:
                sClient, clientAddress = sServer.accept()
                sClient.setblocking(False)
                inputs.append(sClient)
                print("Client connected from: ", clientAddress)
            else:
                c = sock.recv(30)
                choice = int(str(c, 'utf8'))
                if choice:
                    choices[sock] = choice
                    if sock not in outputs:
                        outputs.append(sock)
                else:
                    if sock in outputs:
                        outputs.remove(sock)
                    inputs.remove(sock)
                    sock.close()
                    del choices[sock]

        for client in writeSocks:
            computerChoice = RPSLS(choices[client])
            if not choices[client]:
                outputs.remove(client)
            else:
                client.send(bytes(computerChoice, 'utf8'))

        for client in exceptSocks:
            inputs.remove(client)
            if client in outputs:
                outputs.remove(client)
            client.close()
            del choices[client]
