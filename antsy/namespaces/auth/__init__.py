# -*- coding: UTF-8 -*-
import logging
from typing import Optional

from httpx import HTTPStatusError

from .models import AccessToken, WhoAmI

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)


class AuthAPI:
    def __init__(self, antsy_client, version):
        self.__antsy_client = antsy_client
        self.__base_path = f"auth/{version}"

    def refresh(self) -> Optional[AccessToken]:
        full_url = f"{self.__antsy_client.base_url}/{self.__base_path}/refresh"

        try:
            response = self.__antsy_client.client.get(full_url).json()
        except HTTPStatusError as exc:
            logger.error("Error: %s", exc)
            return None

        if response.get("status") != "ok":
            return None

        return AccessToken.model_validate(response.get("data"))

    def whoami(self) -> Optional[WhoAmI]:
        full_url = f"{self.__antsy_client.base_url}/{self.__base_path}/whoami"
        try:
            response = self.__antsy_client.client.get(full_url).json()
        except HTTPStatusError as exc:
            logger.error("Error: %s", exc)
            return None

        if response.get("status") != "ok":
            return None

        return WhoAmI.model_validate(response.get("data"))
