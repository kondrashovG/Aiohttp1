from typing import Optional, Type

import pydantic


class CreateAd(pydantic.BaseModel):
    title: str
    description: str
    owner: str


class PatchAd(pydantic.BaseModel):
    title: Optional[str]
    description: Optional[str]
    owner: Optional[str]


VALIDATION_CLASS = Type[CreateAd] | Type[PatchAd]
