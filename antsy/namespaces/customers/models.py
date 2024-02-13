# -*- coding: UTF-8 -*-
from typing import Optional

import pydantic


class CustomerBirthDay(pydantic.BaseModel):
    day: int
    month: int
    year: int


class Customer(pydantic.BaseModel):
    id: str
    uid: str
    first_name: str
    last_name: str
    name: str = None
    middle_name: str = None
    middle_name: Optional[str] = None
    verified: bool = False
    birthday: Optional[CustomerBirthDay] = None
