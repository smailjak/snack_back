import bcrypt
import jwt
import requests

import json


from django.views           import View
from django.http            import HttpResponse, JsonResponse

from .models                import Account
from .utils                 import login_check
from snack_back.my_settings import SECRET_KEY , ALGORITHM

class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            if Account.objects.filter(user_id = data['user_id']).exists():  # 존재하는 유저아이디인지 확인
                return HttpResponse(status=400)

            Account(
                name     = data['name'],
                user_id  = data['user_id'],
                password = data['password'],
                email    = data['email'],
                phone    = data['phone']
            ).save()

            return HttpResponse(status=200) # 회원가입 완료

        except KeyError:
            return JsonResponse({'message': 'INVALID_KEY'}, status = 400)

class SignInView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            if Account.objects.filter(user_id = data['user_id']).exists():
                account = Account.objects.get(user_id = data['user_id'])

                if account.password == data['password']:
                    token = jwt.encode({"user":account.id} , SECRET_KEY['secret'] , algorithm = ALGORITHM)

                    return JsonResponse({"token":token.decode('utf-8')} , status=200)

                return HttpResponse(status=401)

            return HttpResponse(status=400)

        except KeyError:
            return JsonResponse({'message': 'INVALID_KEYS'}, status=400)

class ProfileView(View):
    @login_check
    def get(self , request):
        account_data = (Account.
                        objects.
                        filter(user_id = request.
                                       account.
                                       user_id).values())

        return JsonResponse({'data':list(account_data)},status=200)

    @login_check
    def post(self , request):
        data     = json.loads(request.body)
        account  = Account.objects.get(user_id = request.account.user_id)

        try :
            if Account.objects.filter(user_id = account.user_id):
                if bcrypt.checkpw(data['password'].encode('utf-8') ,
                                  account.password.encode('utf-8')):

                    account.update(
                        name    = data['name'],
                        user_id = data['user_id'],
                        email   = data['email'],
                        gender  = data['gender'],
                        post    = data['post'],
                    )

                    return HttpResponse(status=200)

        except KeyError:
            return JsonResponse({'message':'INVALID_KEY'},status=400)

        except ValueError:
            return HttpResponse(status=400)

        except Exception as e:
            return JsonResponse({'message':e} , status=400)
