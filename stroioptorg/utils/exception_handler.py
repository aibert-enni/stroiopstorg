from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import exceptions
from rest_framework.serializers import as_serializer_error

from rest_framework.views import exception_handler

def drf_custom_exception_handler(exc, context):
    if isinstance(exc, DjangoValidationError):
        exc = exceptions.ValidationError(as_serializer_error(exc))

    response = exception_handler(exc, context)

    if response is not None:
        response.data['status_code'] = response.status_code

    return response