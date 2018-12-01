from apiclient.discovery import build
from oauth2client.tools import argparser
import  pandas as pd
import sys
import string
import re
from sys import argv
# DF TO EXCEL
from pandas import ExcelWriter

DEVELOPER_KEY = ""
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"




def youtube_search(q, max_results=50, order="relevance", token=None, location=None, location_radius=None):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

    search_response = youtube.search().list(
        q=q,
        type="video",
        pageToken=token,
        order=order,
        part="id,snippet",  # Part signifies the different types of data you want
        maxResults=max_results,
        location=location,
        locationRadius=location_radius).execute()
    videoId = []

    for search_result in search_response.get("items", []):
        # pprint.pprint(search_result)


        if search_result["id"]["kind"] == "youtube#video":
            response = youtube.videos().list(
                part='statistics, snippet',
                id=search_result['id']['videoId']).execute()
            if response['items'][0]['statistics']['viewCount'] > '1000000':
                videoId.append(search_result['id']['videoId'])
    print(len(videoId))
    return videoId


def get_comment_threads(searchName):
    outputDF = pd.DataFrame([])
    videoIds= youtube_search(searchName)
    #videoIds = ['PYN4H0JXBJc']
    for video_id in videoIds:
        youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                        developerKey=DEVELOPER_KEY)
        results = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            textFormat="plainText"
        ).execute()

        for item in results["items"]:
            comment = item["snippet"]["topLevelComment"]

            createdTime = comment["snippet"]["publishedAt"]
            text = comment["snippet"]["textDisplay"]
            cleanText = cleanComment(text)
            # print("Comment by %s: at %s: %s" % (author, createdTime,text))
            outputDF=outputDF.append(pd.DataFrame({'videoID': video_id, 'CreateTimeStamp': createdTime, 'Comment': cleanText, 'Type': 'Comment'}, index=[0]),ignore_index=True)

        for item1 in results["items"]:
            results1 = youtube.comments().list(
                part="snippet",
                parentId=item1['id'],
                textFormat="plainText"
            ).execute()

            for item2 in results1["items"]:
                text1 = item2["snippet"]["textDisplay"]
                cleanText1 = cleanComment(text1)
                createdTime1 = item2["snippet"]["publishedAt"]
                outputDF=outputDF.append(pd.DataFrame({'videoID': video_id, 'CreateTimeStamp': createdTime1, 'Comment': cleanText1, 'Type': 'Reply'}, index=[0]),ignore_index=True)
        print(video_id)
    return outputDF

def cleanComment(text):
    text = text.lower()
    text = re.sub(r'https?:\/\/.\/\w', '', text)
    text = re.sub('@[^\s]+','',text)
    text = re.sub(r'\&\w*;', '', text)
    text = re.sub(r'\$\w*', '', text)
    text = re.sub(r'#\w*', '', text)
    text = re.sub(r'\b\w{1,2}\b', '', text)
    text = re.sub(r'\s\s+', ' ', text)
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r'\r', ' ', text)
    text = ''.join(r for r in text if r <= '\uFFFF')
    return text

def main():
    SearchString = sys.argv[1]
    #SearchString = 'Samsung VR HeadSet'
    comments = get_comment_threads(searchName=SearchString)
    comments.to_csv("SamsungVRHeadSet.csv", sep='\t', index=False)


if __name__ == "__main__":
    main()
