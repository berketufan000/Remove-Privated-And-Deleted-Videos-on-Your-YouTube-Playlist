# Remove Deleted & Privated Videos from YouTube Playlist

This script allows you to remove deleted and private videos from your YouTube playlist. It checks each video in the playlist and removes those that are no longer available (either deleted or set to private).

## Features
- Removes deleted and private videos from a specified YouTube playlist.
- The playlist must be from your own YouTube account.
- Automatically authenticates with your Google account for access to the YouTube API.
- Logs the process in both a log file (`script_log.txt`) and to the console.

## Requirements

Before running the script, make sure you have the following:

- Python 3.x
- A `client_secret.json` file from the Google Developer Console.

The `client_secret.json` file must be placed in the same directory as the script. If it's missing, the script will notify you.

## Setup

1. Clone this repository to your local machine:
    ```bash
    git clone https://github.com/your-username/Remove-Deleted-Privated-Videos-YouTube-Playlist.git
    cd Remove-Deleted-Privated-Videos-YouTube-Playlist
    ```

2. Make sure the `client_secret.json` file is present in the root directory. This file is required for authenticating with the YouTube API.

## How It Works

1. **Authentication:**
   - The script starts by asking for Google account authentication using OAuth2. The user will be prompted to log in to their Google account and grant permission to access their YouTube account.
   
2. **Playlist ID:**
   - After authentication, the user is asked to input the **Playlist ID** of the YouTube playlist they want to clean.
   
3. **Checking Videos:**
   - The script fetches all videos from the specified playlist using the YouTube API.
   - It then checks each video to determine if it is deleted or set to private. If a video is no longer available, it is marked for removal.

4. **Removing Videos:**
   - The script then removes any videos that are no longer available (deleted or private) from the playlist.
   - A log of the entire process is created, including details of which videos were removed, which are still available, and any errors encountered.

5. **Logging:**
   - The script logs the results of the operation both to a file (`script_log.txt`) and to the console. This includes information about the total videos found, any duplicate videos identified, and the removal actions taken.

## Usage

1. Run the script by executing either the `run.bat` file (for Windows) or the `run.sh` file (for Linux/macOS). These scripts will automatically start the script.

2. Follow the prompts to log in to your Google account and provide the Playlist ID for the playlist you want to clean.

## Example

```bash
python script.py
