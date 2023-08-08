import os
import shutil
import re

from typing import Tuple

from linebot import LineBotApi
from linebot.models import TextSendMessage
from linebot.exceptions import LineBotApiError

import requests
import redis
from bs4 import BeautifulSoup



def push_chirashi():

    url, storeName, content = scraping()

    if is_updated(url):
        send_message(storeName, url)


def is_updated(url: str):
    updated: bool = False

    r = redis.from_url(os.environ.get("REDIS_URL"))
    url_old = r.get("url")

    if url_old is None:
        updated = True
    else:
        if url != url_old.decode("utf-8"):
            updated = True

    r.set("url", url)
    r.quit()

    return(updated)


def scraping() -> Tuple[str, str]:

    domain = 'https://sunbelx.com'
    url = f'{domain}/store/39'
    response = requests.get(url)
    soup = BeautifulSoup(response.text)
    title = soup.find("title")
    storename = re.search("^(.+店)",title.text).group()

    chirashi = [a for a in soup.find_all("a") if a.text == "PDF版チラシ"][0]

    url = domain + chirashi.get("href")
    r = requests.get(url)
    return (url, storename, r.content)

    # if os.path.exists("new.bin"):
    #     shutil.copy("new.bin","old.bin")


    # with open("old.bin","rb") as f:
    #     old = f.read

    # with open('new.bin', 'wb') as f:
    #     f.write(r.content)
    #     new = r.content

    isupdate = (old != new)

def send_message(storeName: str, url: str):
    token = os.environ.get("TOKEN")
    line_bot_api = LineBotApi(token)
    line_bot_api.broadcast(TextSendMessage(text = f"{storeName}のチラシが更新されました。"))
    line_bot_api.broadcast(TextSendMessage(text = url))

