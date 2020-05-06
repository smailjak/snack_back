import json
from django.views import View
from django.http import JsonResponse
from .models import Account


class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)
        print(request)
        print(request.body)
        Account(
            name = data['name'],
            user_id = data['user_id'],
            password = data['password'],
            email = data['email'],
            phone = data['phone']
        ).save()

        return JsonResponse({'message': '회원가입 완료'}, status=200)


class SignInView(View):
    def post(self, request):
        data = json.loads(request.body)

        if Account.objects.filter(user_id = data['user_id']).exists():
            user = Account.objects.get(user_id = data['user_id'])
            if user.password == data['password']:
                return JsonResponse({'message': f'{user.user_id}님 로그인 성공!'}, status=200)
            else:
                return JsonResponse({'message': '비밀번호가 틀렸어요'}, status=200)
        return JsonResponse({'message': '등록되지 않은 이메일 입니다.'}, status=200)