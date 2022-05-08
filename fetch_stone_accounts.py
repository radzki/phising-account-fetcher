#!/bin/python3

from time import sleep
import requests
import sys
from loguru import logger
from requests.structures import CaseInsensitiveDict
import re

def configure_logging():
    logger.remove()
    logger.add(sys.stdout, level="INFO")

def fetch_from_brshoping():
    url = "https://brshoping.com/api/user/recharge"

    headers = CaseInsensitiveDict()
    headers["User-Agent"] = "Mozilla/5.0 (X11; Ubuntu; Linux aarch64; rv:99.0) Gecko/20100101 Firefox/99.0"
    headers["Accept"] = "application/json, text/plain, */*"
    headers["Accept-Language"] = "en-US,en;q=0.5"
    headers["Accept-Encoding"] = "gzip, deflate, br"
    headers["Content-Type"] = "application/json; charset=UTF-8"
    headers["token"] = "eyJpdiI6Im9OOXlwckc1VHIxS1NxWlVEeG9MblE9PSIsInZhbHVlIjoiMXZkemVZT2liTEhibHdJVUliZU8vdFV0TVkrelZmK3BzYkZueEdmMjY2OD0iLCJtYWMiOiJjMjdlOTRkNTExYzYxZmFlYzhlYTFjM2RjZjZlNGY1ZjAwZmI1OTYxMjY0NmEyYTJjNjU1NDBlY2ZkZDdhZDk0In0="
    headers["language"] = "pt"
    headers["Origin"] = "https://brshoping.com"
    headers["Connection"] = "keep-alive"
    headers["Referer"] = "https://brshoping.com/"
    headers["Sec-Fetch-Dest"] = "empty"
    headers["Sec-Fetch-Mode"] = "cors"
    headers["Sec-Fetch-Site"] = "same-origin"
    headers["TE"] = "trailers"

    data = '{"p":"Sg61QCt2D6uIlua8ED98rh8Gh1uFTrAhdKsd9CAcndDmM3uMYTj4gQbeLwPdLB2GNnEKIOYoFIByJ8FVphiUFBaFVi39sjGR0A/I49I7swQ="}'


    resp = requests.post(url, headers=headers, data=data)

    data = resp.json()

    logger.debug(data)

    next_url = data.get('data').get('native_url')

    return next_url

def fetch_infro_from_bcb_dict(pix_key):
    # This must be implemented
    pass

def fetch_from_speed(url):
    if url is None:
        raise Exception("Unable to fetch url")
    logger.debug(f"Speedly URL: {url}")
    r = requests.get(url)
    data = r.text
    pix_key = re.search(r'qrcodeapp\.makeCode\(\"(.*?)\)', data).group(1)[:-1]
    return pix_key

def main_loop():
    configure_logging()
    wait_time = 10
    while True:
        try:
            logger.info(f"Trying to fetch uptaded PIX Key. Current timeout {wait_time} seconds.")
            pix_key = fetch_from_speed(fetch_from_brshoping())
            fetch_infro_from_bcb_dict(pix_key)
            logger.info(f"Latest PIX {pix_key}")
            wait_time = 10
        except Exception as e:
            logger.error(repr(e))
            if wait_time < 600:
                wait_time += 10
        
        sleep(wait_time)

main_loop()