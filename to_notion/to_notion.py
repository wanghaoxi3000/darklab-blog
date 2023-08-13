import glob
import io
import json
import os

import yaml
from dateutil.parser import parse
from md2notion.upload import upload
from notion.client import NotionClient
from notion.collection import NotionDate


def read_post_file(post_path):
    pathname = os.path.join(post_path, "**/*.md")

    index = 0
    bloglist = []
    for fp in glob.iglob(pathname, recursive=True):
        with open(fp, "r", encoding="utf-8") as mdFile:
            mdStr = mdFile.read()
            mdStr = mdStr.strip("-").strip()
            mdChunks = mdStr.split("---", 1)
            header = yaml.safe_load(mdChunks[0])

            slug = header["slug"].lower()
            content = mdChunks[1].lstrip("\n")
            summary = header.get("description")
            des_list = content.split("<!-- more -->")
            if len(des_list) > 1 and summary is None:
                summary = des_list[0].strip("\n")

            date = header.get("date")
            if isinstance(date, str):
                date = parse(date)

            content = content.replace("<!-- more -->", "", 1)

            page = {
                "filepath": fp,
                "title": header["title"],
                "slug": slug,
                "category": header.get("categories"),
                "tags": header.get("tags", []),
                "summary": summary,
                # "date": date.strftime("%Y-%m-%d %H:%M:%S"),
                "date": date.date(),
                "content": content,
            }

        bloglist.append(page)
        index += 1

    bloglist.sort(key=lambda x: x["date"], reverse=True)
    return bloglist


def upload_notion(bloglist: list):
    token_v2 = ""
    collection_view_id = "https://www.notion.so/xxxxx"

    client = NotionClient(
        token_v2
    )
    cv = client.get_collection_view(
        collection_view_id
    )

    with open('record.json', 'r') as f:
        record = json.load(f)

    index = 1
    for page in bloglist:
        if page["slug"] in record["imported"]:
            print("skip article", page.get("title"))
            index += 1
            continue

        print(f"{index}/{len(bloglist)}:Uploading {page.get('filepath')}")

        row = cv.collection.add_row()
        row.type = "Post"
        row.date = NotionDate(page["date"])
        row.title = page["title"]
        row.slug = page["slug"]
        row.category = page["category"][0]
        if page["tags"]:
            row.tags = page["tags"]
        row.status = "Draft"
        if page.get("summary"):
            row.summary = page["summary"]

        mdFile = io.StringIO(page.get("content"))
        mdFile.__dict__["name"] = page["filepath"]

        try:
            upload(mdFile, row)
        except Exception as e:
            print(e)
            with open('record.json', 'w') as f:
                json.dump(record, f, ensure_ascii=False, indent=4)
            exit(1)

        index += 1
        record["imported"].append(page["slug"])


if __name__ == "__main__":
    bloglist = read_post_file("content/posts")
    upload_notion(bloglist)
