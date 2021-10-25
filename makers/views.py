import json
import base64

from django.http.response import JsonResponse
from django.views import View

from django.core.files.storage import FileSystemStorage

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
    DraftEvidence,
)


class MakerApplyView(View):
    def post(self, request):
        try:
            data = json.loads(request.POST["data"])
            makernickname = data["makernickname"]
            makername = data["makername"]
            introduce = data["introduce"]
            languages = data["language"]
            sns_address_list = data["sns_address"]
            status = data["status"]
            bank = data["bank"]
            account_number = data.get("account_number")
            account_holder = data["account_holder"]
            productform = data["productform"]
            evidence_kind = data["evidence_kind"]
            regions = data["region"]
            categories = data["category"]
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

            language = Language.objects.create(
                Language=[language for language in languages]
            )
            maker.language.add(language)

            Sns.objects.create(
                maker_id=maker.id,
                address=[sns_address for sns_address in sns_address_list],
            )

            Evidence.objects.create(
                image=evidence, maker_id=maker.id, kind=evidence_kind
            )

            region = Region.objects.create(region=[region for region in regions])
            maker.region.add(region)

            category = Category.objects.create(name=[name for name in categories])
            maker.category.add(category)

            if Tour.objects.filter(kind=tour_kind).exists():
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
    def get(self, request):
        try:
            user = request.user
            maker_id = request.GET.get("id")

            if not maker_id:
                return JsonResponse({"message": "WRONG ID FORMAT"}, status=400)

            maker = DraftMaker.objects.get(id=maker_id, user_id=user)
            evidences = DraftEvidence.objects.select_related("maker").filter(
                maker=maker_id
            )

            result = {
                "makername": maker.makername,
                "makernickname": maker.makernickname,
                "profile": base64.encodebytes(
                    open(maker.profile.path, "rb").read()
                ).decode("utf-8"),
                "profile_name": maker.profile.name,
                "profile_url": maker.profile.url,
                "introduce": maker.introduce,
                "evidence": [
                    {
                        "evidence_kind": evidence.kind,
                        "evidence_image": base64.encodebytes(
                            open(evidence.image.path, "rb").read()
                        ).decode("utf-8"),
                        "evidence_name": evidence.image.name,
                        "evidence_url": evidence.image.url,
                    }
                    for evidence in evidences
                ],
                "sns": list(maker.sns.values_list("address", flat=True)),
                "language": list(maker.language.values_list("Language", flat=True)),
                "category": list(maker.category.values_list("name", flat=True)),
                "region": list(maker.region.values_list("region", flat=True)),
                "idcard": base64.encodebytes(
                    open(maker.idcard.path, "rb").read()
                ).decode("utf-8"),
                "idcard_name": maker.idcard.name,
                "idcard_url": maker.idcard.url,
                "bankbook": base64.encodebytes(
                    open(maker.bankbook_image.path, "rb").read()
                ).decode("utf-8"),
                "bankbook_name": maker.bankbook_image.name,
                "bankbook_url": maker.bankbook_image.url,
                "bank": maker.bank,
                "account_number": maker.account_number,
                "account_holder": maker.account_holder,
                "productform": maker.productform,
                "tour": list(maker.tour.values_list("kind", flat=True)),
            }

            if DraftMaker_Drafttour.objects.filter(
                maker_id=maker, tour_id__kind="차량투어"
            ).exists():
                tour = DraftMaker_Drafttour.objects.get(
                    maker_id=maker, tour_id__kind="차량투어"
                )
                tour_limit = {
                    "limit_people": tour.limit_people,
                    "limit_load": tour.limit_load,
                }
                result.update(tour_limit)

            return JsonResponse({"Message": result}, status=200)
        except DraftMaker.DoesNotExist:
            return JsonResponse({"Message": "MAKERS DOES NOT EXISTS"}, status=400)

    def post(self, request):
        try:
            data = json.loads(request.POST["data"])
            makernickname = data["makernickname"]
            makername = data["makername"]
            introduce = data["introduce"]
            languages = data["language"]
            sns_address_list = data["sns_address"]
            status = data["status"]
            bank = data["bank"]
            account_number = data.get("account_number")
            print(data)
            account_holder = data["account_holder"]
            productform = data["productform"]
            evidence_kind = data["evidence_kind"]
            regions = data["region"]
            categories = data["category"]
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
            draftlanguage = DraftLanguage.objects.create(
                Language=[language for language in languages]
            )
            draftmaker.language.add(draftlanguage)

            DraftEvidence.objects.create(
                image=evidence, maker_id=draftmaker.id, kind=evidence_kind
            )

            draftregion = DraftRegion.objects.create(
                region=[region for region in regions]
            )
            draftmaker.region.add(draftregion)

            draftcategory = DraftCategory.objects.create(
                name=[category for category in categories]
            )
            draftmaker.category.add(draftcategory)

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
                },
                status=201,
            )

        except KeyError:
            return JsonResponse({"MESSAGE": "KEY_ERROR"}, status=400)

        except ValueError:
            return JsonResponse({"MESSAGE": "VALUE_ERROR"}, status=400)


