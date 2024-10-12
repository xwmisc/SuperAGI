from superagi.lib.logger import logger


class RemoteLinuxExecutionTool():
    
    def _parse_user_input(self, user_input):
        # 使用正则表达式提取用户名、IP地址和端口号
        import re
        pattern = r'(?P<username>[^@]+)@(?P<ip>[^:]+):(?P<port>\d+)'
        match = re.match(pattern, user_input)
        
        if match:
            return match.groupdict()
        else:
            return None

    def _execute(self, addr: str, password: str, bash_script: str, echo_command: str="") -> str:
        """
        Execute the remote Linux execution tool.

        Args:
            addr : The IP address and port in the format: username@ip:port.
            password : The password for accessing the server.
            bash_script : The Bash script command to execute.

        Returns:
            The output of the executed command.
        """
        target = self._parse_user_input(addr)
        if not target:
            return "Invalid input format. Please provide the IP address, port, and username in the format: username@ip:port"
        ip, port, username = target['ip'], target['port'], target['username']
        
        import paramiko
        import socket
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(ip, port=int(port), username=username, password=password, timeout=60)

            stdin, stdout, stderr = ssh.exec_command(bash_script)
            stdout_data = stdout.read().decode('utf-8')
            stderr_data = stderr.read().decode('utf-8')
            exit_status = stdout.channel.recv_exit_status()
    
            if echo_command != "":
                output = f"Command: {echo_command}\n"
            else:
                output = f"Command: {bash_script}\n"
            output += f"Exit Status: {exit_status}\n"
            output += f"Standard Output:\n{stdout_data}\n"
            if stderr_data != "":
                output += f"Error Output:\n{stderr_data}\n"

            return output

        except paramiko.AuthenticationException:
            return "Authentication failed: Please check username and password"
        except paramiko.SSHException as ssh_exception:
            return f"SSH connection error: {str(ssh_exception)}"
        except socket.error as socket_error:
            return f"Network error: {str(socket_error)}"
        except Exception as e:
            import traceback
            logger.error(f'SSH Tool Error traceback: {traceback.format_exc()}')
            return f"An unexpected error occurred: {str(e)}"
        finally:
            ssh.close()
