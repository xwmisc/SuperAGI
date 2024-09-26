from typing import Type
from pydantic import BaseModel, Field
from superagi.tools.base_tool import BaseTool


class SshPythonExecutionSchema(BaseModel):
    ssh_connection_info: str = Field(
      ...,
        description="The SSH connection information in the format 'user@ip:port'.",
    )
    password: str = Field(
      ...,
        description="The password for accessing the remote server.",
    )
    python_code: str = Field(
      ...,
        description="The Python 3 code to execute in the container.",
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
        "A tool for connecting to a remote server via SSH, "
        "and executing provided Python 3.6.8 code. Input should include SSH connection info in the format 'user@ip:port' "
        "and the password for accessing the server, along with the Python code to execute."
    )
    args_schema: Type[SshPythonExecutionSchema] = SshPythonExecutionSchema

    def _execute(self, ssh_connection_info: str, password: str, python_code: str) -> str:
        """
        Execute the SSH Python execution tool.

        Args:
            ssh_connection_info : The SSH connection information in the format 'user@ip:port'.
            password : The password for accessing the remote server.
            python_code : The Python 3 code to execute.

        Returns:
            The output of the executed command.
        """
        import paramiko
        import io
        import re
        import base64
        user_ip_port = ssh_connection_info
        match = re.match(r'(\w+)@([\w.]+):(\d+)', user_ip_port)
        if not match:
            return "Invalid SSH connection info format. Expected 'user@ip:port'."
        username, ip, port = match.groups()

        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh_client.connect(ip, port=int(port), username=username, password=password, timeout=60)

            # 对 Python 代码进行 base64 编码
            encoded_code = base64.b64encode(python_code.encode()).decode()

            # 创建临时文件并写入编码后的代码，然后解码到目标文件
            temp_file_name = "temp_code.py"
            command_write_encoded = f"echo '{encoded_code}' > temp_encoded.txt"
            ssh_client.exec_command(command_write_encoded)
            command_decode_to_file = "cat temp_encoded.txt | base64 -d > " + temp_file_name
            ssh_client.exec_command(command_decode_to_file)

            # 使用 SSH 操作 Docker 创建容器并挂载临时文件执行 Python 代码
            docker_run_command = f"python3 $PWD/{temp_file_name}"
            stdin, stdout, stderr = ssh_client.exec_command(docker_run_command)
            stdout_data = stdout.read().decode('utf-8')
            stderr_data = stderr.read().decode('utf-8')
            exit_status = stdout.channel.recv_exit_status()

            output = io.StringIO()
            output.write(f"Command: {docker_run_command}\n")
            output.write(f"Exit Status: {exit_status}\n")
            output.write(f"Standard Output:\n{stdout_data}\n")
            if stderr_data!= "":
                output.write(f"Error Output:\n{stderr_data}\n")

            return output.getvalue()

        except paramiko.AuthenticationException:
            return "Authentication failed: Please check username and password."
        except paramiko.SSHException as ssh_exception:
            return f"SSH connection error: {str(ssh_exception)}"
        except Exception as e:
            return f"An unexpected error occurred: {str(e)}"
        finally:
            ssh_client.close()