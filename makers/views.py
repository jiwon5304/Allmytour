import json, base64
from os import sched_getscheduler
from django.http.response import HttpResponse, JsonResponse

# from django.shortcuts import render, render_to_response
from django.core.files.storage import FileSystemStorage
from django.views import View
from django.http import FileResponse

from .models import (
    Category,
    Evidence,
    Maker,
    Maker_tour,
    Region,
    Sns,
    Language,
    Tour,
    Available_schedule,
    Available_service,
)


class MakerApplyView(View):
    def post(self, request):
        try:
            data = json.loads(request.POST["data"])
            makername = data["makername"]
            # makernickname = data["makernickname"]
            # introduce = data["introduce"]

            # sns_address = data["address"]
            # language = data["language"]
            # snskind = data["snskind"]
            # sns_address_list = sns_address.split(",")
            # language_list = language.split(",")

            if request.FILES["profile"]:
                uploaded_profile = request.FILES["profile"]
                fs = FileSystemStorage(location="media/profile", base_url="profile")
                filename = fs.save(uploaded_profile.name, uploaded_profile)
                uploaded_profile_url = fs.url(filename)
                profile = uploaded_profile_url

                # if request.FILES["idcard"]:
                #     uploaded_idcard = request.FILES["idcard"]
                #     fs = FileSystemStorage(
                #         location="media/idcard", base_url="/media/idcard"
                #     )
                #     filename = fs.save(uploaded_idcard.name, uploaded_idcard)
                #     uploaded_idcard_url = fs.url(filename)
                #     idcard = uploaded_idcard_url

                # if request.FILES["bankbook_image"]:
                #     uploaded_bankbook_image = request.FILES["bankbook_image"]
                #     fs = FileSystemStorage(
                #         location="media/bankbook", base_url="/media/bankbook"
                #     )
                #     filename = fs.save(
                #         uploaded_bankbook_image.name, uploaded_bankbook_image
                #     )
                #     uploaded_bankbook_image_url = fs.url(filename)
                #     bankbook = uploaded_bankbook_image_url

                # if request.FILES["evidence"]:
                #     uploaded_evidence = request.FILES["evidence"]
                #     fs = FileSystemStorage(
                #         location="media/evidence", base_url="/media/evidence"
                #     )
                #     filename = fs.save(uploaded_evidence.name, uploaded_evidence)
                #     uploaded_evidence_url = fs.url(filename)
                #     evidence = uploaded_evidence_url

                # if data["status"] == "임시저장":
                #     Maker.objects.create(
                #         user_id=1,
                #         makername=makername,
                #         makernickname=makernickname,
                #         introduce=introduce,
                #         profile=profile,
                #         idcard=idcard,
                #         bankbook_image=bankbook,
                #         status=data["status"],
                #         # is_draft = data["is_draft"], # 필드값 추가해야할 듯?
                #         bank=data["bank"],
                #         account_number=data["account_number"],
                #         account_holder=data["account_holder"],
                #         productform=data["productform"],
                #         have_car=data["have_car"],
                #         passenger_limit=data["passenger_limit"],
                #     )

                # # 필수: makername, makernickname, profile, introduce, idcard
                # if (
                #     data["status"] == "제출하기"
                #     and makername
                #     and makernickname
                #     and profile
                #     and introduce
                #     and idcard
                # ):
                Maker.objects.create(
                    user_id=1,
                    makername=makername,
                    # makernickname=makernickname,
                    # introduce=introduce,
                    profile=profile,
                    # idcard=idcard,
                    # bankbook_image=bankbook,
                    # status=data["status"],
                    # # is_draft = data["is_draft"], # 필드값 추가해야할 듯?
                    # bank=data["bank"],
                    # account_number=data["account_number"],
                    # account_holder=data["account_holder"],
                    # productform=data["productform"],
                    # have_car=data["have_car"],
                    # passenger_limit=data["passenger_limit"],
                )

            maker = Maker.objects.last()
            url = Maker.objects.get(id=maker.id).profile.url
            name = Maker.objects.get(id=maker.id).profile.path
            img = open(name, "rb")
            response = base64.encodebytes(img.read()).decode("utf-8")

            # Sns.objects.create(
            #     maker_id=maker.id,
            #     address=[sns_address for sns_address in sns_address_list],
            #     kind=snskind,
            # )
            # Language.objects.create(Language=[language for language in language_list])

            # Evidence.objects.create(
            #     image=evidence, maker_id=maker.id, kind=data["kind"]
            # )

            # Region.objects.create(region=data["region"])
            # Category.objects.create(name=data["category"])
            # Tour.objects.create(kind=data["tour"])  # DB에 종류만 저장해두면 될듯?
            # tour = Tour.objects.get(kind=data["tour"])
            # Maker_tour.objects.create(
            #     limit_people=data["limit_people"],
            #     limit_load=data["limit_load"],
            #     tour_id=tour.id,
            #     maker_id=maker.id,
            # )
            # Available_schedule.objects.create(schedule=data["schedule"])
            # Available_service.objects.create(service=data["service"])

            return JsonResponse(
                {"MESSAGE": "CREATED", "URL": url, "RESPONSE": response}, status=201
            )

        except KeyError:
            return JsonResponse({"MESSAGE": "KEY_ERROR"}, status=400)

        except ValueError:
            return JsonResponse({"MESSAGE": "VALUE_ERROR"}, status=400)
