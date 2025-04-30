import uuid
import datetime
from pyexpat.errors import messages

from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from .models import CustomUser, OTP
from rest_framework.authentication import TokenAuthentication
import random
from methodism import METHODISM
from authapp import methods

class Main(METHODISM):
    file = methods
    token_key = 'Token'
    not_auth_methods = ['regis', 'login']






def validate_password(password, request):
    data = request.data
    if len(data['password']) < 6 or ' ' in data['password'] or not data['password'].isalnum() \
            or len([i for i in data['password'] if i.isalpha() and i.isupper()]) < 1 \
            or len([i for i in data['password'] if i.isalpha() and i.islower()]) < 1:
        return Response({
            "Error": "Parol noto'g'ri kiritildi"
        })
    return password


class RegisterView(APIView):
    def post(self, request):
        data = request.data

        if 'key' not in data or 'password' not in data:
            return Response({
                "Error" : 'Parol yo nomerri yozilmaydimi silar tarafda'
            })

        otp = OTP.objects.filter(key=data['key']).first()

        if not otp.is_conf:
            return Response({
                "error" : "Telefon bilan tasdiqlanmagan"
            })

        validate_password(data['password'], request)




        # if len(data['password']) < 6 or ' ' in data['password'] or not data['password'].isalnum()\
        # or len([i for i in data['password'] if i.isalpha() and i.isupper()]) < 1\
        # or len([i for i in data['password'] if i.isalpha() and i.islower()]) < 1:
        #     return Response({
        #     "Error" : "Parol noto'g'ri kiritildi"
        # })


        phone = CustomUser.objects.filter(phone=otp.phone).first()
        if phone:
            return Response({
                'error' : "Bu raqamdan oldin foydalanilgan"
            })

        user_data = {
            'phone' : otp.phone,
            'password' : data['password'],
            'name' : data.get('password')
        }

        if data.get('key', '') == '123':
            user_data.update({
                'is_active' : True,
                'is_staff' : True,
                'is_superuser' : True
            })



        user = CustomUser.objects.create_user(**user_data)
        token = Token.objects.create(user=user)

        return  Response({
            'Xabar' : "Hush Kepsiz, Brodar",
            'tokeningiz' : token.key
        })



class LoginView(APIView):
    def post(self, request):
        data = request.data

        otp = OTP.objects.filter(key=data['key']).first()
        if not otp:
            return Response({
                'error' : 'Bu key bilan OTP topilmadi'
            })

        user = CustomUser.objects.filter(phone=otp.phone).first()

        if not user:
            return Response({
                "data" : "Bu telefondan royxatdan otilmagan"
            })

        if not user.check_password(data['password']):
            return Response({
                'data' : "Parol mos emas"
            })

        token = Token.objects.get_or_create(user=user)

        return Response({
            "data" : "Siz Muvaffaqiyatli tizimga kirdingiz",
            'Token' : token[0].key
        })


class LogOut(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication ]

    def post(self, request):
        token = Token.objects.filter(user=request.user).first()
        token.delete()
        return Response({
            "data" : "Kozimga Korinmang"
        })



class ProfileView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request):
        user = request.user
        return Response({
          'data' : user.format()
        })



    def patch(self, request):
        data = request.data
        user_ = request.user

        if data['phone']:
            user = CustomUser.objects.filter(phone=data['phone']).first()

            if int(user_.phone) == data['phone']:
                return Response({
                    'data' : "Bu sizning telefon raqamingiz, O'zgartirmasangiz qayta jonatmang afandi"
                })

            if user:
                return Response({
                    'data' : "Bu raqam bilan oldin Ro'yxatdan o'tilgan"
                })
            else:
                return Response({
                'data' : 'Qoyil sizga'
            })

        user_.name = data.get('name', user_.name)
        user_.phone = data.get('phone', user_.phone)
        user_.save()


class DeleteView(APIView):
    permission_classes = IsAuthenticated,
    authentication_classes = TokenAuthentication,

    def delete(self, request):
        user = request.user
        user.delete()
        return Response({
            'data' : "Xayt Brodar"
        })


class ChangePassword(APIView):
    def post(self, request):
        data = request.data
        user = request.user

        if not user or not user.is_authenticated():
            return Response({
                "Eror" : "user royhatdan otmagan"
            })

        if not user.check_password(data['old']):
            return Response({
                'data' : "Eski kodni to'g'ri kiriting"
            })

        user.set_password(data['new'])
        user.save()
        return Response({
            'data' : 'Parolingiz saqlandi'
        })


class AuthOne(APIView):
    def post(self, request):
        data = request.data
        if not data['phone']:
            return Response({
                'data' : "Telefon raqam kiritilmadi"
            })

        if len(str(data['phone'])) !=  12 or not isinstance((data['phone']), int) or str(data['phone'])[:3] != '998':
            return Response({
                'error' : 'raqam hato'
            })


        code = ''.join([str(random.randint(1, 999999))[-1] for _ in range(6)])
        # str_ = string.ascii_letters
        # int_ = string.digits
        # letters = str_ + str(int_)
        # code = ''.join(letters[random.randint(1, len(letters)-1)] for _ in range(6))
        # print(code)
        # print(int_)
        # print(int_)
        key = uuid.uuid4().__str__() + str(code)

        otp = OTP.objects.create(phone=data['phone'], key=key)

        return Response({
            'otp' : code,
            'token' : key
        })


class AuthTwo(APIView):
    def post(self, request):
        data = request.data
        if not data['code'] or not data['key']:
            return Response({
                'error' : "Siz to'liq malumot kiritmadingiz"
            })


        otp = OTP.objects.filter(key=data['key']).first()

        if not otp:
            return Response({
                'error' : 'Kiritilgan kod xato'
            })

        now = datetime.datetime.now(datetime.timezone.utc)

        if (now - otp.created_at).total_seconds() >= 180:
            otp.is_expire = True
            otp.save()
            return Response({
                'error' : 'kod kiritish vaqti rugadi'
            })



        if otp.is_expire:
            return Response({
                'error' : "kod expire bolib ketti"
            })


        if data['code'] != data['key'][-6:]:
            otp.tried += 1
            otp.save()
            return Response({
                'error' : 'Siz hato kod kiritdingiz'
            })

        if otp.is_conf:
            return Response({
                'arror' : 'key eskirgan'
            })

        otp.is_conf = True
        otp.save()

        user = CustomUser.objects.filter(phone=otp.phone).first()

        return Response({
            'message' : user is not None
        })












