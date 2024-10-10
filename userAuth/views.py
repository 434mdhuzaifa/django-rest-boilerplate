from django.shortcuts import render
from rest_framework.decorators import api_view
from userAuth.serializers import UserInputSerializers
from common.utility import PrintErrorWithTrace,SendMsgResponse,SendResponse
from rest_framework.serializers import ValidationError
# Create your views here.
@api_view(["POST"])
def userCreate(request):
    try:
        userData= UserInputSerializers(request.data)
        validate_data=userData.run_validation(userData.data)
        userData.create(validate_data)
        return SendMsgResponse("User creation successfull",201)
    except ValidationError as e:
        PrintErrorWithTrace()
        return SendMsgResponse(str(e),400)
    except Exception as e:
        PrintErrorWithTrace()
        return SendMsgResponse(str(e),500)
@api_view(["POST"])
def userLogin(request):
    pass       