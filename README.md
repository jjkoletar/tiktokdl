# tiktokdl
## A simple script for downloading original TikTok video files

This script is a Python module which allows you to download MP4 versions of TikTok videos.

### CLI Usage
On the CLI, invoke the script as such:
```
jjkoletar@The-Beast:~/tiktokdl/tiktokdl$ python3 tiktokdl.py https://www.tiktok.com/@youneszarou/video/6877109293657689345
Saved to 6877109293657689345.mp4
```

You can also pass -O to specify the output filename:
```
jjkoletar@The-Beast:~/tiktokdl/tiktokdl$ python3 tiktokdl.py https://www.tiktok.com/@youneszarou/video/6877109293657689345 -O video.mp4
Saved to video.mp4
```

### Library Usage
You can also import the `tiktokdl` module and call the function inside your own libraries:
```
jjkoletar@The-Beast:~/tiktokdl/tiktokdl$ python3
Python 3.8.5 (default, Jan 27 2021, 15:41:15) 
[GCC 9.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from tiktokdl import tiktokdl
>>> tiktokdl("https://www.tiktok.com/@youneszarou/video/6877109293657689345")
< ... long byte string ... >
```
This function will return the bytes of the video.
