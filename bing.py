import requests
import json
import os

base_url = "https://cn.bing.com"
dpilist = ["1366x768", "1920x1080", "1080x1920", "4K"]
base_path = os.getcwd()

def folder():
    if not os.path.exists(f"{base_path}/img"):
        os.mkdir(f"{base_path}/img")
    if not os.path.exists(f"{base_path}/img/1366x768"):
        os.mkdir(f"{base_path}/img/1366x768")
    if not os.path.exists(f"{base_path}/img/1920x1080"):
        os.mkdir(f"{base_path}/img/1920x1080")
    if not os.path.exists(f"{base_path}/img/1080x1920"):
        os.mkdir(f"{base_path}/img/1080x1920")
    if not os.path.exists(f"{base_path}/img/4K"):
        os.mkdir(f"{base_path}/img/4K")

def getBingImg():
    try:
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
        }
        response = requests.get(
            f"{base_url}/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=zh-CN",
            headers=headers,
            timeout=3,
        )
        response = json.loads(response.text)  # 转化为json
        imgList = []
        for item in response["images"]:
            imgList.append(
                {
                    "copyright": item["copyright"],  # 版权
                    "date": item["enddate"],
                    "1366x768": f"{base_url}{item['urlbase']}_1366x768.jpg",
                    "1920x1080": f"{base_url}{item['urlbase']}_1920x1080.jpg",
                    "1080x1920": f"{base_url}{item['urlbase']}_1080x1920.jpg",
                    "4K": f"{base_url}{item['urlbase']}_UHD.jpg",
                }
            )
        return imgList  # 返回一个数据数组
    except:
        return False
    
def save_img(url, path):
    img = requests.get(url, stream=True)
    if img.status_code == 200:
        with open(path, "wb") as f:
            f.write(img.content)
            print('Create Image Success!')
    else:
        print('Create Image Faild!')

def down_img(imglist):
    for item in imglist:
        img_date = item['date']
        name = item['copyright'].replace("/","_")
        for dpi in dpilist:
            print(f"下载{dpi}图片")
            save_img(item[dpi], f"{base_path}/img/{dpi}/{img_date}.jpg")
    open(f"{base_path}/{name}", 'a').close()

if __name__ == "__main__":
    folder()
    down_img(getBingImg())
