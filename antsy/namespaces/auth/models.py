# -*- coding: UTF-8 -*-
from typing import Optional

import pydantic


class AccessToken(pydantic.BaseModel):
    access_token: str


class Site(pydantic.BaseModel):
    uid: str
    name: str


class Organization(pydantic.BaseModel):
    uid: str
    name: str


class WhoAmI(pydantic.BaseModel):
    organization: Organization
    site: Optional[Site] = None
