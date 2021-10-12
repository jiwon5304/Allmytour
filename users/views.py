import json, jwt, bcrypt

from django.views import View
from django.http import JsonResponse

from .models import User
from my_settings import SECRET_KEY


class SigninView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            if not User.objects.filter(email=data["email"]).exist():
                return JsonResponse({"MESSAGE": "INVALID_USER"}, status=401)

            user = User.objects.get(email=data["email"])

            if not bcrypt.checkpw(
                data["password"].encode("utf-8"), user.password.encode("utf-8")
            ):
                return JsonResponse({"MESSAGE": "PASSWORD ERROR"}, status=401)

            access_token = jwt.encode({"id": user.id}, SECRET_KEY, algorithm="HS256")
            return JsonResponse(
                {"MESSAGE": "SUCCESS", "token": access_token}, status=200
            )

        except KeyError:
            return JsonResponse({"MESSAGE": "KEY_ERROR"}, status=400)
