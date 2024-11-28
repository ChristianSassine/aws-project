import time
import paramiko
from utils import get_path
from constants import *
import select


class File:
    def __init__(self, path, name):
        self.path = get_path(path)
        self.name = name


def bootstrap_instance(
    key_path: str,
    address: str,
    files_to_upload: list[File],
    instance_id: str,
    bootstrap_async: bool,
):
    # Initialize clients
    print(f"[{instance_id}] Starting bootstrap process...")
    ssh_client = create_ssh_client(key_path, address)
    transport = ssh_client.get_transport()
    channel = transport.open_session()
    sftp_client = ssh_client.open_sftp()

    try:
        # Upload necessary files
        print(f"[{instance_id}] Uploading files...")
        remote_directory = "/home/ubuntu/"

        for file in files_to_upload:
            sftp_upload(sftp_client, file.path, remote_directory + file.name)

        # Execute bootstrap script
        print(f"[{instance_id}] Bootstrapping the instance...")
        command = f"chmod +x bootstrap.sh && ./bootstrap.sh"
        if bootstrap_async:
            command = f"chmod +x bootstrap.sh && nohup ./bootstrap.sh > /dev/null 2>&1 &"
            
        channel.set_combine_stderr(True)
        channel.exec_command(command)

        # Output ssh
        while not channel.exit_status_ready():
            rl, _, _ = select.select([channel], [], [], 0.0)
            if len(rl) > 0:
                print(channel.recv(1024).decode("utf-8"))

    except Exception as e:
        print(f"[{instance_id}] Failed to bootstrap instance: {e}")
    finally:
        channel.close()
        transport.close()
        ssh_client.close()
        sftp_client.close()


def sftp_upload(sftp_client, file_path, remote_path):
    # Upload the file
    sftp_client.put(file_path, remote_path)
    print(f"Successfully uploaded files")


def create_ssh_client(key_path, address):

    # Variables
    local_key_path = get_path(key_path)
    key = paramiko.RSAKey.from_private_key_file(local_key_path)
    remote_user = "ubuntu"

    # Create a transport object
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Attempt to connect with ssh
    timeout = 300
    end_time = time.time() + timeout
    while time.time() < end_time:
        try:
            print(f"Attempting to connect to {address} via SSH...")
            ssh_client.connect(
                hostname=address, port=22, username=remote_user, pkey=key
            )
            print("SSH is available!")
            return ssh_client
        except (paramiko.SSHException, Exception) as e:
            print(f"SSH not available yet: {e}")
            time.sleep(5)  # Wait before retrying

    raise Exception("Couldn't connect to the ssh server")
