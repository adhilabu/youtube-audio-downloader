import yt_dlp
import os

def download_audio(query, download_path="/home/ubuntu/youtube_audio_downloader/downloads"):
    """Searches YouTube for the query and downloads the audio of the first result.

    Args:
        query (str): The search query for YouTube.
        download_path (str): The directory to save the downloaded audio file.

    Returns:
        str: The path to the downloaded audio file, or None if download failed.
    """
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    ydl_opts = {
        'format': 'bestaudio/best',
        'ffmpeg_location': 'C:/ffmpeg/bin',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
        'default_search': 'ytsearch1', # Search YouTube and get the first result
        'noplaylist': True,
        'quiet': True, # Suppress console output from yt-dlp
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(query, download=True)
            # ydl.download([query]) # This might re-download if extract_info didn't trigger it fully

            # Construct the expected filename after download and conversion
            # Note: This relies on yt-dlp's naming convention and might need adjustment
            # if the title contains characters invalid for filenames.
            # A more robust way might involve hooks, but this is simpler for now.
            if info_dict and 'entries' in info_dict and info_dict['entries']:
                # Handle search results (which are like playlists)
                video_info = info_dict['entries'][0]
            elif info_dict:
                 # Handle direct URL or single video result
                 video_info = info_dict
            else:
                print("Error: Could not extract video info.")
                return None

            # Get the base filename yt-dlp would use (before extension change)
            base_filename = ydl.prepare_filename(video_info)
            # Change the extension to mp3
            downloaded_file_path = os.path.splitext(base_filename)[0] + '.mp3'

            # Check if the file exists (download and conversion successful)
            if os.path.exists(downloaded_file_path):
                print(f"Successfully downloaded and converted: {downloaded_file_path}")
                return downloaded_file_path
            else:
                # Sometimes the filename might differ slightly, try finding the mp3 file
                for file in os.listdir(download_path):
                    if file.endswith(".mp3") and video_info.get('title', '___') in file:
                         print(f"Found matching mp3: {os.path.join(download_path, file)}")
                         return os.path.join(download_path, file)
                print(f"Error: Expected file not found after download: {downloaded_file_path}")
                return None

    except yt_dlp.utils.DownloadError as e:
        print(f"Error during download: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None