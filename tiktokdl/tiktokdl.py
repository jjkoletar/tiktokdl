import requests
import json
import bs4
import sys
import io
from dataclasses import dataclass


@dataclass
class TikTokAuthor:
    id: int
    unique_id: str
    nickname: str
    avatar: str

@dataclass
class TikTokVideo:
    id: int
    permalink: str
    cdn_link: str
    duration: int
    cover: str
    desc: str

@dataclass
class DownloadedTikTok:
    content: str
    datatype: str
    extension: str


class TikTok:
    def __init__(self, url):
        try:
            self.get_meta(url)
        except Exception as e:
            raise(e)
    
    def get_meta(self, url):
        headers = {
        "user-agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/86.0.4240.111 Safari/537.36")
        }

        response = requests.get(url, headers=headers)
        self.tt_webid_v2 = response.cookies["tt_webid_v2"]

        if not response.ok:
            raise Exception(f"Issue loading webpage: {response}")

        content = bs4.BeautifulSoup(response.content, "html.parser")
        data = content.find_all(id="__NEXT_DATA__")

        if not data:
            raise Exception(
                "Couldn't find a single __NEXT_DATA__ element in the DOM. Are we getting blocked?"
            )

        data = json.loads(data[0].string)

        #Assume data is the video we want
        item_struct = data["props"]["pageProps"]["itemInfo"]["itemStruct"]
        video_struct = item_struct["video"]
        self.video = TikTokVideo(
            id = video_struct["id"],
            permalink = url,
            cdn_link = video_struct["playAddr"],
            duration = video_struct["duration"],
            cover = video_struct["cover"],
            desc = item_struct["desc"],

        )
        author_struct = item_struct["author"]
        self.author = TikTokAuthor(
            id = author_struct["id"],
            unique_id = author_struct["uniqueId"],
            nickname = author_struct["nickname"],
            avatar = author_struct["avatarThumb"],
        )

    def download(self, fp=None):
        headers = {
        "Accept": "video/webm,video/ogg,video/*;q=0.9,application/ogg;q=0.7,audio/*;q=0.6,*/*;q=0.5",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "Range": "bytes=0-",
        "Referer": "https://www.tiktok.com/",
        "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/86.0.4240.111 Safari/537.36"),
        }
        video = requests.get(
            self.video.permalink, headers=headers, cookies={"tt_webid_v2": self.tt_webid_v2}
        )
        if not video.ok:
            raise Exception(f"Uh oh, we didn't get the data back from the CDN. {video}")

        if fp:
            if not hasattr(fp, "write"):
                raise Exception(f"Variable `fp` did not have attribute \"write\"")

            fp.write(video.content)
        return video.content
