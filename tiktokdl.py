import requests, json, bs4, argparse, sys


def tiktokdl(url) -> bytes:
    user_agent = (
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:87.0) Gecko/20100101 Firefox/87.0"
    )

    webpage = requests.get(url, headers={"User-Agent": user_agent})

    if not webpage.ok:
        raise Exception(f"Issue loading webpage: {webpage}")

    tt_webid_v2 = webpage.cookies["tt_webid_v2"]

    content = bs4.BeautifulSoup(webpage.content, "html.parser")
    next_data_maybe = content.find_all(id="__NEXT_DATA__")
    if len(next_data_maybe) != 1:
        raise Exception(
            "Couldn't find a single __NEXT_DATA__ element in the DOM. Are we getting blocked?"
        )

    next_data = json.loads(next_data_maybe[0].string)
    play_addr = next_data["props"]["pageProps"]["itemInfo"]["itemStruct"]["video"][
        "playAddr"
    ]

    video_headers = {
        "Accept": "video/webm,video/ogg,video/*;q=0.9,application/ogg;q=0.7,audio/*;q=0.6,*/*;q=0.5",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "Range": "bytes=0-",
        "Referer": "https://www.tiktok.com/",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:87.0) "
        "Gecko/20100101 Firefox/87.0",
    }

    video = requests.get(
        play_addr, headers=video_headers, cookies={"tt_webid_v2": tt_webid_v2}
    )
    if not video.ok:
        raise Exception(f"Uh oh, we didn't get the data back from the CDN. {video}")

    return video.content


def cli(url, output_path) -> None:
    video_content = tiktokdl(url)
    print("Saved to " + output_path)
    with open(output_path, "wb") as fd:
        fd.write(video_content)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Download MP4 versions of TikTok videos"
    )
    parser.add_argument(
        "url",
        help="Permalink URL of the TikTok, example: https://www.tiktok.com/@youneszarou/video/6877109293657689345",
    )
    parser.add_argument("-O", "--output-path", help="Output path for the video")
    args = parser.parse_args()

    if args.output_path:
        output_path = args.output_path
    else:
        url_parts = args.url.split("/")
        url_component = None
        while not url_component and url_parts:
            url_component = url_parts.pop()

        output_path = url_component + ".mp4"

    cli(args.url, output_path)
