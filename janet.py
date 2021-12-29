from bs4 import BeautifulSoup
from typing import List, Any
import os
import random
import asyncio


def get_random_image() -> str:

    f = open("./assets/xChocoBars_instagram.html", "r")
    instagram_html = f.read()
    f.close()

    soup: BeautifulSoup = BeautifulSoup(instagram_html, "html.parser")

    image_ids: List[str] = []

    for image in soup.find_all("div", class_="v1Nh3"):
        i = image.find_all("a")
        image_ids.append(i[0].get("href"))

    url = f"https://www.instagram.com{random.choice(image_ids)}media/?size=m"

    return url