class MakerReviseView(View):
    def get(self, request):
        try:
            user = request.user
            maker_id = request.GET.get("id")

            if not maker_id:
                return JsonResponse({"message": "WRONG ID FORMAT"}, status=400)

            maker = Maker.objects.get(id=maker_id, user_id=user)
            evidences = Evidence.objects.select_related("maker").filter(maker=maker_id)

            result = {
                "makername": maker.makername,
                "makernickname": maker.makernickname,
                "profile": base64.encodebytes(
                    open(maker.profile.path, "rb").read()
                ).decode("utf-8"),
                "profile_name": maker.profile.name,
                "profile_url": maker.profile.url,
                "introduce": maker.introduce,
                "evidence": [
                    {
                        "evidence_kind": evidence.kind,
                        "evidence_image": base64.encodebytes(
                            open(evidence.image.path, "rb").read()
                        ).decode("utf-8"),
                        "evidence_name": evidence.image.name,
                        "evidence_url": evidence.image.url,
                    }
                    for evidence in evidences
                ],
                "sns": list(maker.sns.values_list("address", flat=True)),
                "language": list(maker.language.values_list("Language", flat=True)),
                "category": list(maker.category.values_list("name", flat=True)),
                "region": list(maker.region.values_list("region", flat=True)),
                "idcard": base64.encodebytes(
                    open(maker.idcard.path, "rb").read()
                ).decode("utf-8"),
                "idcard_name": maker.idcard.name,
                "idcard_url": maker.idcard.url,
                "bankbook": base64.encodebytes(
                    open(maker.bankbook_image.path, "rb").read()
                ).decode("utf-8"),
                "bankbook_name": maker.bankbook_image.name,
                "bankbook_url": maker.bankbook_image.url,
                "bank": maker.bank,
                "account_number": maker.account_number,
                "account_holder": maker.account_holder,
                "productform": maker.productform,
                "tour": list(maker.tour.values_list("kind", flat=True)),
            }

            if Maker_tour.objects.filter(maker_id=maker, tour_id__kind="차량투어").exists():
                tour = Maker_tour.objects.get(maker_id=maker, tour_id__kind="차량투어")
                tour_limit = {
                    "limit_people": tour.limit_people,
                    "limit_load": tour.limit_load,
                }
                result.update(tour_limit)

            return JsonResponse({"Message": result}, status=200)
        except Maker.DoesNotExist:
            return JsonResponse({"Message": "MAKERS DOES NOT EXISTS"}, status=400)

    def post(self, request):
        try:
            user = request.user
            data = json.loads(request.POST["data"])

            Maker.objects.get(id=data["id"]).delete()

            maker = Maker.objects.create(
                user_id=user,
                makername=data["makername"],
                makernickname=data["makernickname"],
                introduce=data["introduce"],
                bank=data["bank"],
                account_number=data["account_number"],
                account_holder=data["account_holder"],
                productform=data["productform"],
                profile=request.FILES["profile"],
                idcard=request.FILES["idcard"],
                bankbook_image=request.FILES["bankbook"],
            )
            print(request.FILES["profile"])

            for sns in data["sns"]:
                Sns.objects.create(
                    maker_id=maker.id,
                    address=sns["address"],
                )

            for evidence, image in zip(
                data["evidence"], request.FILES.getlist("evidence")
            ):
                Evidence.objects.create(
                    kind=evidence["kind"], maker_id=maker.id, image=image
                )

            for language in data["language"]:
                Language.objects.get_or_create(Language=language["language"])
                maker.language.add(
                    Language.objects.get(Language=language["language"]).id
                )

            for region in data["region"]:
                Region.objects.get_or_create(region=region["region"])
                maker.region.add(Region.objects.get(region=region["region"]).id)

            for category in data["category"]:
                Category.objects.get_or_create(name=category["category"])
                maker.category.add(Category.objects.get(name=category["category"]).id)

            if data["tour"] == "차량투어":
                Maker_tour.objects.create(
                    maker_id=maker.id,
                    tour_id=Tour.objects.get(kind=data["tour"]).id,
                    limit_people=data["limit_people"],
                    limit_load=data["limit_load"],
                )

            return JsonResponse({"Result": "SUCCESS"}, status=200)
        except KeyError:
            return JsonResponse({"Message": "KEY ERROR"}, status=400)
        except Language.DoesNotExist:
            return JsonResponse({"Message": "WRONG LANGUAGE"}, status=400)
        except Region.DoesNotExist:
            return JsonResponse({"Message": "WRONG REGION"}, status=400)
        except Category.DoesNotExist:
            return JsonResponse({"Message": "WRONG CATEGORY"}, status=400)
