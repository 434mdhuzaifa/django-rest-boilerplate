import sys
import traceback
from rest_framework.response import Response
def PrintErrorWithTrace():
    exc_type, exc_value, exc_traceback = sys.exc_info()
    error_message = f"{exc_type.__name__}: {str(exc_value)}"
    error_details = traceback.format_exc()
    ic("Error occurred:")
    print(error_message)
    ic("Detailed error trace:")
    print(error_details)

def SendResponse(data,status):
    return Response(data,status=status)

def SendMsgResponse(msg:str,status:int):
    return Response({"msg":msg},status=status)