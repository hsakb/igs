import os
import datetime

path = "crawler/data"
now = datetime.datetime.now()

for file_name in os.listdir(path):
    file_path = os.path.join(path, file_name)
    if os.path.isfile(file_path):
        file_date = datetime.datetime.strptime(file_name, "%Y年%m月%d日.json")
        if (now - file_date).days > 7:
            os.remove(file_path)
