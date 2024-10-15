import os
from typing import Type

from pydantic import BaseModel, Field

from superagi.helper.resource_helper import ResourceHelper
from superagi.models.agent_execution import AgentExecution
from superagi.models.agent import Agent
from superagi.tools.base_tool import BaseTool
from superagi.types.storage_types import StorageType
from superagi.config.config import get_config
from superagi.helper.s3_helper import S3Helper


class ToolDeleteFileInput(BaseModel):
    """Input for CopyFileTool."""
    path: str = Field(..., description="Path of the file to delete. Must absolute path. Don't only include file name.")
    addr: str = Field(..., description="The address of the remote server in the format: username@ip:port")
    password: str = Field(..., description="The password for accessing the remote server.")


class ToolDeleteFileTool(BaseTool):
    """
    Delete File tool

    Attributes:
        name : The name.
        agent_id: The agent id.
        description : The description.
        args_schema : The args schema.
    """
    name: str = "Tool Delete File"
    agent_id: int = None
    agent_execution_id:int = None
    args_schema: Type[BaseModel] = ToolDeleteFileInput
    description: str = "Delete a file for tool build task"

    def _execute(self, path: str, addr: str, password: str) -> str:
        from superagi.tools.tool_creator.ssh import RemoteLinuxExecutionTool
        bash_script=f'rm -f {path}'
        return RemoteLinuxExecutionTool()._execute(addr=addr, password=password, bash_script=bash_script)