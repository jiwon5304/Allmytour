import json
import os
import base64

from django.http.response import JsonResponse
from django.views import View
from .models import Category, Evidence, Language, Maker, Maker_tour, Region, Sns, Tour


class MakerReviseView(View):
    def get(self, request):
        try:
            user = request.user
            maker_id = request.GET.get("id")

            if not maker_id:
                return JsonResponse({"message": "WRONG ID FORMAT"}, status=400)

            maker = Maker.objects.get(id=maker_id, user_id=1)
            evidences = Evidence.objects.select_related("maker").filter(maker=maker_id)
            snses = Sns.objects.select_related("maker").filter(maker=maker_id)

            result = {
                "makername": maker.makername,
                "makernickname": maker.makernickname,
                "profile": base64.encodebytes(
                    open(maker.profile.path, "rb").read()
                ).decode("utf-8"),
                "introduce": maker.introduce,
                "evidence": [
                    {
                        "evidence_kind": evidence.kind,
                        "evidence_image": base64.encodebytes(
                            open(evidence.image.path, "rb").read()
                        ).decode("utf-8"),
                        "evidence_size": evidence.image.size,
                        "evidence_name": evidence.image.name,
                    }
                    for evidence in evidences
                ],
                "sns": [
                    {"sns_kind": sns.kind, "sns_address": sns.address} for sns in snses
                ],
                "language": list(maker.language.values_list("Language", flat=True)),
                "category": list(maker.category.values_list("name", flat=True)),
                "region": list(maker.region.values_list("region", flat=True)),
                "idcard": base64.encodebytes(
                    open(maker.idcard.path, "rb").read()
                ).decode("utf-8"),
                "bankbook": base64.encodebytes(
                    open(maker.bankbook_image.path, "rb").read()
                ).decode("utf-8"),
                "bank": maker.bank,
                "account_number": maker.account_number,
                "account_holder": maker.account_holder,
                "productform": maker.productform,
                "tour": list(maker.tour.values_list("kind", flat=True)),
            }

            if Maker_tour.objects.filter(
                maker_id=maker, tour_id__kind="차량 투어"
            ).exists():
                tour = Maker_tour.objects.get(maker_id=maker, tour_id__kind="차량 투어")
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
            # user = request.user
            data = json.loads(request.POST["data"])

            for i in data:
                print(i)
                print("============")
            # Maker.objects.get(id=data[id]).delete()

            maker = Maker.objects.create(
                user_id=1,
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
                    kind=sns["kind"],
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
                maker.language.add(
                    Language.objects.get(Language=language["language"]).id
                )

            for region in data["region"]:
                maker.region.add(Region.objects.get(region=region["region"]).id)

            for category in data["category"]:
                maker.category.add(Category.objects.get(name=category["category"]).id)

            if data["tour"] == "차량 투어":
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
