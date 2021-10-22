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
    DraftMaker,
    DraftTour,
    DraftMaker_Drafttour,
    DraftCategory,
    DraftLanguage,
    DraftRegion,
)


class MakerApplyView(View):
    def post(self, request):
        try:
            data = json.loads(request.POST["data"])
            print(data)
            makernickname = data["makernickname"]
            makername = data["makername"]
            introduce = data["introduce"]
            language = data["language"]
            sns_address = data["sns_address"]
            sns_address_list = sns_address.split(",")
            language_list = language.split(",")
            status = data["status"]
            bank = data["bank"]
            account_number = int(data.get("account_number"))
            account_holder = data["account_holder"]
            productform = data["productform"]
            evidence_kind = data["evidence_kind"]
            region = data["region"]
            category = data["category"]
            tour_kind = data["tour"]
            limit_people = data["limit_people"]
            limit_load = data["limit_load"]
            PROFILE = request.FILES.get("profile")
            IDCARD = request.FILES.get("idcard")
            BANKBOOK = request.FILES.get("bankbook")
            EVIDENCE_IMAGE = request.FILES.get("evidence_image")
            # 사용언어 배열, sns 배열, 서비스지역, 카테고리, 증빙서류

            if PROFILE:
                uploaded_profile = PROFILE
                fs = FileSystemStorage(location="media/profile", base_url="profile")
                filename = fs.save(uploaded_profile.name, uploaded_profile)
                uploaded_profile_url = fs.url(filename)
                profile = uploaded_profile_url

            if IDCARD:
                uploaded_idcard = IDCARD
                fs = FileSystemStorage(
                    location="media/idcard", base_url="/media/idcard"
                )
                filename = fs.save(uploaded_idcard.name, uploaded_idcard)
                uploaded_idcard_url = fs.url(filename)
                idcard = uploaded_idcard_url

            if BANKBOOK:
                uploaded_bankbook_image = BANKBOOK
                fs = FileSystemStorage(
                    location="media/bankbook", base_url="/media/bankbook"
                )
                filename = fs.save(
                    uploaded_bankbook_image.name, uploaded_bankbook_image
                )
                uploaded_bankbook_image_url = fs.url(filename)
                bankbook = uploaded_bankbook_image_url

            if EVIDENCE_IMAGE:
                uploaded_evidence = EVIDENCE_IMAGE
                fs = FileSystemStorage(
                    location="media/evidence", base_url="/media/evidence"
                )
                filename = fs.save(uploaded_evidence.name, uploaded_evidence)
                uploaded_evidence_url = fs.url(filename)
                evidence = uploaded_evidence_url

            if not (makername and makernickname and PROFILE and introduce and IDCARD):
                return JsonResponse({"MESSAGE": "ENTER_REQUIRED_VALUES"}, status=400)

            maker = Maker.objects.create(
                user_id=1,
                makername=makername,
                makernickname=makernickname,
                introduce=introduce,
                profile=profile,
                idcard=idcard,
                bankbook_image=bankbook,
                status=status,
                bank=bank,
                account_number=account_number,
                account_holder=account_holder,
                productform=productform,
            )

            Sns.objects.create(
                maker_id=maker.id,
                address=[sns_address for sns_address in sns_address_list],
            )
            Language.objects.create(Language=[language for language in language_list])

            Evidence.objects.create(
                image=evidence, maker_id=maker.id, kind=evidence_kind
            )

            Region.objects.create(region=region)
            Category.objects.create(name=category)
            tour = Tour.objects.get(kind=tour_kind)
            Maker_tour.objects.create(
                limit_people=limit_people,
                limit_load=limit_load,
                tour_id=tour.id,
                maker_id=maker.id,
            )

            return JsonResponse({"MESSAGE": "CREATED"}, status=201)

        except KeyError:
            return JsonResponse({"MESSAGE": "KEY_ERROR"}, status=400)

        except ValueError:
            return JsonResponse({"MESSAGE": "VALUE_ERROR"}, status=400)


