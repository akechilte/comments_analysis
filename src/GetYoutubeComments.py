from apiclient.discovery import build
from oauth2client.tools import argparser
import pandas as pd
import sys
import string
import re
from sys import argv
# DF TO EXCEL
from pandas import ExcelWriter

YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


def youtube_search(q, developer_key, max_results, order="relevance", token=None, location=None, location_radius=None):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=developer_key)

    search_response = youtube.search().list(
        q=q,
        type="video",
        pageToken=token,
        order=order,
        part="id,snippet",  # Part signifies the different types of data you want
        maxResults=max_results,
        location=location,
        locationRadius=location_radius).execute()
    videoId = {}

    for search_result in search_response.get("items", []):
        # pprint.pprint(search_result)


        if search_result["id"]["kind"] == "youtube#video":
            response = youtube.videos().list(
                part='statistics, snippet',
                id=search_result['id']['videoId']).execute()
            if response['items'][0]['statistics']['viewCount'] > '1000000':
                videoId[search_result['id']['videoId']]= search_result['snippet']['title']
                #videoId.add(search_result['id']['videoId'],(search_result['snippet']['title']))
    return videoId


def clean_text(text):
    '''
    Utility function to clean the text in a tweet by removing
    links and special characters using regex.
    '''
    clean_text = ' '.join(re.sub("(@[A-Za-z]+)|([^A-Za-z \t])|(\w+:\/\/\S+)", " ", text).split())
    return clean_text


def get_comment_threads(searchName, max_results, developer_key):
    outputDF = pd.DataFrame([])
    videoIds = youtube_search(searchName, developer_key, max_results)
    print("videoIds count : {0}".format(len(videoIds)))
    # videoIds = ['PYN4H0JXBJc']
    for video_id, video_title in videoIds.items():
        youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                        developerKey=developer_key)
        results = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            textFormat="plainText"
        ).execute()

        for item in results["items"]:
            comment = item["snippet"]["topLevelComment"]

            createdTime = comment["snippet"]["publishedAt"]
            text = comment["snippet"]["textDisplay"]
            cleanText = clean_text(text)
            commentID = item['id']
            # print("Comment by %s: at %s: %s" % (author, createdTime,text))
            outputDF = outputDF.append(pd.DataFrame(
                {'videoID': video_id,'videoTitle': video_title, 'CreateTimeStamp': createdTime, 'Comment': cleanText, 'Type': 'Comment', 'CommentID': commentID},
                index=[0]), ignore_index=True)

        for item1 in results["items"]:
            results1 = youtube.comments().list(
                part="snippet",
                parentId=item1['id'],
                textFormat="plainText"
            ).execute()

            for item2 in results1["items"]:
                text1 = item2["snippet"]["textDisplay"]
                cleanText1 = clean_text(text1)
                createdTime1 = item2["snippet"]["publishedAt"]
                replyID = item2['id']
                outputDF = outputDF.append(pd.DataFrame(
                    {'videoID': video_id, 'videoTitle': video_title,'CreateTimeStamp': createdTime1, 'Comment': cleanText1, 'Type': 'Reply', 'CommentID': replyID},
                    index=[0]), ignore_index=True)
        print(video_id)
    return outputDF


def filter_comments(comments_df):
    df = comments_df[comments_df['Comment'].notnull()]
    # filtered_df = df[df['Comment'].str.len() > 0]
    filtered_df = df[df['Comment'].apply(lambda x: len(x.strip()) > 2)]
    return filtered_df


def main():
    if len(sys.argv) < 5:
        print("!!!!! Not enough arguments. You need to provide 4 arguments!!!!")
        print(
            "python GetYoutubeComments.py <Developer Key> <video headline> <output file name> <Number of video to look at>")
        sys.exit(1)
    DEVELOPER_KEY = sys.argv[1]
    search_string = sys.argv[2]
    output_file_name = sys.argv[3]
    max_results = sys.argv[4]
    # SearchString = 'Samsung VR HeadSet'
    comments = get_comment_threads(search_string, max_results, DEVELOPER_KEY)
    comments_filtered = filter_comments(comments)
    comments_filtered.to_csv(output_file_name, sep='\t', index=False)

    print("****End of execution****")


if __name__ == "__main__":
    """
    python GetYoutubeComments.py <Developer Key> <video headline> <output file name> <Number of video to look at>
    e.g.
    python GetYoutubeComments.py <Developer Key> "taylor swift" tswift.csv 5
    """
    main()
