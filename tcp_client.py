import socket


def main():
    try:
        target_host = "www.google.com"
        target_port = 80
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to a specific address and port
        tcp_socket.connect((target_host, target_port))  # Use a tuple (host, port)
        tcp_socket.send(b"GET / HTTP/1.1\r\nHost: www.google.com\r\n\r\n")
        print("TCP socket created and bound successfully.")
        response = tcp_socket.recv(4096)
        print(response.decode())
        tcp_socket.close()

    except ConnectionResetError as e:
        print(f"Connection was reset: {e}")
        # Handle the error gracefully, such as retrying the operation or notifying the user
    except socket.timeout as e:
        print(f"Socket timed out: {e}")
        # Handle timeout errors
    except Exception as e:
        print(f"An error occurred: {e}")
        # Handle other types of errors


if __name__ == '__main__':
    main()
