# -*- coding: UTF-8 -*-
from typing import List, Optional

import pydantic


class Queue(pydantic.BaseModel):
    uid: str
    name: str


class SiteLocation(pydantic.BaseModel):
    country_code: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    timezone: Optional[str]


class Site(pydantic.BaseModel):
    uid: str
    name: str
    queues: Optional[List[Queue]] = None
    location: Optional[SiteLocation] = None


class Organization(pydantic.BaseModel):
    uid: str
    name: str
    sites: Optional[List[Site]] = None
