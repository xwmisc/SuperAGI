from typing import Type

from pydantic import BaseModel, Field
from superagi.tools.base_tool import BaseTool


class RemoteLinuxExecutionSchema(BaseModel):
    ip: str = Field(
       ...,
        description="The IP address of the remote Linux server.",
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
        "Input should include IP address, username, password, and the Bash script command."
    )
    args_schema: Type[RemoteLinuxExecutionSchema] = RemoteLinuxExecutionSchema

    def _execute(self, ip: str, username: str, password: str, bash_script: str) -> str:
        """
        Execute the remote Linux execution tool.

        Args:
            ip : The IP address of the remote server.
            username : The username for accessing the server.
            password : The password for accessing the server.
            bash_script : The Bash script command to execute.

        Returns:
            The output of the executed command.
        """
        try:
            import paramiko

            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(ip, username=username, password=password)
            stdin, stdout, stderr = ssh.exec_command(bash_script)
            output = stdout.read().decode('utf-8')
            ssh.close()
            return output
        except Exception as e:
            return f"Error: {str(e)}"