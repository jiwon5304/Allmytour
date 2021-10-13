import json
from django.http.response import HttpResponse, JsonResponse

# from django.shortcuts import render, render_to_response
from django.core.files.storage import FileSystemStorage
from django.views import View

from .models import Evidence, Maker


class MakerApplyView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            # makername = data['makername']
            # makernickname = data['makernickname']
            # introduce = data['introduce']
            # sns_address = data['address'] #다수
            # language = data['language'] #다수

            if request.FILES["profile"]:
                uploaded_profile = request.FILES["profile"]
                fs = FileSystemStorage()
                # location='media/profile', base_url='media/profile')
                filename = fs.save(uploaded_profile.name, uploaded_profile)
                uploaded_profile_url = fs.url(filename)
                print("==========================")
                print(type(uploaded_profile_url))
                print("==========================")

            if request.FILES["idcard"]:
                uploaded_idcard = request.FILES["idcard"]
                fs = FileSystemStorage()
                # location='media/profile', base_url='media/profile')
                filename = fs.save(uploaded_idcard.name, uploaded_idcard)
                uploaded_idcard_url = fs.url(filename)

            if request.FILES["bankbook_image"]:
                uploaded_bankbook_image = request.FILES["bankbook_image"]
                fs = FileSystemStorage()
                # location='media/profile', base_url='media/profile')
                filename = fs.save(
                    uploaded_bankbook_image.name, uploaded_bankbook_image
                )
                uploaded_bankbook_image_url = fs.url(filename)

            if request.FILES["evidence"]:
                uploaded_evidence = request.FILES["evidence"]
                fs = FileSystemStorage()
                # location='media/profile', base_url='media/profile')
                filename = fs.save(uploaded_evidence.name, uploaded_evidence)
                uploaded_evidence_url = fs.url(filename)

            Maker.objects.create(
                makername=data["makername"],
                makernickname=data["makernickname"],
                introduce=data["introduce"],
                sns_address=data["address"],  # 다수
                language=data["language"],  # 다수
                profile=uploaded_profile_url,
                idcard=uploaded_idcard_url,
                bankbook_image=uploaded_bankbook_image_url,
            )

            Evidence.objects.create(image=uploaded_evidence_url)

            return JsonResponse({"MESSAGE": "CREATED"}, status=201)

        except KeyError:
            return JsonResponse({"MESSAGE": "KEY_ERROR"}, status=400)
