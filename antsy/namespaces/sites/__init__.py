# -*- coding: UTF-8 -*-
import logging
from typing import Optional

from httpx import HTTPStatusError

from antsy import exceptions
from .models import Organization, Queue, Site


logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)


class SitesAPI:
    def __init__(self, antsy_client, version):
        self.__antsy_client = antsy_client
        self.__base_path = f"sites/{version}"

    def get(self, site_uid: str) -> Optional[Site]:
        full_url = f"{self.__antsy_client.base_url}/{self.__base_path}/site/{site_uid}"

        try:
            response = self.__antsy_client.client.get(full_url).json()
        except HTTPStatusError as exc:
            logger.error("Error: %s", exc)
            return None

        if response.get("status") != "ok":
            if response.get("message") == "DATABASE_ERROR":
                raise exceptions.AntsyError()
            if response.get("message") == "SITE_NOT_FOUND":
                raise exceptions.SiteNotFound(site_uid=site_uid)

            return None

        data = response.get("data")

        try:
            site = Site.model_validate(data.get("site"))
            site.queues = [Queue.model_validate(queue) for queue in data.get("queues")]
        except Exception as exc:
            logger.error("Error: %s", exc)
            return None

        return site

    def get_organization_sites(self) -> Optional[Organization]:
        full_url = f"{self.__antsy_client.base_url}/{self.__base_path}/organization"

        try:
            response = self.__antsy_client.client.get(full_url).json()
        except HTTPStatusError as exc:
            logger.error("Error: %s", exc)
            return None

        if response.get("status") != "ok":
            if response.get("message") == "DATABASE_ERROR":
                raise exceptions.AntsyError()
            if response.get("message") == "ORGANIZATION_NOT_FOUND":
                raise exceptions.OrganizationNotFound(organization_uid="organization_uid")

            return None

        data = response.get("data")

        try:
            organization = Organization.model_validate(data.get("organization"))
            organization.sites = [Site.model_validate(site) for site in data.get("sites")]
        except Exception as exc:
            logger.error("Error: %s", exc)
            return None

        return organization
