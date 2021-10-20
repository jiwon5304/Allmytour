import json, re, jwt, bcrypt

from django.views import View
from django.http import JsonResponse
from django.db.utils import DataError

from .models import User
from my_settings import SECRET_KEY, ALGORITHM
from .decorator import login_decorator


class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)
        email_format = re.compile("\w+[@]\w+[.]\w+")
        password_format = re.compile(
            "^(?=.*[a-zA-Z])(?=.*[0-9])(?=.*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]{8,20}$"
        )

        try:
            if not email_format.search(data["email"]):
                return JsonResponse({"message": "INVALID_EMAIL_FORMAT"}, status=400)
            if not password_format.match(data["password"]):
                return JsonResponse({"message": "INVALID_PASSWORD_FORMAT"}, status=400)

            if User.objects.filter(email=data["email"]).exists():
                return JsonResponse({"message": "USER_ALREADY_EXISTS"}, status=400)

            salt = bcrypt.gensalt()
            encoded_passwrod = data["password"].encode("utf-8")
            hashed_password = bcrypt.hashpw(encoded_passwrod, salt)
            decoded_password = hashed_password.decode("utf-8")

            User.objects.create(
                name=data["name"],
                password=decoded_password,
                email=data["email"],
                phone=data["phone"],
                agree_service=data["agree_service"],
                agree_maketing=data["agree_maketing"],
            )
            return JsonResponse({"message": "SUCCESS"}, status=201)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
        except DataError:
            return JsonResponse({"message": "DATA_TOO_LONG"}, status=400)


class LoginView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            if not User.objects.filter(email=data["email"]).exists():
                return JsonResponse({"MESSAGE": "INVALID_USER"}, status=401)

            user = User.objects.get(email=data["email"])

            if not bcrypt.checkpw(
                data["password"].encode("utf-8"), user.password.encode("utf-8")
            ):
                return JsonResponse({"MESSAGE": "PASSWORD ERROR"}, status=401)

            access_token = jwt.encode({"id": user.id}, SECRET_KEY, algorithm=ALGORITHM)
            return JsonResponse(
                {"MESSAGE": "SUCCESS", "token": access_token}, status=200
            )

        except KeyError:
            return JsonResponse({"MESSAGE": "KEY_ERROR"}, status=400)


class DoubleCheckEmailView(View):
    def post(self, request):
        data = json.loads(request.body)

        email_format = re.compile("\w+[@]\w+[.]\w+")

        try:
            if not email_format.search(data["email"]):
                return JsonResponse({"message": "INVALID_EMAIL_FORMAT"}, status=400)

            if User.objects.filter(email=data["email"]).exists():
                return JsonResponse({"message": "DUPLICATE_EMAIL"}, status=400)

            return JsonResponse({"message": "NOT_DUPLICATE_EMAIL"}, status=200)

        except KeyError:
            return JsonResponse({"MESSAGE": "KEY_ERROR"}, status=400)


class MypageView(View):
    @login_decorator
    def get(self, request):
        user = request.user

        result = {
            "email": user.email,
            "name": user.name,
            "phone": user.phone,
            "password": user.password,
            "is_maker": user.is_maker,
            "agree_service": user.agree_service,
            "agree_maketing": user.agree_marketing,
        }

        return JsonResponse({"Result": result}, status=200)
