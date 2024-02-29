# -*- coding: UTF-8 -*-
import logging
from typing import List, Optional

from dateutil.parser import parse
from httpx import HTTPStatusError

from antsy import exceptions
from .models import QueueAppointment, QueueAppointmentTask

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)


class AppointmentsAPI:
    def __init__(self, antsy_client, version):
        self.__antsy_client = antsy_client
        self.__base_path = f"appointments/{version}"

    def get_queue_appointments(self, queue_uid: str) -> Optional[List[QueueAppointment]]:
        full_url = f"{self.__antsy_client.base_url}/{self.__base_path}/queue/{queue_uid}"

        try:
            response = self.__antsy_client.client.get(full_url).json()
        except HTTPStatusError as exc:
            logger.error(f"Error: {exc}")
            return None

        if response.get("status") != "ok":
            return None

        data = response.get("data")

        output: List[QueueAppointment] = []
        for appointment in data.get("appointments"):
            entry = {"uid": appointment.get("uid")}
            entry["day"] = parse(appointment.get("day")).date()
            entry["start_time"] = parse(appointment.get("start_time"))

            output.append(QueueAppointment.model_validate(entry))

        return output

    def create(self, queue_appointment_uid: str, customer_uid: str, **kwargs) -> Optional[QueueAppointmentTask]:
        full_url = f"{self.__antsy_client.base_url}/{self.__base_path}/appointments"

        request_data = {"queue_appointment_uid": queue_appointment_uid, "customer_uid": customer_uid}

        try:
            response = self.__antsy_client.client.post(full_url, json=request_data).json()
        except HTTPStatusError as exc:
            logger.error("Error: %s", exc)
            return None

        if response.get("status") != "ok":
            error_message = response.get("message")
            match error_message:
                case "CUSTOMER_ALREADY_EXISTS":
                    raise exceptions.InvalidCustomerUID(customer_uid=customer_uid)
                case "INVALID_QUEUE_APPOINTMENT_UID":
                    raise exceptions.InvalidQueueAppointmentUID(queue_appointment_uid=queue_appointment_uid)
                case "QUEUE_APPOINTMENT_NOT_FOUND":
                    raise exceptions.QueueAppointmentNotFound(queue_appointment_uid=queue_appointment_uid)
                case "QUEUE_APPOINTMENT_NOT_AVAILABLE":
                    raise exceptions.QueueAppointmentNotAvailable(queue_appointment_uid=queue_appointment_uid)
                case "DATABASE_ERROR":
                    raise exceptions.AntsyError()
                case _:
                    return None

        data = response.get("data")
        return QueueAppointmentTask.model_validate(data)

    def get_customer_appointments(self, customer_uid: str) -> Optional[List[QueueAppointment]]:
        full_url = f"{self.__antsy_client.base_url}/{self.__base_path}/customer/{customer_uid}"

        try:
            response = self.__antsy_client.client.get(full_url).json()
        except HTTPStatusError as exc:
            logger.error(f"Error: {exc}")
            return None

        if response.get("status") != "ok":
            return None

        data = response.get("data")
        return [QueueAppointment.model_validate(appointment) for appointment in data.get("appointments")]
