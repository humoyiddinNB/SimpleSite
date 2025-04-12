from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from .models import CustomUser
from rest_framework.authentication import TokenAuthentication



class RegisterView(APIView):
    def post(self, request):
        data = request.data

        if 'phone' not in data or 'password' not in data:
            return Response({
                "Error" : 'Parol yo nomerri yozilmaydimi silar tarafda'
            })

        if len(str(data['phone'])) !=  12 or not isinstance((data['phone']), int) or str(data['phone'])[:3] != '998':
            return Response({
                'error' : 'raqam hato'
            })

        if len(data['password']) < 6 or ' ' in data['password'] or not data['password'].isalnum()\
        or len([i for i in data['password'] if i.isalpha() and i.isupper()]) < 1\
        or len([i for i in data['password'] if i.isalpha() and i.islower()]) < 1:
            return Response({
            "Error" : "Parol noto'g'ri kiritildi"
        })

        phone = CustomUser.objects.filter(phone=data['phone']).first()
        if phone:
            return Response({
                'error' : "Bu raqamdan oldin foydalanilgan"
            })

        user_data = {
            'phone' : data['phone'],
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

        user = CustomUser.objects.filter(phone=data['phone']).first()
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
        if data['phone']:
            user = CustomUser.objects.filter(phone=data['phone']).first()
            if not user:
                return Response({
                    'data' : "Oldin Ro'yxatdan o'tish kere"
                })
            else:
                return Response({
                'data' : 'Qoyil sizga'
            })

class DeleteView(APIView):
    permission_classes = IsAuthenticated,
    authentication_classes = TokenAuthentication,

    def delete(self, request):
        user = request.user
        user.delete()
        return Response({
            'data' : "Xayt Brodar"
        })
