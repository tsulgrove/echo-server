import socket
import sys
import traceback


def client(msg, log_buffer=sys.stderr):

    server_address = ('127.0.0.1', 10000)
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_IP)
    
    print('connecting to {0} port {1}'.format(*server_address), file=log_buffer)

    #connect to the address
    sock.connect(server_address)
    received_message = ''

    try:
        print('sending "{0}"'.format(msg), file=log_buffer)
        
        #send the message, declare buffer, and timeout
        sock.sendall(msg.encode("utf-8"))
        buffer_size = 16
        sock.settimeout(1)
        
        while True:
            
            #recieve a chunk of the message
            chunk = sock.recv(buffer_size)
            
            #if there is nothing then break
            if not chunk:
                break
            
            print('received "{0}"'.format(chunk.decode('utf8')), file=log_buffer)
            
            #add on to recieved message
            received_message += chunk.decode("utf8")
            
    except socket.timeout:
        #catch the timeout when they are done talking
        pass       
    
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
        
    finally:
        #close up when done
        sock.close()
        print('closing socket', file=log_buffer)

    return received_message

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage = '\nusage: python echo_client.py "this is my message"\n'
        print(usage, file=sys.stderr)
        sys.exit(1)

    msg = sys.argv[1]
    client(msg)
