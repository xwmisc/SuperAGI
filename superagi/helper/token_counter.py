from typing import List

import tiktoken

from superagi.types.common import BaseMessage
from superagi.lib.logger import logger
from superagi.models.models import Models
from sqlalchemy.orm import Session


class TokenCounter:

    def __init__(self, session:Session=None, organisation_id: int=None):
        self.session = session
        self.organisation_id = organisation_id

    def token_limit(self, model: str = "gpt-3.5-turbo-0301") -> int:
        """
        Function to return the token limit for a given model.

        Args:
            model (str): The model to return the token limit for.

        Raises:
            KeyError: If the model is not found.

        Returns:
            int: The token limit.
        """
        return 8092

    @staticmethod
    def count_message_tokens(messages: List[BaseMessage], model: str = "gpt-3.5-turbo-0301") -> int:
        """
        Function to count the number of tokens in a list of messages.

        Args:
            messages (List[BaseMessage]): The list of messages to count the tokens for.
            model (str): The model to count the tokens for.

        Raises:
            KeyError: If the model is not found.

        Returns:
            int: The number of tokens in the messages.
        """
        default_tokens_per_message = 4
        encoding = tiktoken.get_encoding("cl100k_base")
        tokens_per_message = default_tokens_per_message

        num_tokens = 0
        for message in messages:
            if isinstance(message, str):
                message = {'content': message}
            num_tokens += tokens_per_message
            num_tokens += len(encoding.encode(message['content']))

        num_tokens += 3
        print("tokens",num_tokens)
        return num_tokens

    @staticmethod
    def count_text_tokens(message: str) -> int:
        """
        Function to count the number of tokens in a text.

        Args:
            message (str): The text to count the tokens for.

        Returns:
            int: The number of tokens in the text.
        """
        encoding = tiktoken.get_encoding("cl100k_base")
        num_tokens = len(encoding.encode(message)) + 4
        return num_tokens
