# -*- coding: UTF-8 -*-

import datetime

import pydantic


class Customer(pydantic.BaseModel):
    uid: str


class Site(pydantic.BaseModel):
    uid: str
    name: str


class Queue(pydantic.BaseModel):
    uid: str
    name: str


class Appointment(pydantic.BaseModel):
    uid: str
    status: str
    start: str


class Task(pydantic.BaseModel):
    uid: str
    status: str
    created: str


class QueueAppointment(pydantic.BaseModel):
    uid: str
    day: datetime.date
    start_time: datetime.datetime


class QueueAppointmentTask(pydantic.BaseModel):
    customer: Customer
    site: Site
    queue: Queue
    appointment: Appointment
    task: Task
