from dataclasses import dataclass
from typing import Optional


@dataclass
class CerebrasKwargs:
    max_completion_tokens: Optional[int] = 256,
    seed: Optional[int] = 0,
    temperature: Optional[float] = 1.0,
    top_p: Optional[float] = 1.0,
