import subprocess
import shutil
import random
import time

def backup_config_file(config_file_path, backup_file_path):
    """Backup the original SSH configuration file."""
    shutil.copy2(config_file_path, backup_file_path)

def edit_ssh_port_config(config_file_path, new_port):
    """Edit the port configuration in the SSH configuration file."""
    with open(config_file_path, 'r') as file:
        config_lines = file.readlines()

    port_modified = False
    for i, line in enumerate(config_lines):
        if line.strip().startswith('Port'):
            old_port = line.strip().split()[-1]
            config_lines[i] = f'Port {new_port}\n'
            port_modified = True
            break

    if not port_modified:
        config_lines.append(f'Port {new_port}\n')

    with open(config_file_path, 'w') as file:
        file.writelines(config_lines)

    restart_ssh_service()

def generate_random_port():
    """Generate a random port number between 2000 and 3000."""
    return random.randint(2000, 3000)

def restart_ssh_service():
    """Restart the SSH service."""
    subprocess.run(['systemctl', 'restart', 'ssh'])

def start_stop_ssh_service(action):
    """Start or stop the SSH service."""
    if action == "start":
        subprocess.run(['systemctl', 'start', 'ssh'])
    elif action == "stop":
        subprocess.run(['systemctl', 'stop', 'ssh'])

def port_change_process():
    """Initiate the port change process."""
    while True:
        if port_change_flag:
            new_port = generate_random_port()
            edit_ssh_port_config(ssh_config_file_path, new_port)
            time.sleep(10)
        else:
            break

def run_backend():
    """Start the backend functionality."""
    backup_config_file(ssh_config_file_path, ssh_backup_file_path)
    port_change_process()

# Define SSH configuration file paths
ssh_config_file_path = '/etc/ssh/sshd_config'
ssh_backup_file_path = '/etc/ssh/sshd_config.bak'
port_change_flag = True

if __name__ == "__main__":
    run_backend()
