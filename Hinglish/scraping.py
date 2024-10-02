import pandas as pd
from googleapiclient.discovery import build

api_key = 'AIzaSyDLuRq30uFLRW_-2WE_UYCLY1e2UUBkGyA'

youtube = build('youtube', 'v3', developerKey=api_key)

def get_comment_texts(video_id):
    comment_texts = []
    try:
        request = youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            # maxResults=max_results,
            textFormat='plainText'
        )
        response = request.execute()

        while response:
            for item in response['items']:
                comment = item['snippet']['topLevelComment']['snippet']
                comment_texts.append(comment['textDisplay'])

            if 'nextPageToken' in response:
                request = youtube.commentThreads().list(
                    part='snippet',
                    videoId=video_id,
                    pageToken=response['nextPageToken'],
                    # maxResults=max_results,
                    textFormat='plainText'
                )
                response = request.execute()
            else:
                break
    except Exception as e:
        print(f"An error occurred: {e}")

    return comment_texts


def save_comment_texts_to_csv(comment_texts, filename):
    df = pd.DataFrame(comment_texts, columns=['comment_text'])
    df.to_csv(filename, index=False)
    print(f"Comment texts saved to {filename}")

video_id = 'tpyfUCOq1cw'

comment_texts = get_comment_texts(video_id)
save_comment_texts_to_csv(comment_texts, 'Hinglish/HinglishScrapRows1.csv')




