import json
import logging
from pathlib import Path

from django.conf import settings
from django.db import transaction

from account.models import Province, Ward

logger = logging.getLogger()


@transaction.atomic
def refresh_vn_location_data(json_path: Path = settings.VN_LOCATION_RESOURCE_DIR):
    logger.info("Starting load data from %s", json_path.resolve())
    with open(json_path, mode="r", encoding="utf-8") as file:
        json_data = json.load(file)

    provinces = []
    wards = []
    for province_data in json_data:
        province = Province(
            name=province_data["Name"],
            name_en=province_data["NameEn"],
            full_name=province_data["FullName"],
            full_name_en=province_data["FullNameEn"],
        )
        for ward_data in province_data["Wards"]:
            ward = Ward(
                name=ward_data["Name"],
                name_en=ward_data["NameEn"],
                full_name=ward_data["FullName"],
                full_name_en=ward_data["FullNameEn"],
                province=province,
            )
            wards.append(ward)
        provinces.append(province)

    logger.info("Delete all Provinces")
    Province.objects.all().delete()

    logger.info("Delete all Wards")
    Ward.objects.all().delete()

    logger.info("Insert Province data")
    Province.objects.bulk_create(provinces)

    logger.info("Insert Ward data")
    Ward.objects.bulk_create(wards)
