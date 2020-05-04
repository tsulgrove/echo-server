import socket
import sys
import traceback


def server(log_buffer=sys.stderr):
    # set an address for our server
    address = ('127.0.0.1', 10000)
    
    #set up socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_IP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(address)
    
    # log that we are building a server
    print("making a server on {0}:{1}".format(*address), file=log_buffer)

    #start listening
    sock.listen(1)

    try:
        while True:
            print('waiting for a connection', file=log_buffer)
            
            #accept connection, set buffer, and timeout
            conn, addr = sock.accept()
            buffer_size = 16
            conn.settimeout(5)
    
            try:
                print('connection - {0}:{1}'.format(*addr), file=log_buffer)

                while True:
                    #recive message from client
                    received_message = conn.recv(buffer_size)
                    
                    data = received_message
                    print('received "{0}"'.format(data.decode('utf8')))
                    
                    #send message back
                    conn.sendall(data)
                    
                    print('sent "{0}"'.format(data.decode('utf8')))
                    
                    #if there is no message then stop this madness in the name of the king
                    if not data:
                        break
                    
            except Exception as e:
                traceback.print_exc()
                sys.exit(1)
                
            finally:
                #close up when done.
                conn.close()
                print(
                    'echo complete, client connection closed', file=log_buffer
                )

    except KeyboardInterrupt:
        #kill command
        sock.close()
        print('quitting echo server', file=log_buffer)


if __name__ == '__main__':
    server()
    sys.exit(0)
