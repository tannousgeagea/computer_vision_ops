import time
import paramiko
import logging
from scp import SCPClient, SCPException
from paramiko.ssh_exception import SSHException

# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def check_remote_file_exists(ssh_client, remote_path):
    """
    Check if a file exists on a remote server using SSH.
    
    Parameters:
        - ssh_client: paramiko.SSHClient()
        - remote_path: str. The full path to the file on the remote server to check for existence.
    
    Returns:
    - bool: True if the file exists, False otherwise.
    
    Raises:
    - Exception: If there's an error connecting to the server or during the operation.
    """
    try:
        
        # Create an SFTP session over the existing connection
        sftp = ssh_client.open_sftp()
        
        # Attempt to stat the remote file. If successful, the file exists.
        try:
            sftp.stat(remote_path)
            exists = True
        except IOError:
            print(f"File {remote_path} does not exits")
            exists = False
        
        sftp.close()
    
        return exists

    except Exception as e:
        # Handle exceptions related to connection errors or others
        print(f"Failed to check file existence: {e}")
        raise

def establish_ssh_connection(hostname, port, username, password):
    """
    Establishes an SSH connection to a remote server using Paramiko.

    Parameters:
        - hostname (str): The hostname or IP address of the remote server.
        - port (int): The port number for the SSH connection.
        - username (str): The username for authentication.
        - password (str): The password for authentication.

    Returns:
        - ssh_client (paramiko.SSHClient): An established SSHClient object if the connection is successful.

    Raises:
        - SSHException: If there's any issue establishing the connection.

    Example usage:
    ssh_client = establish_ssh_connection('192.168.1.1', 22, 'user', 'password')
    """
    try:
        start_time = time.time()
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        logging.info(f"Connecting to {hostname}:{port} as {username}")
        ssh_client.connect(hostname, port=port, username=username, password=password)
        print("SSH connection established successfully in %s seconds" % round((time.time() - start_time), 2))
        return ssh_client
    except Exception as e:
        msg = f"Failed to establish SSH connection -> {str(e)}"
        print(msg)
        
        raise

def create_scp_client(ssh_client):
    """
    Creates an SCP client for file transfer over an existing SSH connection.

    Parameters:
    - ssh_client (paramiko.SSHClient): An established SSHClient object from a successful SSH connection.

    Returns:
    - scp_client (scp.SCPClient): An SCPClient object for file transfer operations.

    Raises:
    - SCPException: If there's an issue creating the SCP client.

    Example usage:
    ssh_client = establish_ssh_connection('192.168.1.1', 22, 'user', 'password')
    scp_client = create_scp_client(ssh_client)
    """
    try:
        start_time = time.time()
        scp_client = SCPClient(ssh_client.get_transport())
        print("SCP client created successfully in %s ms" % round((time.time() - start_time) * 1000, 2))
        return scp_client
    except Exception as e:
        print(f"Failed to create SCP client -> {str(e)}")
        raise

def download_file(scp_client, remote_path, local_path):
    """
    Downloads a file from the remote server using SCP.

    Parameters:
    - scp_client (scp.SCPClient): An SCPClient object for file transfer operations.
    - remote_path (str): The path to the file on the remote server that you want to download.
    - local_path (str): The destination path on the local system where the file should be saved.

    Raises:
    - SCPException: If there's an issue during the file transfer.
    """
    try:
        scp_client.get(remote_path, local_path)
        print(f"File {remote_path} downloaded to {local_path} successfully.")
    except Exception as e:
        print(f"Failed to download file -> {str(e)}")
        raise

def upload_file(scp_client, local_path, remote_path):
    """
    Uploads a file to the remote server using SCP.

    Parameters:
    - scp_client (scp.SCPClient): An SCPClient object for file transfer operations.
    - local_path (str): The path to the file on the local system that you want to upload.
    - remote_path (str): The destination path on the remote server where the file should be uploaded.

    Raises:
    - SCPException: If there's an issue during the file transfer.
    """
    try:
        scp_client.put(local_path, remote_path)
        print(f"File {local_path} uploaded to {remote_path} successfully.")
    except SCPException as e:
        print(f"Failed to upload file -> {str(e)}")
        raise

def list_files_in_directory(ssh_client, remote_directory, extension='*.jpg'):
    """
    Lists all files in a given directory on the remote server.
    
    :param ssh_client: An active SSH client session.
    :param remote_directory: The directory whose files are to be listed.
    :return: A list of file paths.
    """
    stdin, stdout, stderr = ssh_client.exec_command(f'find {remote_directory} -type f -iname "{extension}"')
    file_paths = [f"{line.strip()}" for line in stdout]
    return file_paths


def fetch_image_from_server(
    ssh_client,
    scp_client,
    remote_path="",
    local_path="",
):
    success = False
    try:
        if check_remote_file_exists(ssh_client, remote_path):
            download_file(scp_client, remote_path, local_path)
            success = True

    except Exception as e:
        error_message = f"Failed to fetch image from remote server. Check the server status or network connection: {e}"
        raise ConnectionError(error_message)

    return success