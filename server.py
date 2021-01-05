import socket
import select

if __name__ == '__main__':
    sServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sServer.bind(('localhost', 20001))
    sServer.setblocking(False)
    sServer.listen(3)
    inputs = [sServer]
    outputs = []
    choices = {}

    quitCommand = False
    while not quitCommand:
        readSocks, writeSocks, exceptSocks = select.select(inputs, outputs, inputs, 300)

        for sock in readSocks:
            if sock is sServer:
                sClient, clientAddress = sServer.accept()
                sClient.setblocking(False)
                inputs.append(sClient)
                print("Client connected from: ", clientAddress)
            else:
                choice = sock.recv(30)
                print(choice)
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
            #generate computer choice and send
            #RSPS and send
            if not choices[client]:
                outputs.remove(client)
            else:
                client.send(bytes(str(choices[client]), 'utf-8'))


        for client in exceptSocks:
            inputs.remove(client)
            if client in outputs:
                outputs.remove(client)
            client.close()
            del choices[client]

        command = input('No new actions for the past 60s. Quit? (yes/no)\n')
        if command == 'yes':
            quitCommand = True 
