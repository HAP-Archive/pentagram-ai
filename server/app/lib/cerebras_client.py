import os
import sys
from typing import List, Dict, Any
from functools import wraps

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ..lib.rich_logging import logger as log
from ..models.cerebras_kwargs import CerebrasKwargs

from cerebras.cloud.sdk import Cerebras, CerebrasError
from dotenv import load_dotenv, find_dotenv

load_dotenv((find_dotenv()))


DEFAULT_SYSTEM_PROMPT = """
You are a creative AI curator specializing in Stable Diffusion image generation.
Create engaging, mysterious captions that spark curiosity and wonder from the
prompt that is sent to you. Each post should include the following:
1. A Title that starts with '@' before the title.
2. Brief description of the art's mood and essence from the prompt.
3. Philosophical or though-provoking reflection.
4. 3-4 relevant emojis.
4. Strategic hashtags that focus on:
    - AI art communities (#aiart #stablediffusion #sd)
    - Art style (#digitalart #conceptart #fantasyart)
    - Mood/theme (#dystopian #scifi #surreal)
    - Growth tags (#aiartist #digitalcreator #aiartwork)
    - Engagement (#photooftheday #viral #trending)
    - Include many other tags that would be appropriate for the prompt provided.
    
Keep captions between 100 to 150 words. Maintain a mysterious, avant-garde tone that
positions you as a curator of digital dreams and future visions.
"""

NUMERIC_PARAMS = [
    "temperature",
    "max_completion_tokens",
    "top_p",
    "seed"
]


def validate_numerics(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        numeric_params = {
            k: v for k, v in kwargs.items()
            if isinstance(v, (int, float)) and k in NUMERIC_PARAMS
        }

        for param, value in numeric_params.items():
            if value < 0:
                raise ValueError(f"Invalid value was provided for param: {param}, value: {value}.")

            if value == 0:
                kwargs.pop(param)

        return func(self, *args, **kwargs)

    return wrapper


class CerebrasClient:
    def __init__(self):
        self.__api_key = os.getenv("CEREBRAS_API_KEY")
        try:
            self.__client = Cerebras(
                api_key=self.__api_key,
                default_headers={
                    "Authorization": f"Bearer {self.__api_key}",
                    "Content-Type": "application/json"
                }
            )
            self.__client_models = self.__client.models.list()

        except CerebrasError as e:
            log.warn(f"Provided key: {self.__api_key} is invalid, Error: {str(e)}")
            raise e

    @property
    def client_models(self) -> list:
        return self.__client_models

    @property
    def client(self) -> Cerebras:
        return self.__client

    @client.setter
    def client(self, client: Cerebras) -> None:
        if not isinstance(client, Cerebras):
            raise ValueError(f"Provided type for client is not of type Cerebras.")

        self.__client = client

    def set_api_key(self, api_key: str) -> None:
        if not isinstance(api_key, str):
            raise ValueError(f"Provided type for api_key is not of type str.")

        self.__api_key = api_key

    @validate_numerics
    def create_chat_completion(self,
                               messages: List[Dict[str, str]],
                               config: CerebrasKwargs = None) -> Any:

        if not messages:
            raise ValueError(f"Provided messages: {messages} is invalid.")

        kwargs = {
            "model": os.getenv("CEREBRAS_MODEL"),
            "messages": [
                {
                    "role": "system",
                    "content": DEFAULT_SYSTEM_PROMPT
                },
                *messages
            ],
            "max_completion_tokens": config.max_completion_tokens,
            "temperature": config.temperature,
            "top_p": config.top_p,
            "seed": config.seed
        }

        try:
            response = self.__client.chat.completions.create(**kwargs)

            return (
                response.choices[0].message.content,
                response.usage.prompt_tokens,
                response.usage.completion_tokens,
                response.usage.total_tokens
            )

        except CerebrasError as e:
            log.error(f"Error creating chat completion: {str(e)}")
            raise e

        except Exception as e:
            log.error(f"Other error occurred while creating chat completion: {str(e)}")
            raise e