class DraftMakerView(View):
    def post(self, request):
        try:
            data = json.loads(request.POST["data"])
            makername = data["makername"]
            makernickname = data["makernickname"]
            introduce = data["introduce"]
            language = data["language"]
            sns_address = data["sns_address"]
            sns_address_list = sns_address.split(",")
            language_list = language.split(",")
            status = data["status"]
            bank = data["bank"]
            account_number = data["account_number"]
            account_holder = data["account_holder"]
            productform = data["productform"]
            evidence_kind = data["evidence_kind"]
            region = data["region"]
            category = data["category"]
            tour_kind = data["tour"]
            limit_people = data["limit_people"]
            limit_load = data["limit_load"]

            PROFILE = request.FILES.get("profile")
            IDCARD = request.FILES.get("idcard")
            BANKBOOK = request.FILES.get("bankbook")
            EVIDENCE_IMAGE = request.FILES.get("evidence_image")

            if PROFILE:
                uploaded_profile = PROFILE
                fs = FileSystemStorage(location="media/profile", base_url="profile")
                filename = fs.save(uploaded_profile.name, uploaded_profile)
                uploaded_profile_url = fs.url(filename)
                profile = uploaded_profile_url
            else:
                profile = None

            if IDCARD:
                uploaded_idcard = IDCARD
                fs = FileSystemStorage(
                    location="media/idcard", base_url="/media/idcard"
                )
                filename = fs.save(uploaded_idcard.name, uploaded_idcard)
                uploaded_idcard_url = fs.url(filename)
                idcard = uploaded_idcard_url
            else:
                idcard = None

            if BANKBOOK:
                uploaded_bankbook_image = BANKBOOK
                fs = FileSystemStorage(
                    location="media/bankbook", base_url="/media/bankbook"
                )
                filename = fs.save(
                    uploaded_bankbook_image.name, uploaded_bankbook_image
                )
                uploaded_bankbook_image_url = fs.url(filename)
                bankbook = uploaded_bankbook_image_url
            else:
                bankbook = None

            if EVIDENCE_IMAGE:
                uploaded_evidence = EVIDENCE_IMAGE
                fs = FileSystemStorage(
                    location="media/evidence", base_url="/media/evidence"
                )
                filename = fs.save(uploaded_evidence.name, uploaded_evidence)
                uploaded_evidence_url = fs.url(filename)
                evidence = uploaded_evidence_url
            else:
                evidence = None

            draftmaker = DraftMaker.objects.create(
                user_id=1,
                makername=makername,
                makernickname=makernickname,
                introduce=introduce,
                profile=profile,
                idcard=idcard,
                bankbook_image=bankbook,
                status=status,
                bank=bank,
                account_number=account_number,
                account_holder=account_holder,
                productform=productform,
            )

            Sns.objects.create(
                maker_id=draftmaker.id,
                address=[sns_address for sns_address in sns_address_list],
            )
            DraftLanguage.objects.create(
                Language=[language for language in language_list]
            )

            Evidence.objects.create(
                image=evidence, maker_id=draftmaker.id, kind=evidence_kind
            )

            DraftRegion.objects.create(region=region)
            DraftCategory.objects.create(name=category)
            if DraftTour.objects.filter(kind=tour_kind).exists():
                drafttour = DraftTour.objects.get(kind=tour_kind)
                DraftMaker_Drafttour.objects.create(
                    limit_people=limit_people,
                    limit_load=limit_load,
                    tour_id=drafttour.id,
                    draftmaker_id=draftmaker.id,
                )

            return JsonResponse(
                {
                    "MESSAGE": "DRAFT_CREATED",
                    "DraftMaker_ID": draftmaker.id,
                },
                status=201,
            )

        except KeyError:
            return JsonResponse({"MESSAGE": "KEY_ERROR"}, status=400)

        except ValueError:
            return JsonResponse({"MESSAGE": "VALUE_ERROR"}, status=400)
