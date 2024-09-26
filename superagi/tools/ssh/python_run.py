from typing import Type
from pydantic import BaseModel, Field
from superagi.tools.base_tool import BaseTool
from superagi.lib.logger import logger


class SshPythonExecutionSchema(BaseModel):
    ssh_connection_info: str = Field(
      ...,
        description="The SSH connection information in the format 'user@ip:port'.",
    )
    password: str = Field(
      ...,
        description="The password for accessing the remote server.",
    )
    python_script: str = Field(
      ...,
        description="The completely Python3 script content to execute. Dont use `;` in the script, use `\n` and format code instead.",
    )


class SshPythonExecutionTool(BaseTool):
    """
    SSH Python Execution tool

    Attributes:
        name : The name.
        description : The description.
        args_schema : The args schema.
    """
    name = "SshPythonExecution"
    description = (
        "A tool for executing provided Python 3.6.8 script on remote host path '/'. "
        "Input should include SSH connection info in the format 'user@ip:port' "
        "and the password for accessing the server, along with the Python script to execute."
    )
    args_schema: Type[SshPythonExecutionSchema] = SshPythonExecutionSchema

    def _execute(self, ssh_connection_info: str, password: str, python_script: str) -> str:
        """
        Execute the SSH Python execution tool.

        Args:
            ssh_connection_info : The SSH connection information in the format 'user@ip:port'.
            password : The password for accessing the remote server.
            python_script : The Python3 script content to execute.

        Returns:
            The output of the executed command.
        """
        import paramiko
        import re
        import base64
        user_ip_port = ssh_connection_info
        match = re.match(r'(\w+)@([\w.]+):(\d+)', user_ip_port)
        if not match:
            return "Invalid SSH connection info format. Expected 'user@ip:port'."
        username, ip, port = match.groups()

        with paramiko.SSHClient() as ssh:
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                ssh.connect(ip, port=int(port), username=username, password=password, timeout=60)

                # 对 Python 代码进行 base64 编码
                encoded_code = base64.b64encode(python_script.encode()).decode()

                # 创建临时文件并写入编码后的代码，然后解码到目标文件
                temp_file = "/temp_encoded.txt"
                target_file = "/target_code.py"
                command_write_encoded = f"echo '{encoded_code}' > {temp_file}"
                ssh.exec_command(command_write_encoded)
                command_decode_to_file = f"cat /temp_encoded.txt | base64 -d > {target_file}"
                ssh.exec_command(command_decode_to_file)

                # 使用 SSH 操作 Docker 创建容器并挂载临时文件执行 Python 代码
                command = f"python3 {target_file}"
                stdin, stdout, stderr = ssh.exec_command(command)
                stdout_data = stdout.read().decode('utf-8')
                stderr_data = stderr.read().decode('utf-8')
                exit_status = stdout.channel.recv_exit_status()

                output = f"Python Script: {python_script}\n"
                output += f"Exit Status: {exit_status}\n"
                output += f"Standard Output:\n{stdout_data}\n"
                if stderr_data != "":
                    output += f"Error Output:\n{stderr_data}\n"

                return output

            except paramiko.AuthenticationException:
                return "Authentication failed: Please check username and password."
            except paramiko.SSHException as ssh_exception:
                return f"SSH connection error: {str(ssh_exception)}"
            except Exception as e:
                import traceback
                logger.error(f'Python Tool Error traceback: {traceback.format_exc()}')
                return f"An unexpected error occurred: {str(e)}"