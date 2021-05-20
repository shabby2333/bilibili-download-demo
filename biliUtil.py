import requests
import json
import subprocess
import os

GET_VIDEO_LIST_URL = "https://api.bilibili.com/x/space/arc/search"
GET_VIDEO_INFO_URL = "https://api.bilibili.com/x/web-interface/view"
GET_VIDEO_DOENLOAD_URL = "https://api.bilibili.com/x/player/playurl"

def getVideos(mid, page):
    videoList = []
    response = requests.get(GET_VIDEO_LIST_URL,
                            {
                                "mid": mid,
                                "ps": 30,
                                "tid": 0,
                                "pn": page,
                                "keyword": "",
                                "order": "pubdate"
                            }).json()
    # print(response)
    if response['status'] == True:
        datas = response['data']['list']['vlist']
        for data in datas:
            videoList.append(data['aid'])
    return videoList


def getVideoList(mid, page_num):
    list = []
    for page in range(1, page_num+1):
        # print(page)
        videos = getVideos(mid, page)
        for video in videos:
            list.append(video)
    return list


def getVideoPageNum(mid):
    response = requests.get(GET_VIDEO_LIST_URL,
                            {
                                "mid": mid,
                                "pagesize": 30,
                                "tid": 0,
                                "page": 1,
                                "keyword": "",
                                "order": "pubdate"
                            }).json()
    return response['data']['pages']


def getVideoPages(aid):
    response = requests.get(GET_VIDEO_INFO_URL, {
        "aid": aid
    }).json()
    # print(response)
    if response['code'] == 0:
        return response['data']


def getDownloadUrl(aid, cid, qn=80):
    respone = requests.get(GET_VIDEO_DOENLOAD_URL, {
        'avid': aid,
        'cid': cid,
        'qn': 80,
        'otype': 'json',
        'fnver':0,
        'fnval':16
    }).json()
    if respone['code'] == 0:
        #print(respone)
        return respone['data']['dash']['video']

def downloadVideo(aid,url,title):
    referer = 'https://www.bilibili.com/video/av'+str(aid)
    downShell = './aria2/aria2c '+' -s 5 -o\'files/'+title+'.flv\' --referer='+ referer+' \'' + url+ '\''
    subprocess.Popen([r'powershell',downShell])

if __name__ == "__main__":
    # Change your bilibili space code here
    print("=== 写这段代码的时候，只有上帝和我知道它是干嘛的  ===")
    print("=== 现在，只有上帝知道 ===")
    print("=== 希望您用的时候不要踩坑，虽然不可能 ===")
    print("")
    mid = 180399349
    print("=== your space number is "+str(mid)+" ===")
    os.system('pause')
    

    pageNum = getVideoPageNum(mid)
    print("===get ", pageNum, " pages of videos===")
    videoList = getVideoList(mid, pageNum)
    # print(videoList)
    lenV = len(videoList)

    for i in range(0, lenV):
        video = getVideoPages(videoList[i])
        title = video['title']
        aid = videoList[i]
        pages = video['pages']
        print("===downloading video " + str(i+1) +' of ' + str(lenV) + "===" )

        for i in range(0,len(pages)-1):
            url = getDownloadUrl(aid, pages[i]['cid'])
            downloadVideo(aid,url[len(url)-1]['baseUrl'],title+'-P'+str(i))

    print("===all videos downloaded~~~===")
