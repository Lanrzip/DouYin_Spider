import paramiko


class SSHConfig:
    
    server_user = "root"
    server_host = "region-42.seetacloud.com"
    server_path = "/root/"
    server_port = 27691
    server_password = "8VGQlBc7XbQU"

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(server_host, port=server_port, username=server_user, password=server_password)

    transport = paramiko.Transport((server_host, server_port))
    transport.connect(username=server_user, password=server_password)
    sftp = paramiko.SFTPClient.from_transport(transport)


ssh_config = SSHConfig()