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

    image_links: List[str] = []
    for image in soup.find_all("img", class_="FFVAD"):
        image_links.append(image.get("src"))

    return random.choice(image_links)
