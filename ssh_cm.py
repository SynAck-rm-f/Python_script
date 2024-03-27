import paramiko
import getpass


def ssh_command(ip, port, user, passwd, cmd):
    # Create an SSH client object
    client = paramiko.SSHClient()
    # Automatically add host keys
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Connect to the SSH server
        client.connect(ip, port=port, username=user, password=passwd)

        # Execute the command on the remote server
        # stdin, stdout, stderr = client.exec_command(cmd)
        # https://docs.paramiko.org/en/latest/api/client.html?highlight=client
        _, stdout, stderr = client.exec_command(cmd)

        # Read the output from the command
        output = stdout.readlines() + stderr.readlines()

        # Print the output
        if output:
            print('------------------ Output ------------------')
            for line in output:
                print(line.strip())
    except paramiko.AuthenticationException:
        print("Authentication failed. Please check your credentials.")
    except paramiko.SSHException as e:
        print("SSH error:", e)
    finally:
        # Close the SSH connection
        client.close()


if __name__ == '__main__':
    # Get user input for username, password, IP, port, and command
    in_user = input('Username: ')
    in_password = getpass.getpass(prompt='Password: ', stream=None)
    # https://docs.python.org/3/library/getpass.html
    in_ip = input('Enter server IP: ') or '172.17.46.177'
    in_port = input('Enter port or <CR>: ') or 22
    in_cmd = input('Enter command or <CR>: ') or 'ls -la && id && whoami /all'
    # Access Token on windows whoami /all
    # test
    # Call the ssh_command function with user-provided inputs
    ssh_command(in_ip, in_port, in_user, in_password, in_cmd)
