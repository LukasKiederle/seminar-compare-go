from src.server.serverThread import ServerThread

if __name__ == '__main__':

    for x in range(8):
        server = ServerThread(x)
        # Setting daemon to True will let the main thread exit even though the workers are blocking
        server.daemon = True
        server.start()
