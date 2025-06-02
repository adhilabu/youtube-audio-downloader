import yt_dlp
import os

# Path to your ffmpeg installation (adjust as needed)
FFMPEG_PATH = "C:/ffmpeg-master-latest-win64-gpl-shared/bin"

def add_ffmpeg_to_path():
    """Adds ffmpeg binary directory to system PATH."""
    if FFMPEG_PATH not in os.environ["PATH"]:
        os.environ["PATH"] += os.pathsep + FFMPEG_PATH

def download_media(query, download_path="downloads", media_option="Audio (MP3)"):
    """
    Searches YouTube for the query and downloads audio or video based on media_option.

    Args:
        query (str): The search query or YouTube URL.
        download_path (str): Directory to save the downloaded file.
        media_option (str): One of "Audio (MP3)", "Video Low (MP4)", "Video Standard (MP4)", "Video High (MP4)".

    Returns:
        str: Path to the downloaded file (MP3 or MP4), or None if download failed.
    """
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    # Base ydl_opts; we will modify depending on audio/video
    ydl_opts = {
        'ffmpeg_location': FFMPEG_PATH,
        'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
        'default_search': 'ytsearch1',
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
    }

    # Determine format & postprocessors based on media_option
    if media_option == "Audio (MP3)":
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        })
        expected_ext = '.mp3'

    else:
        # It's video—choose quality
        # yt_dlp allows selecting formats like 'bestvideo[height<=360]+bestaudio' etc.
        if media_option == "Video Low (MP4)":
            # e.g., 360p
            ydl_opts['format'] = 'bestvideo[height<=360]+bestaudio/best'
        elif media_option == "Video Standard (MP4)":
            # e.g., 720p
            ydl_opts['format'] = 'bestvideo[height<=720]+bestaudio/best'
        elif media_option == "Video High (MP4)":
            # e.g., 1080p or best available
            ydl_opts['format'] = 'bestvideo+bestaudio/best'
        else:
            # Fallback to bestvideo+bestaudio
            ydl_opts['format'] = 'bestvideo+bestaudio/best'

        # We want an mp4 container (even if streams come as mkv), so post-process with ffmpeg
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }]
        expected_ext = '.mp4'

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(query, download=True)

            # Extract the video info (either single-video or search result)
            if info_dict and 'entries' in info_dict and info_dict['entries']:
                video_info = info_dict['entries'][0]
            elif info_dict:
                video_info = info_dict
            else:
                print("Error: Could not extract video info.")
                return None

            # Prepare the filename (before extension)
            base_filename = ydl.prepare_filename(video_info)
            downloaded_file_path = os.path.splitext(base_filename)[0] + expected_ext

            # If file exists exactly as expected:
            if os.path.exists(downloaded_file_path):
                print(f"Successfully downloaded: {downloaded_file_path}")
                return downloaded_file_path

            # Otherwise, try to find a matching file in the download directory
            for file in os.listdir(download_path):
                if file.endswith(expected_ext) and video_info.get('title', '') in file:
                    return os.path.join(download_path, file)

            print(f"Error: Expected file not found after download: {downloaded_file_path}")
            return None

    except yt_dlp.utils.DownloadError as e:
        print(f"Error during download: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
