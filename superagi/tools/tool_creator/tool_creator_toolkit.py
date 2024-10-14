from abc import ABC
from typing import List
from superagi.tools.base_tool import BaseTool, BaseToolkit, ToolConfiguration
from superagi.tools.tool_creator.delete_file import DeleteFileTool
from superagi.tools.tool_creator.list_files import ListFileTool
from superagi.tools.tool_creator.read_file import ReadFileTool
from superagi.tools.tool_creator.write_file import WriteFileTool
from superagi.types.key_type import ToolConfigKeyType
from superagi.models.tool_config import ToolConfig


class ToolCreatorToolkit(BaseToolkit, ABC):
    name: str = "Tool Creator"
    description: str = "Tool Creator"

    def get_tools(self) -> List[BaseTool]:
        return [DeleteFileTool(), ListFileTool(), ReadFileTool(), WriteFileTool(), ]

    def get_env_keys(self) -> List[ToolConfiguration]:
        '''
{
    "whitelist": ["/root/aiops-sdk/.*"],
    "blacklist": ["aiops-tool\\.sh$", "standard\\.sh$"]
}
        '''
        return [ToolConfiguration(key="write_rule", key_type=ToolConfigKeyType.STRING, is_required=True)]
