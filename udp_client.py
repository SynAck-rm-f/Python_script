import socket


def main():
    try:
        # Create a UDP socket
        # localhost/127.0.0.1 => because c'est la lo / hostname computer popup Windows FIREWALL
        target_host = "127.0.0.1"
        target_port = 9997
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Bind the socket to a specific address and port
        udp_socket.bind((target_host, target_port))  # Use a tuple (host, port)
        udp_socket.sendto(b"DATA1234566666666666666", (target_host, target_port))
        print("UDP socket created and bound successfully.")
        # Your code to establish connection or perform network operation
        while True:
            data, address = udp_socket.recvfrom(4096)  # Receive data with maximum buffer size of 1024 bytes
            print(f"Received data from {address}: {data.decode()}")
            # Close the socket
            # udp_socket.close() test wireshark

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
