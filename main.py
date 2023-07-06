import storage_mongodb
import vne
from datetime import datetime
import sys
import os

script_name = sys.argv[0]
args = sys.argv[1:]
repo = args[0] if len(args) > 0 else ""
url = args[1] if len(args) > 1 else ""

mongo_conn_str = os.getenv("MONGODB_CONN_STR", "")
mongo_db = os.getenv("MONGODB_DB", "")
if mongo_conn_str == "" or mongo_db == "":
    print(f"Please set environment variables MONGODB_CONN_STR and MONGODB_DB")
    exit(1)

with storage_mongodb.StorageMongoDb(mongo_conn_str, mongo_db) as storage:
    if (repo.upper() == "VNE" or repo.upper() == "VNEXPRESS") and url != "":
        cat_items = vne.fetch_vne_category(url)
        print(f"Repo: VNExpress / Time: {datetime.now()} / Category: {url} / Num items: {len(cat_items)}")
        for sitem in cat_items:
            print(f"{sitem.url} - {sitem.title}")
            storage.save(sitem, "dataset_news_title_summary")
            citem = vne.fetch_vne_article(sitem)
            print(f"\tNum paragraphs: {len(citem.paragraphs)}")
            storage.save(citem, "dataset_news_title_summary_content")
    else:
        print(f"Usage: python {script_name} <repo> <url>")
        print(f"Example: python {script_name} VNExpress https://vnexpress.net/khoa-hoc")
        exit(-1)
