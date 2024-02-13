# -*- coding: UTF-8 -*-
import logging
from typing import List, Optional

from httpx import HTTPStatusError

from antsy import exceptions
from .models import Customer


logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)


class CustomersAPI:
    def __init__(self, antsy_client, version):
        self.antsy_client = antsy_client
        self.base_path = f"customers/{version}"

    def get(self, customer_uid: str) -> Optional[Customer]:
        full_url = f"{self.antsy_client.base_url}/{self.base_path}/customer/{customer_uid}"

        try:
            response = self.antsy_client.client.get(full_url).json()
        except HTTPStatusError as exc:
            logger.error("Error: %s", exc)
            return None

        if response.get("status") != "ok":
            if response.get("message") == "CUSTOMER_NOT_FOUND":
                raise exceptions.CustomerNotFound(customer_uid=customer_uid)
            if response.get("message") == "DATABASE_ERROR":
                raise exceptions.AntsyError()

            return None

        data = response.get("data")
        return Customer.model_validate(data.get("customer"))

    def create(self, **kwargs) -> Optional[Customer]:
        full_url = f"{self.antsy_client.base_url}/{self.base_path}/customers"

        # Required fields
        request_data = {}
        request_data["country_code"] = kwargs.get("country_code")
        request_data["identification_name"] = kwargs.get("identification_name")
        request_data["unique_identifier"] = kwargs.get("unique_identifier")
        request_data["first_name"] = kwargs.get("first_name")
        request_data["last_name"] = kwargs.get("last_name")

        for key, value in request_data.items():
            if value is None:
                logger.error("'%s' cannot be None", key)
                return None

        # Optional fields
        request_data["email"] = kwargs.get("email")
        request_data["address"] = kwargs.get("address")
        request_data["city"] = kwargs.get("city")
        request_data["timezone"] = kwargs.get("timezone")
        request_data["cell_phone"] = kwargs.get("cell_phone")
        request_data["work_phone"] = kwargs.get("work_phone")
        request_data["notes"] = kwargs.get("notes")
        request_data["language"] = kwargs.get("language")
        request_data["receive_sms"] = kwargs.get("receive_sms")

        try:
            response = self.antsy_client.client.post(full_url, data=request_data).json()
        except HTTPStatusError as exc:
            logger.error("Error: %s", exc)
            return None

        if response.get("status") != "ok":
            error_message = response.get("message")
            match error_message:
                case "CUSTOMER_ALREADY_EXISTS":
                    raise exceptions.CustomerAlreadyExists()
                case "INVALID_COUNTRY_CODE":
                    raise exceptions.CustomerInvalidCountryCode(country_code=request_data["country_code"])
                case "INVALID_EMAIL":
                    raise exceptions.CustomerInvalidEmail(email=request_data["email"])
                case "INVALID_ADDRESS":
                    raise exceptions.CustomerInvalidAddress(address=request_data["address"])
                case "INVALID_CITY":
                    raise exceptions.CustomerInvalidCity(city=request_data["city"])
                case "INVALID_TIMEZONE":
                    raise exceptions.CustomerInvalidTimezone(timezone=request_data["timezone"])
                case "INVALID_CELL_PHONE":
                    raise exceptions.CustomerInvalidCellPhone(cell_phone=request_data["cell_phone"])
                case "INVALID_WORK_PHONE":
                    raise exceptions.CustomerInvalidWorkPhone(work_phone=request_data["work_phone"])
                case "INVALID_NOTES":
                    raise exceptions.CustomerInvalidNotes(notes=request_data["notes"])
                case "INVALID_LANGUAGE":
                    raise exceptions.CustomerInvalidLanguage(language=request_data["language"])
                case "INVALID_RECEIVE_SMS":
                    raise exceptions.CustomerInvalidReceiveSMS(receive_sms=request_data["receive_sms"])
                case "DATABASE_ERROR":
                    raise exceptions.AntsyError()
                case _:
                    return None

        data = response.get("data")
        return Customer.model_validate(data.get("customer"))

    def search(self):
        pass
