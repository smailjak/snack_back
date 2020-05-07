import json

from django.views import View
from django.http  import HttpResponse, JsonResponse

from .models      import Account


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
            if Account.objects.filter(user_id = data['user_id']).exists(): # 존재하는 아이디이면
                user = Account.objects.get(user_id = data['user_id'])

                if user.password == data['password']:
                    return HttpResponse(status=200)

                return HttpResponse(status=401)

            return HttpResponse(status=400)

        except KeyError: # 존재하지 않는 아이디여서 keyerror 나면
            return JsonResponse({'message': 'INVALID_KEYS'}, status=400)
