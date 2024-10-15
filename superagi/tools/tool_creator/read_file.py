import os
from typing import Type, Optional
import ebooklib
import bs4 
from bs4 import BeautifulSoup

from pydantic import BaseModel, Field
from ebooklib import epub
from superagi.helper.validate_csv import correct_csv_encoding

from superagi.helper.resource_helper import ResourceHelper
from superagi.helper.s3_helper import S3Helper
from superagi.models.agent_execution import AgentExecution
from superagi.resource_manager.file_manager import FileManager
from superagi.tools.base_tool import BaseTool
from superagi.models.agent import Agent
from superagi.types.storage_types import StorageType
from superagi.config.config import get_config
from unstructured.partition.auto import partition
from superagi.lib.logger import logger

class ToolReadFileSchema(BaseModel):
    """Input for CopyFileTool."""
    path: str = Field(..., description="Path of the file to read")
    addr: str = Field(..., description="The address of the remote server in the format: username@ip:port")
    password: str = Field(..., description="The password for accessing the remote server.")


class ToolReadFileTool(BaseTool):
    """
    Read File tool

    Attributes:
        name : The name.
        description : The description.
        args_schema : The args schema.
    """
    name: str = "Tool Read File"
    agent_id: int = None
    agent_execution_id: int = None
    args_schema: Type[BaseModel] = ToolReadFileSchema
    description: str = "Reads the file content in a specified location for tool build task"
    resource_manager: Optional[FileManager] = None

    def _execute(self, path: str, addr: str, password: str) -> str:
        from superagi.tools.tool_creator.ssh import RemoteLinuxExecutionTool
        bash_script=f'cat {path}'
        return RemoteLinuxExecutionTool()._execute(addr=addr, password=password, bash_script=bash_script)