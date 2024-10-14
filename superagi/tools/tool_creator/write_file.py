from typing import Type, Optional
from superagi.lib.logger import logger
from pydantic import BaseModel, Field

# from superagi.helper.s3_helper import upload_to_s3
from superagi.resource_manager.file_manager import FileManager
from superagi.tools.base_tool import BaseTool
from superagi.tools.tool_creator.ssh import RemoteLinuxExecutionTool
import base64
import re
import json

# from superagi.helper.s3_helper import upload_to_s3


class WriteFileInput(BaseModel):
    """Input for CopyFileTool."""
    path: str = Field(..., description="Path of the file to write. Include path. Don't Only include the file name.")
    content: str = Field(..., description="File content to write")
    addr: str = Field(..., description="The address of the remote server in the format: username@ip:port")
    password: str = Field(..., description="The password for accessing the remote server.")


class WriteFileTool(BaseTool):
    """
    Write File tool

    Attributes:
        name : The name.
        description : The description.
        agent_id: The agent id.
        args_schema : The args schema.
        resource_manager: File resource manager.
    """
    name: str = "Write File"
    args_schema: Type[BaseModel] = WriteFileInput
    description: str = "Writes text to a file"
    agent_id: int = None
    resource_manager: Optional[FileManager] = None

    class Config:
        arbitrary_types_allowed = True

    def _check_path(self, path: str):
        try:
            rule = json.loads(self.get_tool_config("write_rule"))
        except Exception as e:
            logger.error(f"Error loading write rule: {e}")
            return True
        whitelist_patterns = [re.compile(pattern) for pattern in rule['whitelist']]
        blacklist_patterns = [re.compile(pattern) for pattern in rule['blacklist']]
        for pattern in whitelist_patterns:
            if pattern.match(path):
                for black_pattern in blacklist_patterns:
                    if black_pattern.search(path):
                        return False
                return True
        return False

    def _execute(self, path: str, content: str, addr: str, password: str) -> str:
        
        if not self._check_path(path):
            return f'Denied. User telling you NOT TO write to this path({path}).'
        
        base64enc = base64.b64encode(content.encode()).decode()
        bash_script = f'file_path={path};dir=$(dirname "$file_path");mkdir -p "$dir";echo "{base64enc}" | base64 -d > "$file_path"; chmod 777 "$file_path"'

        return RemoteLinuxExecutionTool()._execute(addr=addr, password=password, bash_script=bash_script, echo_command=f"write {path}")
