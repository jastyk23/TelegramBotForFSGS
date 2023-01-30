from minio import Minio
import json, re


# Поиск и сбор станций в хранилище АПК
def apk_raw(opname, op_data, date):
    client = Minio(
                endpoint="10.20.19.72:9000",
                access_key="fsgs",
                secret_key="Htf53#cdAqDx",
                secure=False,
                region='eu-east-1'
            )

    pattern = r"_(?!{year})[a-zA-Z0-9]{{4}}_|[a-zA-Z0-9]{{4}}{year_day}_|_[a-zA-Z0-9]{{4}}{year_day}0|_[a-zA-Z0-9]{{4}}00|_(?!{year})[a-zA-Z0-9]{{3}}__|[a-zA-Z0-9]{{3}}_{year_day}_|_[a-zA-Z0-9]{{3}}_{year_day}0|_[a-zA-Z0-9]{{3}}_00"

    repl = {"year_day": date.strftime('%j'), "year": date.strftime('%Y')}
    pattern = pattern.format(**repl)

    op_list = []
    ispr_op_name = opname.replace(" ", "_")
    path = f"{date.year}/{date.strftime('%m')}/{date.strftime('%d')}/Оператор/{ispr_op_name}/необработанные_файлы/"
    bucket = client.list_objects(bucket_name="fsgs", prefix=path)
    for obj in bucket:
        name = "".join(re.findall(pattern, obj.object_name))
        op_list.append(name[1:5].upper())

    if len(op_list) != 0:
        op_list = list(set(op_list))
        op_list = op_list

    else:
        op_list = []

    return  op_list