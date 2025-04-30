from mailbox import MHMessage

from rest_framework.authtoken.models import Token

from authapp.models import OTP, CustomUser
from  methodism import custom_response, error_messages, MESSAGE

def regis(request, params):
    return {
        'bu regis' : 'Bu regis Funksiyasi'
    }

def login(request, params):

    otp = OTP.objects.filter(key=params['key']).first()
    if not otp:
        return custom_response(False, message=MESSAGE['AuthToken'])

    user = CustomUser.objects.filter(phone=params.phone).first()
    if not user:
        return custom_response(False, message=MESSAGE['UserNotFound'])

    if not user.check_password(params['password']):
        return custom_response(False, message=MESSAGE['PasswordError'])

    token = Token.objects.get_or_create(user=user)

    return custom_response(True, data={"token" : token[0].key}, message={'success' : 'Tizimga hush kelibsiz bordar'})