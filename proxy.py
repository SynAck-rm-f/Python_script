import sys
import socket
import threading

HEX_FILTER = ''.join(
    [(len(repr(chr(i))) == 3) and chr(i) or '.' for i in range(256)])


def hexdump(src, length=16):
    result = []  # Initialize an empty list to store formatted lines
    digits = 4 if isinstance(src, str) else 2  # Determine the number of digits to represent each byte

    # Iterate over the source data in chunks of length
    for i in range(0, len(src), length):
        s = src[i:i + length]  # Get a chunk of data of specified length
        # Convert each byte in the chunk to its hexadecimal representation
        hexa = b' '.join([b"%0*X" % (digits, x) for x in s])  # Removed ord() function
        # Convert non-printable characters to '.' and keep printable characters as is
        text = b''.join([bytes([x]) if 0x20 <= x < 0x7F else b'.' for x in s])  # Adjusted to handle bytes directly
        # Format the line with the offset, hexadecimal representation, and text representation
        result.append(
            b"%04X   %-*s   %s" % (i, length * (digits + 1), hexa, text))

    print(b'\n'.join(result))


def receive_from(connection):
    # For receiving both local and remote data, we pass in the socket object
    # to be used. We create an empty byte string, buffer, that will accumulate
    # responses from the socket
    buffer = b''

    # By default, we set a five-second timeout, which
    # might be aggressive if you’re proxying traffic to other countries or over lossy
    # networks, so increase the timeout as necessary.
    connection.settimeout(8)  # WSL NAT ?

    try:
        # We set up a loop to read
        # response data into the buffer
        # keep reading into the buffer until there's no more data or we time-out
        while True:
            data = connection.recv(4096)
            if not data:
                break
            # return the buffer byte string to the caller,
            # which could be either the local or remote machine
            buffer += data

    except TimeoutError:
        pass

    return buffer


# modify the response or request packets
# before the proxy sends them on their way
def request_handler(buffer):
    # perform packet modifications
    return buffer


def response_handler(buffer):
    # perform packet modifications
    return buffer

    # Inside these functions, you can modify the packet contents, perform
    # fuzzing tasks, test for authentication issues, or do whatever else your heart desires


def proxy_handler(client_socket, remote_host, remote_port, receive_first):
    # connect to the remote host
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))

    # Then we check to make sure we don’t need to first initiate a connection
    # to the remote side and request data
    # before going into the main loop. Some server daemons will expect you
    # to do this (FTP servers typically send a banner first, for example)
    if receive_first:
        remote_buffer = receive_from(remote_socket)
        hexdump(remote_buffer)

        # send it to our response handler
        remote_buffer = response_handler(remote_buffer)

        # if we have data to send to our local client send it
        if len(remote_buffer):
            print("[<==] Sending %d bytes to localhost." % len(remote_buffer))
            client_socket.send(remote_buffer)

    # now let's loop and read from local, send to remote, send to local
    # rinse wash repeat
    while True:
        # read from local host
        local_buffer = receive_from(client_socket)

        if len(local_buffer):
            print("[==>] Received %d bytes from localhost." % len(local_buffer))
            hexdump(local_buffer)

            # send it to our request handler
            local_buffer = request_handler(local_buffer)

            # send off the data to the remote host
            remote_socket.send(local_buffer)
            print("[==>] Sent to remote.")

        # receive back the response
        remote_buffer = receive_from(remote_socket)

        if len(remote_buffer):
            print("[<==] Received %d bytes from remote." % len(remote_buffer))
            hexdump(remote_buffer)

            # send to our response handler
            remote_buffer = response_handler(remote_buffer)

            # send the response to the local socket
            client_socket.send(remote_buffer)

            print("[<==] Sent to localhost.")

        # if no more data on either side close the connections
        if not len(local_buffer) or not len(remote_buffer):
            client_socket.close()
            remote_socket.close()
            print("[*] No more data. Closing connections.")
            break


def server_loop(local_host, local_port, remote_host, remote_port,
                receive_first):
    # The server_loop function creates a socket and then binds to the local
    # host and listens
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((local_host, local_port))
    except socket.error as exc:
        print("[!!] Failed to listen on %s:%d" % (local_host,
                                                  local_port))
        print("[!!] Check for other listening sockets or correct "
              "permissions.")
        print(f"[!!] Caught exception error: {exc}")
        sys.exit(0)

    print("[*] Listening on %s:%d" % (local_host, local_port))

    server.listen(5)

    while True:
        # when a fresh connection request
        # comes in, we hand it off to the proxy_handler in a new thread which does
        # all of the sending and receiving of juicy bits to either side of the data stream.
        client_socket, addr = server.accept()

        # print out the local connection information
        print("[==>] Received incoming connection from %s:%d" % (
            addr[0], addr[1]))

        # start a thread to talk to the remote host
        proxy_thread = threading.Thread(target=proxy_handler, args=(
            client_socket, remote_host, remote_port, receive_first))
        proxy_thread.start()


def main():
    # no fancy command line parsing here
    if len(sys.argv[1:]) != 5:
        print("Usage: ./proxy.py [localhost] [localport] [remotehost] "
              "[remoteport] [receive_first]")
        print("Example: ./proxy.py 127.0.0.1 9000 10.12.132.1 9000 True")
        sys.exit(0)

    # setup local listening parameters
    local_host = sys.argv[1]
    local_port = int(sys.argv[2])

    # setup remote target
    remote_host = sys.argv[3]
    remote_port = int(sys.argv[4])

    # this tells our proxy to connect and receive data
    # before sending to the remote host
    receive_first = sys.argv[5]

    if "True" in receive_first:
        receive_first = True
    else:
        receive_first = False

    # now spin up our listening socket
    server_loop(local_host, local_port, remote_host, remote_port, receive_first)


main()
