import os
from typing import Type

from pydantic import BaseModel, Field

from superagi.helper.resource_helper import ResourceHelper
from superagi.helper.s3_helper import S3Helper
from superagi.tools.base_tool import BaseTool
from superagi.models.agent import Agent
from superagi.types.storage_types import StorageType
from superagi.config.config import get_config


class ListFileInput(BaseModel):
    path: str = Field(..., description="The path of the directory to list files in. Only show max 50 files.")
    addr: str = Field(..., description="The address of the remote server in the format: username@ip:port")
    password: str = Field(..., description="The password for accessing the remote server.")


class ListFileTool(BaseTool):
    """
    List File tool

    Attributes:
        name : The name.
        agent_id: The agent id.
        description : The description.
        args_schema : The args schema.
    """
    name: str = "List File"
    agent_id: int = None
    args_schema: Type[BaseModel] = ListFileInput
    description: str = "lists files in a directory recursively"

    def _execute(self, path: str, addr: str, password: str) -> str:
        from superagi.tools.tool_creator.ssh import RemoteLinuxExecutionTool
        bash_script=f'find "{path}" -type f | head -n 50'
        return RemoteLinuxExecutionTool()._execute(addr=addr, password=password, bash_script=bash_script)

