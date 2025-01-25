from socket import *
import sys

if len(sys.argv) < 3: # Check if the user has specified serverIP and serverPort
    print("Format to run program: python3 ./MessageBoardClient.py <serverIP> <serverPort>")
    sys.exit(1)

# Create the TCP socket and initiate connection to the server
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.settimeout(10)
try:
    # sys.argv = sys.argv[1] (serverIP), sys.argv[2] (serverPort)
    clientSocket.connect((sys.argv[1], int(sys.argv[2])))
except ConnectionRefusedError:
    print("server: ERROR - Connection to server failed. Please check server IP address and port.")
    sys.exit(1)
except TimeoutError:
    print("server: ERROR - Connection timed out. Please check server IP and port.")
    sys.exit(1)

def getInput():
    try:
        return input("client: ")
    except Exception as e:
        print("server: ERROR - Input failed to receive")
        return None

def sendCommand(command):
    try:
        clientSocket.send(command.encode())
    except Exception as e:
        print("server: ERROR - Failed to send command")

def receiveCommand():
    try:
        return clientSocket.recv(4096).decode()
    except Exception as e:
        print("server: ERROR - Failed to receive command")
        return None

def closeSocket():
    try:
        clientSocket.close()
    except Exception as e:
        print("ERROR - Failed to close socket")



def main():
    while True:
        try:
            command = input("client: ")
            if command == 'POST':
                # Send command to server
                sendCommand('POST')

                while True:
                    lineInput = getInput()
                    # Send command to server
                    sendCommand(lineInput)

                    if lineInput == '#':
                        break
                serverReply = receiveCommand()
                if serverReply == 'OK':
                    print('server: OK')

            elif command == 'GET':
                # Send command to server
                sendCommand('GET')
                
                # Prints response from server
                while True:
                    serverMsg = receiveCommand()
                    print("server: " + serverMsg)
                    if serverMsg == '#':
                        break

            elif command == 'DELETE':
                # Send command to server
                sendCommand('DELETE')

                while True:
                    # Send command to server
                    lineInput = getInput()
                    sendCommand(lineInput) # message ID to delete

                    if lineInput == '#':
                        break
                try:
                    serverMsg = receiveCommand()
                    if serverMsg == 'OK':
                        print('server: OK')
                    else:
                        raise ValueError()
                except ValueError as e:
                    print("server: ERROR - Wrong ID")

            elif command == 'QUIT':
                # Send command to server
                sendCommand('QUIT')

                serverMsg = receiveCommand()
                if serverMsg == 'OK':
                    print('server: OK')
                closeSocket()
                break

            else:
                raise ValueError()
            
        except KeyboardInterrupt as e:
            print("\nserver: ERROR - Wrong command")
            print("server: To quit, type 'QUIT'")
        except EOFError as e:
            print("\nserver: ERROR - Wrong command")
            print("server: To quit, type 'QUIT'")  
        except ValueError as e:
            print("server: ERROR - Command not understood")

if __name__ == '__main__':
    main()      