from openai import OpenAI
import traceback
from superagi.lib.logger import logger


class OpenAiEmbedding:
    def __init__(self, api_key, model="text-embedding-v2"):
        self.model = model
        self.api_key = api_key
        
    async def get_embedding_async(self, text: str):
        try:
            client = OpenAI()
            response = await client.embeddings.create(
                input=[text],
                model=self.model
            )
            return response.data[0].embedding
        except Exception as exception:
            logger.error(f'OpenAiEmbedding Error traceback: {traceback.format_exc()}')
            return {"error": exception}    

               
    def get_embedding(self, text):
        try:
            client = OpenAI()
            response = client.embeddings.create(
                input=[text],
                model=self.model
            )
            return response.data[0].embedding
        except Exception as exception:
            logger.error(f'OpenAiEmbedding Error traceback: {traceback.format_exc()}')
            return {"error": exception}
