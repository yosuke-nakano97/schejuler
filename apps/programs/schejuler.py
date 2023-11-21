from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime, timedelta
import os
import json
import re
import csv

#Youtubeの基本情報
DEVELOPER_KEY = "AIzaSyAX_Q6kIbXlUuV6BIwfjaA5IZipMhchWn8"
DEVELOPER_KEY2 = "AIzaSyC6VAjJ_pxJ9MwFKzB93o55r0y1FFiRa-4"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey = DEVELOPER_KEY2,  cache_discovery=False)

def FindId(url):
    respond = youtube.search().list(

        part ="id",
        type = "channel",
        q = url,
        maxResults = 1
    ).execute()
    #print(str(respond))
    #print(json.dumps(respond, indent=4, ensure_ascii=False))
    #print("/////////////////////////////////////////////////")
    channel_id = re.findall("Id': '(.+)'",str(respond))
    #print(channel_id[0])
    return channel_id[0]

def FindChannelIcon(id):
    respond = youtube.search().list(
        part = "snippet",
        type = "channel",
        channelId = str(id),
        maxResults = 1

    ).execute()
    #print(str(respond))
    #print(json.dumps(respond, indent=4, ensure_ascii=False))
    #print("/////////////////////////////////////////////////")
    channel_icon = re.findall("default': {'url': '(.+)'}, 'medium",str(respond))
    #print(channel_icon[0])
    return channel_icon[0]

def ChannelResister(url, name):
    channel_id = FindId(url)
    channel_icon = FindChannelIcon(channel_id)
    try:
        with open(pathcsv, mode = "a") as f:
            f.write(f"{name},{url},{channel_id},{channel_icon}\n")
            #print(name)
            #print(url)
             #print(channnel_id)
    except FileNotFoundError:
    	print("file not exist")


def GetStreamSchejule():
    s=""

def GetStreamInfo():
    a=""

def MakeInfoList():
    try:
        with open(pathcsv) as f:
            reader = csv.reader(f)
            l = [row for row in reader]
            print(l)
    except FileNotFoundError:
        print("file not exist")
        


           




sample_url = "https://www.youtube.com/@virtual_kaf"
name = "kaf"

#ChannelResister(sample_url,name)
MakeInfoList() 