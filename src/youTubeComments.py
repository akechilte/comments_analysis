from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import  pandas as pd
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
            if response['items'][0]['statistics']['viewCount'] > '100000':
                videoId.append(search_result['id']['videoId'])
    print(videoId)
    return videoId


def geo_query(video_id):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)

    video_response = youtube.videos().list(
        id=video_id,
        part='snippet, recordingDetails, statistics'

    ).execute()

    return video_response



def get_comment_threads(searchName):
    outputDF = pd.DataFrame([])
    videoIds= youtube_search(searchName)
    for id in videoIds:
        youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                        developerKey=DEVELOPER_KEY)
        results = youtube.commentThreads().list(
            part="snippet",
            videoId=id,
            textFormat="plainText"
        ).execute()

        for item in results["items"]:
            comment = item["snippet"]["topLevelComment"]
            author = comment["snippet"]["authorDisplayName"]
            createdTime = comment["snippet"]["publishedAt"]
            text = comment["snippet"]["textDisplay"]
            #print("Comment by %s: at %s: %s" % (author, createdTime,text))
            outputDF = outputDF.append(pd.DataFrame({'videoID': id, 'CreateTimeStamp': createdTime, 'Comment': text}, index=[0]), ignore_index=True)
    #print(outputDF)
    return outputDF


def main():
    SearchString = 'Eminem - Not Afraid'
    comments = get_comment_threads(searchName=SearchString)
    writer = ExcelWriter('Comments.xlsx')
    comments.to_excel(writer, 'Sheet1')
    writer.save()
    #youtube_search(q='the family vacation sit')
    #print(comments)

#The tonight show
#samsung vr headset
#

if __name__ == "__main__":
    main()
