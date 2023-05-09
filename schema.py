import pydantic
from typing import Optional, Type


class CreateAd(pydantic.BaseModel):
    title: str
    description: str
    owner: str

    # @pydantic.validator("password")
    # def validate_password(cls, value):
    #     if len(value) < 8:
    #         raise ValueError("Password is too short")
    #     return value


class PatchAd(pydantic.BaseModel):
    title: Optional[str]
    description: Optional[str]
    owner: Optional[str]

    # @pydantic.validator("password")
    # def validate_password(cls, value):
    #     if len(value) < 8:
    #         raise ValueError("Password is too short")
    #     return value


VALIDATION_CLASS = Type[CreateAd] | Type[PatchAd]
