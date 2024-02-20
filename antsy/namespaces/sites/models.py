# -*- coding: UTF-8 -*-
from typing import List, Optional

import pydantic


class Queue(pydantic.BaseModel):
    uid: str
    name: str


class Site(pydantic.BaseModel):
    uid: str
    name: str
    queues: Optional[List[Queue]] = None


class Organization(pydantic.BaseModel):
    uid: str
    name: str
    sites: Optional[List[Site]] = None
