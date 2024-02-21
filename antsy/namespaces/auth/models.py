# -*- coding: UTF-8 -*-

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
    site: Site
    organization: Organization
