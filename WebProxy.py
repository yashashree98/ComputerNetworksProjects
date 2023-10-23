# Import required libraries
import socket
from urllib.parse import urlparse 
import sys
from pathlib import Path                                                                                        

# Declared constant
CACHE_DIRECTORY = 'cache'

# Function to handle client requests 
def handle_client_request(conn_client_socket):

    # Receive the request from the client
    client_request = conn_client_socket.recv(1024).decode()

    # Print the request received from client 
    print("Received a message from this client:", client_request)

    # Parse the request
    method, host, port, path, http_version = request_parsing(client_request)

    #Create a cache dir if it doesnt exist
    dir = Path(CACHE_DIRECTORY)
    dir.mkdir(parents=True,exist_ok=True)
    
    # Check if the requested file is in the cache where host=zhiju.me and path=networks
    cache_file_path = dir / host/ Path(path[1:])

    # Check if the cache dir is already created the folder; if yes print the below statement
    if cache_file_path.is_file():
        print('Yeah! The requested file is in the cache and is about to be sent to the client!')                    
        
        # Read the file from the cache file and send the response as it is Cache-Hit:1
        with open(cache_file_path, 'rb') as cachefile:
            response = cachefile.read()
            cache_hit = b'Cache-Hit: 1\r\n'
            conn_client_socket.send(cache_hit)
    else:
            # The file is not into the cache folder hence cache miss
            print('Oops! No Cache hit! Requesting origin server for the file...')   

            # Sending the request to the server to fetch the response                                    
            print('Sending the following msg from proxy to server: ', client_request, '\n host: ', host, 'Connection: close')
            
            # To print the given statements as in the project description
            try:

                # Create a socket connection to the remote server
                server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                # Connect the host and the port as entered by the user
                server_socket.connect((host, port))

                # Send the modified request to the remote server
                # Using send() to respond using a tcp connection
                server_socket.send(f'{method} {path} {http_version}\r\nHost: {host}\r\nConnection: close\r\n\r\n'.encode())

                # Receive the response from the remote server
                response = b''

                # Fetch the data in the socket using recv string one by one and collect it into respnse variable
                while True:
                    data = server_socket.recv(1024)
                    if not data:
                        break
                    response += data

                # Close the connection to the remote server
                server_socket.close()

            # Print exception if above code doesnt work
            except Exception as e:
                print(f'Error connecting to server: {e}')
                response=  b'HTTP/1.1 500 Internal Error\r\n\r\n'

            # As the request was forwarded to the server it was a Cache-Hit:0     
            cache_hit = b'Cache-Hit: 0\r\n'

            # Create sub directory under cache/host/path {cache/zhiju.me/networks/}
            dir_sub = Path(cache_file_path).parent

            # Create sub directory if it doesnt already exist
            dir_sub.mkdir(parents=True,exist_ok=True)

            # Cache the file as response is successfull i.e HTTP 200
            if response.startswith(b'HTTP/1.1 200'):
                print(f'Response received from server, and status code is 200! Write to cache to save time next time...')
        
            # Split the response header from body and write the file in the cache
                with open(cache_file_path, 'wb') as cachefile:                                                                      
                    cachefile.write(response.split(b'\r\n\r\n',1)[1])
            else:
                # Response will not be written to the file as HTTP is not 200
                print(f'Response received from server, and status code is not 200! No cache writing...')
            
            # Respond to the client
            print('Now responding the client...')

    # Add the cache hit to header of the responce
    response = response.replace(b'\r\n\r\n', b'\r\n' + cache_hit + b'\r\n')
            
    # Send the modified responce to the client
    conn_client_socket.send(response)                                                                 
        
    print('All done! Closing socket...')

    # Closing the connection socket
    conn_client_socket.close()

# Function to parse the client requests 
def request_parsing(client_request):
    
    # Extract method, host, path, version from the url
    lines = client_request.split('\r\n')
    method, url, http_version = lines[0].split(' ')
    url_parsed = urlparse(url)
    host = url_parsed.netloc
    path = url_parsed.path
    port = url_parsed.port or 80
    return method, host, port, path, http_version 

# Function to call web proxy 
def create_web_proxy(port):

    # Create a socket for the proxy server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   

    # Bind the localhost and port entered by the user   
    server_socket.bind(('localhost', port))
    server_socket.listen(1)

    print('*************** Ready to serve ***************')
    
    while True:
        # Clients socket and client address
        conn_clientsocket, address = server_socket.accept()  
        print(f'Received a  connection from: {address}')

        # Handle the client request in a separate function
        handle_client_request(conn_clientsocket)


if __name__ == '__main__':

    # Check if the argument port is given or not
    if len(sys.argv) != 2:
        print("Port number is not specified! ")
        sys.exit()
    
    port = int(sys.argv[1])

    #Calculate server port number using SU ID
    server_port = port + (4193376) % 100
    
    # Call the web proxy function to start the code execution
    create_web_proxy(port)