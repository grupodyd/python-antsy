# -*- coding: UTF-8 -*-


class AntsyError(Exception):
    fmt = "An unspecified error occurred"

    def __init__(self, **kwargs):
        msg = self.fmt.format(**kwargs)
        Exception.__init__(self, msg)
        self.kwargs = kwargs


class CustomerNotFound(AntsyError):
    fmt = "Customer not found: '{customer_uid}'"


class CustomerCreateRequiredField(AntsyError):
    fmt = "Field '{field}' is required when creating a customer"


class CustomerSearchRequiredField(AntsyError):
    fmt = "Field '{field}' is required when searching for a customer"


class CustomerAlreadyExists(AntsyError):
    fmt = "Customer already exists"


class CustomerInvalidCountryCode(AntsyError):
    fmt = "Invalid country code: '{country_code}'"


class CustomerInvalidEmail(AntsyError):
    fmt = "Invalid email: '{email}'"


class CustomerInvalidAddress(AntsyError):
    fmt = "Invalid address: '{address}'"


class CustomerInvalidCity(AntsyError):
    fmt = "Invalid city: '{city}'"


class CustomerInvalidTimezone(AntsyError):
    fmt = "Invalid timezone: '{timezone}'"


class CustomerInvalidCellPhone(AntsyError):
    fmt = "Invalid cell phone: '{cell_phone}'"


class CustomerInvalidWorkPhone(AntsyError):
    fmt = "Invalid work phone: '{work_phone}'"


class CustomerInvalidNotes(AntsyError):
    fmt = "Invalid notes: '{notes}'"


class CustomerInvalidLanguage(AntsyError):
    fmt = "Invalid language: '{language}'"


class CustomerInvalidReceiveSMS(AntsyError):
    fmt = "Invalid receive SMS: '{receive_sms}'"
