from pydantic import BaseModel, HttpUrl, Field
from typing import Optional


class AppRepo(BaseModel):
    type: str
    imagePath: HttpUrl
    authType: Optional[str]


class RequiredResources(BaseModel):
    numCPU: int
    memory: int
    storage: int


class AppManifest(BaseModel):
    name: str = Field(..., regex="^[A-Za-z][A-Za-z0-9_]{1,63}$")
    version: int
    packageType: str
    appRepo: AppRepo
    requiredResources: RequiredResources
