import os
import google.auth
import logging
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Create file handler for logging to file
file_handler = logging.FileHandler('script_log.txt')
file_handler.setLevel(logging.INFO)

# Create stream handler for logging to console
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)

# Define formatter for both handlers
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

# Add handlers to logger
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

# Example logging messages
logger.info('Script started.')

# Kullanıcıdan Playlist ID'sini al
def get_playlist_id():
    playlist_id = input("Enter the Playlist ID: ")
    return playlist_id

# YouTube API'ye kimlik doğrulaması yapma
def authenticate():
    CLIENT_SECRET_FILE = "client_secret.json"  # Bu dosyayı Google Developer Console'dan alın
    API_NAME = "youtube"
    API_VERSION = "v3"
    SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

    if not os.path.exists(CLIENT_SECRET_FILE):
        logger.error("The file 'client_secret.json' is missing. Please add the file to the directory.")
        exit(1)  # Programı sonlandır

    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
    credentials = flow.run_local_server(port=0)

    youtube = build(API_NAME, API_VERSION, credentials=credentials)
    return youtube

# Oynatma listesindeki tüm videoları almak
def get_playlist_items(youtube, playlist_id):
    playlist_items = []
    next_page_token = None

    while True:
        request = youtube.playlistItems().list(
            part="snippet",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        )
        response = request.execute()

        for item in response["items"]:
            video_id = item["snippet"]["resourceId"]["videoId"]
            playlist_items.append(video_id)

        next_page_token = response.get("nextPageToken")

        if not next_page_token:
            break

    return playlist_items

# Tekrar eden videoları kaldırma
def remove_duplicates(youtube, playlist_id):
    logger.info("Fetching playlist items...")
    playlist_items = get_playlist_items(youtube, playlist_id)
    logger.info(f"Total items found: {len(playlist_items)}")

    # Videoları say ve tekrar edenleri tespit et
    video_count = {}
    for video_id in playlist_items:
        video_count[video_id] = video_count.get(video_id, 0) + 1

    duplicate_videos = [video_id for video_id, count in video_count.items() if count > 1]
    logger.info(f"Found duplicate videos: {duplicate_videos}")

    for video_id in duplicate_videos:
        try:
            # Playlist'ten video silme
            request = youtube.playlistItems().list(
                part="snippet",
                playlistId=playlist_id,
                maxResults=50
            )
            response = request.execute()

            for item in response["items"]:
                if item["snippet"]["resourceId"]["videoId"] == video_id:
                    playlist_item_id = item["id"]
                    youtube.playlistItems().delete(id=playlist_item_id).execute()
                    logger.info(f"Removed duplicate video with ID: {video_id}")
        except HttpError as error:
            logger.error(f"HTTP error occurred: {error}")
        except Exception as error:
            logger.error(f"An unexpected error occurred: {error}")

def main():
    youtube = authenticate()
    playlist_id = get_playlist_id()
    remove_duplicates(youtube, playlist_id)

if __name__ == "__main__":
    main()
