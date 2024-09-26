from typing import Type

from pydantic import BaseModel, Field
from superagi.tools.base_tool import BaseTool


class RemoteLinuxExecutionSchema(BaseModel):
    ip: str = Field(
       ...,
        description="The IP address of the remote Linux server.",
    )
    port: str = Field(
       ...,
        description="The port number for SSH connection, default is 22.",
    )
    username: str = Field(
       ...,
        description="The username for accessing the remote server.",
    )
    password: str = Field(
       ...,
        description="The password for accessing the remote server.",
    )
    bash_script: str = Field(
       ...,
        description="The Bash script command to execute on the remote server.",
    )


class RemoteLinuxExecutionTool(BaseTool):
    """
    Remote Linux Execution tool

    Attributes:
        name : The name.
        description : The description.
        args_schema : The args schema.
    """
    name = "RemoteLinuxExecution"
    description = (
        "A tool for connecting to a remote Linux server and executing a Bash script command."
        "Input should include IP address, port, username, password, and the Bash script command."
    )
    args_schema: Type[RemoteLinuxExecutionSchema] = RemoteLinuxExecutionSchema

    def _execute(self, ip: str, port: str, username: str, password: str, bash_script: str) -> str:
        """
        Execute the remote Linux execution tool.

        Args:
            ip : The IP address of the remote server.
            port : The port number for SSH connection.
            username : The username for accessing the server.
            password : The password for accessing the server.
            bash_script : The Bash script command to execute.

        Returns:
            The output of the executed command.
        """
        import paramiko
        import socket
        with paramiko.SSHClient() as ssh:
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                ssh.connect(ip, port=int(port), username=username, password=password, timeout=60)
                with ssh.exec_command(bash_script) as (stdin, stdout, stderr):
                    stdout_data = stdout.read().decode('utf-8')
                    stderr_data = stderr.read().decode('utf-8')
                    exit_status = stdout.channel.recv_exit_status()

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
                return f"An unexpected error occurred: {str(e)}"
