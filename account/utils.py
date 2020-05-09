import jwt

from .models                import Account
from snack_back.my_settings import ALGORITHM, SECRET_KEY
from django.http            import JsonResponse


def login_check(func):
    def wrapper(self, request, *args, **kwargs):

        try:
            auth_token   = request.headers.get('Authorization', None)
            payload      = jwt.decode(auth_token,
                                      SECRET_KEY['secret'],
                                      algorithms = ALGORITHM)

            account      = User.objects.get(id = payload["id"])
            request.user = account

            return func(self, request, *args, **kwargs)

        except User.DoesNotExist:
            return JsonResponse({'message': 'INVALID_USER'}, status=401)

        except KeyError:
            return JsonResponse({'message': 'INVALID'}, status=400)

        except jwt.DecodeError:
            return JsonResponse({'message': 'INVALID TOKEN'}, status=401)

    return wrapper
