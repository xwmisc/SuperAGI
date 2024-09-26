from abc import ABC
from typing import List
from superagi.tools.base_tool import BaseTool, BaseToolkit, ToolConfiguration
from superagi.tools.ssh.ssh import RemoteLinuxExecutionTool
from superagi.tools.ssh.python_run import SshPythonExecutionTool
from superagi.models.tool_config import ToolConfig
from superagi.types.key_type import ToolConfigKeyType


class RemoteLinuxExecutionToolkit(BaseToolkit, ABC):
    name: str = "Remote Linux Execution Toolkit"
    description: str = "Toolkit for connecting to a remote Linux server and executing scripts"

    def get_tools(self) -> List[BaseTool]:
        return [RemoteLinuxExecutionTool(), SshPythonExecutionTool()]

    def get_env_keys(self) -> List[ToolConfiguration]:
        return []
