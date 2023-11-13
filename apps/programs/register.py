from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json
from ast import keyword
import re

DEVELOPER_KEY = "AIzaSyAX_Q6kIbXlUuV6BIwfjaA5IZipMhchWn8"
DEVELOPER_KEY2 = "AIzaSyC6VAjJ_pxJ9MwFKzB93o55r0y1FFiRa-4"

#Youtubeapiの基本情報
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey = DEVELOPER_KEY,  cache_discovery=False)

# チャンネル情報をもらってくる(name id icon)
def GetChannelInfo(url):
    ch_info = []
    try:
        respond = youtube.search().list(
        part ="snippet",
        type = "channel",
        q = url,
        maxResults = 1
    ).execute()
    except HttpError:
            print("request was denied")
    #name
    for item in respond['items']:
        snippet = item['snippet']
        name = snippet['title']
    ch_info.append(name)
    #id
    for item in respond['items']:
        snippet = item['snippet']
        id = snippet['channelId']
    ch_info.append(id)
    #icon
    for item in respond['items']:
        snippet = item['snippet']
        thumbnails = snippet['thumbnails']
        thumbnail = thumbnails['default']
        icon = thumbnail['url']
    ch_info.append(icon)
    return ch_info

#Get the playlist with channel's all video 
def GetPlaylistId(ch_id):
    try:
        respond = youtube.channels().list(
        part ="contentDetails",
        id = ch_id,
        maxResults = 1
    ).execute()
    except HttpError:
        print("request was denied")
    print(json.dumps(respond, indent=4, ensure_ascii=False))
    for item in respond['items']:
        contentDetail = item['contentDetails']
        relatedPlaylists = contentDetail['relatedPlaylists']
        playlist_id = relatedPlaylists['uploads']
    return playlist_id

def ChannelRegestar(url):
    info = GetChannelInfo(url)
    info.append(GetPlaylistId(url))
    RecordInfo(info)