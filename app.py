import streamlit as st
import os
import shutil

# Import from your updated youtube_utils
from youtube_utils import download_media, FFMPEG_PATH, add_ffmpeg_to_path

st.title("YouTube Media Downloader")

# Verify ffmpeg availability and add to PATH
def is_ffmpeg_available() -> bool:
    if shutil.which("ffmpeg"):
        return True
    ffmpeg_exe = os.path.join(FFMPEG_PATH, "ffmpeg.exe")
    if os.path.isfile(ffmpeg_exe):
        add_ffmpeg_to_path()
        return True
    return False

# Check FFmpeg availability
if not is_ffmpeg_available():
    st.error(
        "ffmpeg not found. Please install ffmpeg and ensure it's available in your PATH, "
        f"or adjust FFMPEG_PATH in youtube_utils.py to point to your ffmpeg binary directory. "
        f"Current path: {FFMPEG_PATH}"
    )
    st.stop()

# Sidebar: configure download directory
download_dir = st.sidebar.text_input(
    "Download directory:",
    value=os.path.join(os.getcwd(), "downloads")
)
os.makedirs(download_dir, exist_ok=True)

# Normal widgets (no st.form)
media_option = st.radio(
    "Select media type:",
    ("Audio (MP3)", "Video Low (MP4)", "Video Standard (MP4)", "Video High (MP4)")
)
search_query = st.text_input("Enter song name or YouTube URL:")

# Now this button’s label will always show the current media_option
if st.button(f"Download {media_option}"):
    if not search_query:
        st.warning("Please enter a search query or URL.")
    else:
        st.info(f"Searching and downloading {media_option.lower()} for: {search_query}")
        with st.spinner("Downloading..."):
            try:
                file_path = download_media(search_query, download_dir, media_option)
                if file_path and os.path.exists(file_path):
                    st.success("Download complete!")
                    file_name = os.path.basename(file_path)
                    mime_type = "audio/mpeg" if media_option.startswith("Audio") else "video/mp4"
                    with open(file_path, "rb") as fp:
                        st.download_button(
                            label=f"Download {file_name}",
                            data=fp,
                            file_name=file_name,
                            mime=mime_type
                        )
                else:
                    st.error(
                        "Download failed. Could not find the downloaded file "
                        "or an error occurred during processing."
                    )
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")

st.markdown("---")
st.markdown(
    "Enter the name of a song or a direct YouTube video URL, choose media type "
    "(including low/high quality), and click Download to get your file."
)
