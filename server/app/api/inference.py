import os
import re
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ..lib.rich_logging import logger as log
from ..lib.cerebras_client import CerebrasClient, CerebrasKwargs

from fastapi import APIRouter, Query

TITLE_REGEX = r"@([^\n]+)\n"
HASHTAG_REGEX = r"#\w+"

router = APIRouter(
    prefix="/api/v1",
    tags=["AI", "Inference", "Modal", "Cerebras"],
)
client = CerebrasClient()


def sanitized_content(content: str):
    return re.sub(r'@([^\n]+)\n|#\w+\s*', '', content).strip()


def format_request(
        prompt: str,
        content: str,
        prompt_tokens: int,
        completion_tokens: int,
        total_tokens: int
):
    title = re.match(TITLE_REGEX, content).group(1)
    hashtags = re.finditer(HASHTAG_REGEX, content)
    hashtags_lst = []

    for idx, tag in enumerate(hashtags, 1):
        hashtags_lst.append({
            "id": idx,
            "tag": tag.group()
        })

    return {
        "prompt": prompt,
        "content": sanitized_content(content),
        "usage": {
            "prompt_tokens": str(prompt_tokens),
            "completion_tokens": str(completion_tokens),
            "total_tokens": str(total_tokens)
        },
        "title": title,
        "hashtags": hashtags_lst
    }


@router.post("/inference")
async def inference_request(
        prompt: str = Query(..., description="Prompt that was used for Image Generation."),
        max_completion_tokens: int = Query(256, description="Maximum number of tokens to generate."),
        temperature: float = Query(1, description="Temperature for the model."),
        top_p: float = Query(1, description="Top p for the model."),
        seed: int = Query(0, description="Seed for the model.")):
    try:
        log.info(f"Received user prompt that generated an image: {prompt}")

        config = CerebrasKwargs(
            max_completion_tokens=max_completion_tokens,
            temperature=temperature,
            top_p=top_p,
            seed=seed)

        response, prompt_tokens, completion_tokens, total_tokens = client.create_chat_completion(
            messages=[
                {
                    "role": "user",
                    "content": f"""
                    Take the following prompt and create a content for a viral instagram post:
                    {prompt}
                    """
                }
            ],
            config=config
        )

        if not response:
            log.error(f"No response was received from Cerebras.")
            raise ValueError(f"No response was received from Cerebras for prompt: {prompt}")

        log.info(f"Response from Cerebras LLM: {response}")
        return format_request(
            prompt=prompt,
            content=response,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens
        )

    except Exception as e:
        log.error(f"Error occurred while generating image: {str(e)}")
        raise e
