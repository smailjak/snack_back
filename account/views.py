import jwt
import requests

import json
import re


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

                if account.password == data['password']:

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

class ActivateView(View):
    def get(self, request , uidb64, token):

        try:
            uid  = force_text(urlsafe_base64_decode(uidb64))
            account = Account.objects.get(pk=uid)

            if account_activation_token.check_token(account, token):
                account.is_active = True
                account.save()

                return redirect(EMAIL['REDIRECT_PAGE'])

            return JsonResponse({'message':'auth fail'} , status=200)

        except ValidationError:
            return JsonResponse({'message' : 'type_error'} , status=400)

        except KeyError:
            return JsonResponse({'message' : 'invalid_key'} , status=400)

class KakaoView(View):
    def post(self , request):
        access_token = request.headers.get('Authorization' , None)

        if access_token is None:
            return HttpResponse(status=400)

        try :
            url     = 'https://kapi.kakao.com/v2/user/me'
            headers = {
                "Host"          : "kapi.kakao.com",
                "Authorization" : f"Bearer{access_token}",
                "Content-type"  : "application/x-www-from-urlencoded;charset=utf-8"
            }

            req           = requests.get(url , headers =headers)
            req_json      = req.json()

            kakao_id      = req_json.get('id'            , None)
            kakao_account = req_json.get('kakao_account' , None)
            kakao_email   = kakao_account.get('email'    , None)

            if Account.objects.filter(email=kakao_email).exists():

                token = jwt.encode({'email' : kakao_email},
                                   SECRET_KEY['secret'],
                                   algorithm=ALGORITHM).decode("utf-8")

                return JsonResponse({"token" : token} , status = 200)

            Account(
                email    = kakao_email ,
                kakao_id = kakao_id,
            ).save()

        except KeyError:
            return JsonResponse({'error':'invalid_key'} , status=400)

        except jwt.DecodeError:
            return HttpResponse(status=400)

        except Exception as e:
            return JsonResponse({'error' : e} , status=400)

