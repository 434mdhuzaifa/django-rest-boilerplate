import sys
import traceback
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
import string
import random


def PrintErrorWithTrace():
    exc_type, exc_value, exc_traceback = sys.exc_info()
    error_message = f"{exc_type.__name__}: {str(exc_value)}"
    error_details = traceback.format_exc()
    ic("Error occurred:")
    print(error_message)
    ic("Detailed error trace:")
    print(error_details)


def convert_error_details(error_details):
    result = []
    if isinstance(error_details, list):
        for i, data in enumerate(error_details):
            result.append({"key": f"Error {i+1}", "detail": str(data)})
    else:
        for field, details in error_details.items():
            for detail in details:
                result.append({"key": field, "detail": str(detail)})
    return result


def SendResponse(data, status=200):
    
    return Response(data, status=status)


def SendMsgResponse(detail: str, status: int = 200):
    return Response({"detail": detail}, status=status)


def SendErrorResponse(error, status=500):
    PrintErrorWithTrace()
    if isinstance(error, ValidationError):
        result = convert_error_details(error.detail)
        return SendResponse(result, status)
    return SendMsgResponse(str(error), status)


def generateToken(number):
    return "".join(random.choices(string.digits, k=number))

